from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks


class GameLoopSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("gameloop session joined: {}".format(details))

        def userevent(msg):
            print('userevent on {}: {}!'.format(topic, msg))

        try:
            topic = u'com.game.user'
            yield self.subscribe(userevent, topic)
            print('subscribed ' + topic)

        except Exception as e:
            print('something wrong while subscribing! %s' % e)

