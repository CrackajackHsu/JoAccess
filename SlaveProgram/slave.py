import logging
import json
import socket
import select

class SlaveBase:

    def __init__(self, name):
        self.name = name
        self.socket = None
        self.package_mount = json.dumps({"TYPE": "mount","data":{"name": self.name}}).encode('utf-8')
        self.package_unmount = json.dumps({"TYPE": "unmount"}).encode('utf-8')

    def connectAccess(self, address):
        tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmp_socket.connect(address)
        logging.debug('ConnectAccess:%s', address)
        self.socket = tmp_socket
        self.socket.send(self.package_mount)

    def disconnect(self):
        if self.socket:
            self.socket.send(self.package_unmount)

    def poll(self):
        inputs = [self.socket]
        while inputs:
            readable, writable, exceptional = select.select(inputs, [], inputs)
            if self.socket in readable:
                    data = self.socket.recv(1024)
                    if data:
                        logging.debug('%s', data)
                    else:
                        self.socket.close()
                        self.socket = None
                        raise RuntimeError('socket connection broken')
        
            if self.socket in exceptional:
                self.socket.close()
                self.socket = None
                raise RuntimeError('socket connection broken')