import socket
import json
import time
import argparse


class Client():
    def __init__(self,
                 id,
                 status,
                 ip='127.0.0.1',
                 port=8081):
        self.SENDER = 0
        self.RECEIVER = 1
        self.BUFFER_SIZE = 1024

        self.data = ''
        self.id = id
        self.status = status
        self.socket = socket.socket()
        self.socket.connect((ip, port))

    def receive(self, remote_id):
        data = {'id': self.id,
                'remote_id': remote_id,
                'id_status': self.status,
                'status': '0',
                'data': ''}
        remote_data = json.dumps(data).encode('utf-8')
        self.socket.send(remote_data)
        time.sleep(0.001)
        return json.loads(self.socket.recv(self.BUFFER_SIZE).decode('utf-8'))


    def send(self, remote_id, data):
        data = {'id': self.id,
                'remote_id': remote_id,
                'id_status': self.status,
                'status': '0',
                'data': data}
        remote_data = json.dumps(data).encode('utf-8')
        self.socket.send(remote_data)
        time.sleep(0.001)
        status = json.loads(self.socket.recv(self.BUFFER_SIZE).decode('utf-8'))['status']
        return status

    def do(self, remote_id, hz=50):
        while True:
            if self.status == self.SENDER:
                # ===========================
                # 消息在这里写
                input_info = input('>>>')
                # ===========================
                status = self.send(remote_id, input_info)
                print(status)

            else:
                msg = self.receive(remote_id)
                # ===========================
                # 消息在这里写
                data_info = msg['data']
                if data_info != self.data:
                    print(data_info)
                    self.data = data_info
                # ===========================

            time.sleep(1/hz)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m_id', '--id')
    parser.add_argument('-r_id','--remote_id')
    parser.add_argument('-s','--status', type=int)
    args = parser.parse_args()

    client = Client(args.id, args.status)
    client.do(args.remote_id)
