import logging
import json
from datetime import datetime


class SlaveConnection:

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.connect_time = datetime.now()
        self.wdt = self.connect_time
        self.slave = None

    def parse(self, buf):
        message = json.loads(buf)
        msg_type = message.get('TYPE')
        msg_data = message.get('data', None)

        self.wdt = datetime.now()

        if msg_type == 'mount':
            name = msg_data.get('name', None)
            if self.slave:
                logging.warning('@%s Double mount', self.address)
            else:
                import importlib
                module = importlib.import_module('handler.' + name.lower())
                class_ = getattr(module, name.lower())
                self.slave = class_()
        else:
            method_name = 'handle_' + msg_type
            if hasattr(self.slave, method_name):
                method = getattr(self.slave, method_name)
                method(msg_data)
            else:
                logging.warning('Slave object has no attribute:%s', method_name)


class SlaveService:

    def __init__(self):
        pass

    def entry(self, connection):
        reply_data = dict()
        reply_data['time'] = connection.connect_time.isoformat()
        reply_data['version'] = 'v0.01'
        socket = connection.socket
        sent = socket.send(json.dumps(reply_data).encode('utf-8'))
        if sent == 0:
            raise RuntimeError("socket connection broken")

        socket.settimeout(60)
        while True:
            try:
                chunk = socket.recv(1024)
                if chunk == '':
                    raise RuntimeError("socket connection broken")
                logging.debug("chunk:%s", chunk)
                connection.parse(chunk)
            except IOError as e:
                logging.warning('@%s IOError:%s', connection.address, e)
                raise RuntimeError(e)
