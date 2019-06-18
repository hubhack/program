# 聊天，群聊 TCP
# TCP Server 端开发
import socket
import time
import datetime
import threading
import logging

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.sock = socket.socket()
        self.addr = ip, port
        self.event = threading.Event()
        self.clients = {}
        self.lock = threading.Lock()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()
        threading.Thread(target=self.accept, name='accept').start()

    def accept(self):
        while not self.event.is_set():
            newsock, clientinfo = self.sock.accept()
            with self.lock:
                self.clients[clientinfo] = newsock # 增加item
            threading.Thread(target=self.recv, name='recv', args=(newsock, clientinfo)).start()

    def recv(self, sock:socket.socket, clientinfo):
        while not self.event.is_set():
            try:
                data = sock.recv(1024) # 阻塞等待信息
            except Exception as e:
                logging.error(e)
                data = b''
            print(data) # bytes

            if data.strip() == b'quit' or data.strip() == b'':
                with self.lock:
                    self.clients.pop(clientinfo)
                sock.close()
                break

            msg = "{:%Y/%m/%d %H:%M:%S} [{}:{}] - {}".format(datetime.datetime.now(),
                            *clientinfo, data.decode())

            exps = []
            expc = []
            with self.lock:
                for c, s in self.clients.items():
                    try:
                        s.send(msg.encode()) # 有可能出错
                    except:
                        exps.append(s)
                        expc.append(c)
                for c in expc:
                    self.clients.pop(c)

            for s in exps:
                s.close()

    def stop(self):
        self.event.set()
        keys = []
        with self.lock:
            keys = list(self.clients.values())
            self.clients.clear()
        for s in keys:
            s.close()
        self.sock.close()


cs = ChatServer()
cs.start()

while True:
    cmd = input('>>').strip()
    if cmd == 'quit':
        cs.stop()
        break
    logging.info(threading.enumerate())
















