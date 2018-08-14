import logging
import threading
from controller import SlaveController
from slave import SlaveService

import SocketServer
import BaseHTTPServer


class CallbackHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)


class AccessHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.server.controller.slave_accept(self.request, self.client_address)


class Access:
    def __init__(self, accessserver, callbackserver):
        self.accessserver = accessserver
        self.callbackserver = callbackserver

    def __server_start(self, server):
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        logging.info("Server loop running in thread:%s", server_thread.name)

    def __server_stop(self, server):
        server.shutdown()
        server.server_close()

    def setup(self):
        service = SlaveService()
        controller = SlaveController(service)
        self.accessserver.controller = controller
        self.callbackserver.controller = controller

        self.__server_start(self.accessserver)
        self.__server_start(self.callbackserver)

    def shutdown(self):
        self.__server_stop(self.accessserver)
        self.__server_stop(self.callbackserver)
