from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep



class GameLoopSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        events = []
        active_rooms = {
            # (0,0): room_object
        }

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

        def ret(event):
            t = 'com.game.rooms.0.0'
            print('returning %s on %s' % (event['msg'], t))
            print(self.publish(t, event['msg'], x=1))

        while True:
            for event in events:
                ret(event)
            events = []
            yield sleep(1/16)
