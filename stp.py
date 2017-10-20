import stomp
import config as c

class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)
    def on_message(self, headers, message):
        print('received a message %s' % message)


class Messenger(object):

    def __init__(self, host, port=61613, destination=''):
        self.aq = stomp.Connection12([(host, port)])
        # self.aq.set_listener('', MyListener())
        self.aq.start()
        self.aq.connect(username=c.config['Stomp']['Username'], passcode=c.config['Stomp']['Password'])
        self.des = destination
        self.aq.subscribe(destination=destination, id=1, ack='auto')


    def addQueue(self, jstring):
        if jstring is not None:
            self.aq.send(body=jstring, destination=self.des)

    def close(self):
        self.aq.disconnect()