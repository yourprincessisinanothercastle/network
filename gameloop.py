from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

import config

from worldmap.world import get_world
from worldmap import db

world_name = 'test16'


class GameLoopSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        active_rooms = {
            # id: room_object
        }
        users = {
            # username: player_object
        }

        world = get_world(world_name, 321, 8, 8)

        # inline defined network-related methods
        # - subscribe to all player events
        def user_event(msg, details=None):
            username = details.topic.split('.')[-1]
            event = msg

        try:
            topic = u'com.game.events'
            yield self.subscribe(user_event, topic, options=SubscribeOptions(match=u"prefix", details_arg="details"))
            print('subscribed ' + topic)

        except Exception as e:
            print('something wrong while subscribing! %s' % e)

        def get_voronoi(x, y):
            v = world.get_voronoi(x, y)
            return {'shape': v.shape,
                    'biome': v.biome,
                    'neighbors': [[n.x_on_tilemap, n.y_on_tilemap] for n in v.neighbors],
                    "x_on_tilemap": x,
                    "y_on_tilemap": y,
                    "height": v.height
                    }

        def bulk_get_voronoi(tuples):
            voronois = []
            for t in tuples:
                voronois.append(get_voronoi(t[0], t[1]))
            return voronois

        self.register(get_voronoi, 'com.game.get_voronoi')
        self.register(bulk_get_voronoi, 'com.game.bulk_get_voronoi')

    def onClose(self, wasClean):
        print('deleting world')
        db.drop_database(world_name)
