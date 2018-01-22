#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson8-5---如何实现线程池？

案例：我们之前实现了一个多线程web视频监控服务器，我们需要对请求连接数做限制，以防止恶意用户发起大量连接而导致服务器
创建大量线程，最终因资源耗尽而瘫痪。
可以使用线程池，替代原来的每次请求创建线程。

方案：在python3中，使用标准库中concurrent.futures下的ThreadPoolExecutor对象的submit和map方法，
用来启动线程池中线程执行任务
'''


import os, cv2, time, struct, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import TCPServer, ThreadingTCPServer
from threading import Thread, RLock
from select import select

class JpegStreamer(Thread):
    def __init__(self, camera):
        Thread.__init__(self)
        self.cap = cv2.VideoCapture(camera)
        self.lock = RLock()
        self.pipes = {}

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
        os.close(pr)
        os.close(pw)

    def capture(self):
        cap = self.cap
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                #ret, data = cv2.imencode('.jpg', frame)
                ret, data = cv2.imencode('.jpg', frame, (cv2.IMWRITE_JPEG_QUALITY, 40))
                yield data.tostring()

    def send(self, frame):
        n = struct.pack('l', len(frame))
        self.lock.acquire()
        if len(self.pipes):
            _, pipes, _ = select([], iter(self.pipes.values()), [], 1)
            for pipe in pipes:
                os.write(pipe, n)
                os.write(pipe, frame)
        self.lock.release()

    def run(self):
        for frame in self.capture():
            self.send(frame)

class JpegRetriever(object):
    def __init__(self, streamer):
        self.streamer = streamer
        self.local = threading.local()

    def retrieve(self):
        while True:
            ns = os.read(self.local.pipe, 8)
            n = struct.unpack('l', ns)[0]
            data = os.read(self.local.pipe, n)
            yield data

    def __enter__(self):
        if hasattr(self.local, 'pipe'):
            raise RuntimeError()

        self.local.pipe = streamer.register()
        return self.retrieve()

    def __exit__(self, *args):
        self.streamer.unregister(self.local.pipe)
        del self.local.pipe
        return True

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
        self.send_header('Content-type', 'multipart/x-mixed-replace;boundary=abcde')
        self.end_headers()

        with self.retriever as frames:
            for frame in frames:
                self.send_frame(frame)

    def send_frame(self, frame):
        s  = '--abcde\r\n'
        s += 'Content-Type: image/jpeg\r\n'
        s += 'Content-Length: %s\r\n\r\n' % len(frame)
        self.wfile.write(s.encode('ascii'))
        self.wfile.write(frame)


from concurrent.futures import ThreadPoolExecutor


class ThreadingPoolTCPServer(ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, max_thread=100):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.executor = ThreadPoolExecutor(max_thread)

    def process_request(self, request, client_address):
        """Start a new thread to process the request."""
        self.executor.submit(self.process_request_thread, request, client_address)


if __name__ == '__main__':
    streamer = JpegStreamer(0)
    streamer.start()

    retriever = JpegRetriever(streamer)
    Handler.setJpegRetriever(retriever)

    print('Start server...')
    httpd = ThreadingPoolTCPServer(('', 9000), Handler, max_thread=3)
    httpd.serve_forever()

'''
课后小结&拓展：
    1.concurrent.futures.ThreadPoolExecutor(max_workers=None)
    线程池，规定了最多可以进行的线程数，用于防止恶意执行过多线程。
'''