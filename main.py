import logging
from optparse import OptionParser
from ConfigParser import ConfigParser

import SocketServer
import BaseHTTPServer

import access

ACCESS_SERVER_ADDR = None

CALLBACK_SERVER_ADDR = None


class AccessServerImpl(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class CallbackServerImpl(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


def main():
    SocketServer.TCPServer.allow_reuse_address = True
    server_access = AccessServerImpl(ACCESS_SERVER_ADDR, access.AccessHandler)
    logging.info("Access Server:%s", server_access.server_address)

    server_callback = CallbackServerImpl(CALLBACK_SERVER_ADDR, access.CallbackHandler)
    logging.info("Callback Server:%s", server_callback.server_address)

    try:
        server = access.Access(server_access, server_callback)
        server.setup()
        while True:
            pass
    except KeyboardInterrupt:
        logging.warn('EXIT')
    finally:
        server.shutdown()


if __name__ == "__main__":
    usage = 'AccessJo'
    parser = OptionParser(usage)
    parser.add_option('-a', '--addr', type='string', dest='addr', default='', help='IP address for UDP Server')
    parser.add_option('-p', '--port', type='int', dest='port', default='5566', help='Port for UDP Server')
    (options, args) = parser.parse_args()
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S',
                        level=logging.DEBUG)

    #    config = ConfigParser()
    #    config.read('setting.ini')
    #    print config.get('adapter.server.1', 'ip', 1)
    #    print config.get('adapter.server.1', 'port', 1)
    #    print config.get('adapter.server.1', 'path', 1)
    ACCESS_SERVER_ADDR = (options.addr, options.port)
    CALLBACK_SERVER_ADDR = (options.addr, options.port + 1)

    main()
