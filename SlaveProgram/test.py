import logging
import slave
from optparse import OptionParser


class TestHandler(slave.SlaveBase):
    def __init__(self):
        slave.SlaveBase.__init__(self, 'TEST')

    def onIdle(self):
        pass


def main():
    client = TestHandler()
    try:
        client.connectAccess(('127.0.0.1',5566))
        client.poll()
    except RuntimeError as e:
        logging.error('Error in Connection: %s', e.message)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()


if __name__ == "__main__":
    usage = 'TEST Handler'
    parser = OptionParser(usage)
    parser.add_option('-a', '--addr', type='string', dest='addr', default='', help='IP address for UDP Server')
    parser.add_option('-p', '--port', type='int', dest='port', default='5566', help='Port for UDP Server')
    (options, args) = parser.parse_args()
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S',
                        level=logging.DEBUG)
    main()
