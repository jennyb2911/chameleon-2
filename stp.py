import stomp
import config as c


class Messenger:
    def __init__(self, host, port=61613, destination=''):
        self.aq = stomp.Connection12([(host, port)])
        self.aq.start()
        self.aq.connect(username=c.config['Aq']['Username'], passcode=c.config['Aq']['Password'])
        self.des = destination
        self.aq.subscribe(destination=destination, id=1, ack='auto')

    def addqueue(self, jstring):
        if jstring is not None:
            self.aq.send(body=jstring, destination=self.des)

    def close(self):
        self.aq.disconnect()