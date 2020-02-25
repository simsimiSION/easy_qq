import socket
import json
from threading import Thread, Lock

class Server():
    def __init__(self,
                 id,
                 ip='127.0.0.1',
                 port=8081):
        self.SENDER = 0
        self.RECEIVER = 1
        self.BUFFER_SIZE = 1024

        self.data = {}
        self.id = id
        self.lock = Lock()
        self.socket = socket.socket()
        self.socket.bind((ip, port))

    def msg_handle(self, msg):
        msg_status = msg['id_status']
        if msg_status == self.SENDER:
            self.lock.acquire()
            self.data[msg['remote_id']+':'+msg['id']] = msg
            self.lock.release()
            # 接受成功回响
            msg['status'] = '200'
        else:
            self.lock.acquire()
            if msg['id']+':'+msg['remote_id'] in self.data:
                msg['data'] = self.data[msg['id']+':'+msg['remote_id']]['data']
                msg['status'] = '200'
            else:
                msg['status'] = '404'
            self.lock.release()
        return msg

    def worker(self, conn):
        while True:
            try:
                msg = json.loads(conn.recv(self.BUFFER_SIZE).decode('utf-8'))

                # ===========================
                # 执行消息处理事件
                msg = self.msg_handle(msg)
                print('status: {}, data: {}'.format(msg != '', msg))
                # ===========================
                conn.send(json.dumps(msg).encode('utf-8'))

            except Exception:
                print('远程主机强迫关闭了一个现有的连接，续继等待其它的连接。')
                break

    def start(self):
        self.socket.listen()

        while True:
            conn, addr = self.socket.accept()
            Thread(target=self.worker, args=(conn, )).start()

        self.socket.close()


if __name__ == '__main__':
    server = Server('server')
    server.start()



