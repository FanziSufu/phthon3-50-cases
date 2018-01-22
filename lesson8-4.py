#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson8-4---如何使用线程本地数据

案例：我们实现了一个web视频监控服务器，服务器端采集摄像头数据，客户端使用浏览器通过http请求接收数据。服务器使用推送
的方式（multipart/x-mixed-replace)一直使用一个tcp连接向客户端传递数据，这种方式将持续占用一个线程，导致单线程
服务器无法处理多客户端请求。
改写程序，在每个线程中处理一个客户端请求，支持多客户端访问。

方案：threading.local函数可以创建线程本地数据空间。 其下属性对每个线程独立存在
'''

import os, cv2, time, struct, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import TCPServer, ThreadingTCPServer
from threading import Thread, RLock
from select import select

# 从摄像头获取数据源
class JpegStreamer(Thread):
    def __init__(self, camera):
        Thread.__init__(self)
        self.cap = cv2.VideoCapture(camera)
        self.lock = RLock()
        self.pipes = {}

    # 获取数据
    def register(self):
        pr, pw = os.pipe()
        self.lock.acquire()
        self.pipes[pr] = pw
        self.lock.release()
        return pr

    def unregister(self, pr):
        self.lock.acquire()
        pw = self.pipes.pop(pr)
        self.lock.release()
        pr.close()
        pw.close()

    # 采集数据
    def capture(self):
        cap = self.cap
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # ret, data = cv2.imencode('.jpg', frame)
                ret, data = cv2.imencode('.jpg', frame, (cv2.IMWRITE_JPEG_QUALITY, 40))
                yield data.tostring()

    # 发送数据
    def send(self, frame):
        n = struct.pack('l', len(frame))
        self.lock.acquire()
        if len(self.pipes):
            _, pipes, _ = select([], self.pipes.itervalues(), [], 1)
            for pipe in pipes:
                os.write(pipe, n)
                os.write((pipe, frame))
        self.lock.release()

    def run(self):
        for frame in self.capture():
            self.send(frame)


# 加工数据源
class JpegRetriever(object):
    def __init__(self, streamer):
        self.streamer = streamer
        self.local = threading.local()

    def retriver(self):
        while True:
            ns = os.read(self.local.pipe, 8)
            n = struct.unpack('l', ns)[0]
            data = os.read(self.local.pipe, n)
            yield data

    def __enter__(self):
        if hasattr(self.local, 'pipe'):
            raise RuntimeError()

        self.local.pipe = streamer.register()
        return self.retriver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.streamer.unregister(self.local.pipe)
        del self.local.pipe
        return True


# 建立HTTP连接，与客户端交互
class Handler(BaseHTTPRequestHandler):
    retriever = None
    @staticmethod
    def setJpegRetriever(retriever):
        Handler.retriever = retriever

    def do_GET(self):
        if self.retriever is None:
            raise RuntimeError('no retriver')

        if self.path != '/':
            return

        self.send_response(200)
        self.send_header("conten-type", 'multipart/x-mixed-replace;boundary=abcde')
        self.end_headers()

        with self.retriever as frame:
            for frame in frame:
                self.send_frame(frame)

    def send_frame(self, frame):
        self.wfile.write('--abcde\r\n')
        self.wfile.write('Content-Type: image/jpeg\r\n')
        self.wfile.write('Content-Length: %d\r\n\r\n' % len(frame))
        self.wfile.write(frame)


if __name__ == '__mail__':

    streamer = JpegStreamer(0)
    streamer.start()

    retriever = JpegRetriever(streamer)
    Handler.setJpegRetriever(retriever)

    print('start server...')
    httpd = ThreadingTCPServer((', 9000', Handler))
    http.server_forever()

'''
课后小结&拓展;
    1.本结内容没有进行深入研究，未接触过的知识点太多，且本地没有摄像头，无法测试代码。以目前的水平研究透，
    可能用掉大量的时间和精力最后还是有很多不解之处。考虑到效率问题，暂时先把这部分内容放下，以后若有合适的需求
    再来研究。代码照着课程抄了一遍，可能有抄错的地方，没有进行过调试，仅供参考。
    2.本结的主要知识点是 threading.local()的应用
    使用该函数，可以规定某变量只能在此线程中使用。本例中应用该函数，实现了每个客户端都有自己的管道变量，从而可以让
    多个客户端同时访问
    3.cv2是跟计算机视觉相关的库，安装openCV就有了。人脸识别跟这套程序有关
'''