import logging
import slave


class SlaveController:
    def __init__(self, service):
        self.service = service
        self.slaveConnections = dict()

    def slave_accept(self, socket, address):
        logging.info('@%s%s', address, socket)
        self.slaveConnections[socket] = slave.SlaveConnection(socket, address)
        try:
            self.service.entry(self.slaveConnections[socket])
        except RuntimeError as e:
            pass
        self.slaveConnections.pop(socket)
