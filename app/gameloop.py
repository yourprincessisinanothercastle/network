from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions

from twisted.internet.defer import inlineCallbacks

from time import sleep

events = []
active_rooms = {
    # (0,0): room_object
}

class GameLoopSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("gameloop session joined: {}".format(details))

        def userevent(msg, details=None):
            events.append({'user': details.topic.split('.')[-1], 'msg': msg})
            print('userevent on {}: {} ({})!'.format(details.topic.split('.')[-1], msg, details))
        try:
            topic = u'com.game.events'
            yield self.subscribe(userevent, topic, options=SubscribeOptions(match=u"prefix", details_arg="details"))
            print('subscribed ' + topic)

        except Exception as e:
            print('something wrong while subscribing! %s' % e)
