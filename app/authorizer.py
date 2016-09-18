from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession


class UserAuthorizer(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("MyAuthorizer.onJoin({})".format(details))
        try:
            yield self.register(self.authorize, 'com.game.authorize')
            print("MyAuthorizer: authorizer registered")
        except Exception as e:
            print("MyAuthorizer: failed to register authorizer procedure ({})".format(e))

    def authorize(self, session, uri, action):
        allowed = [
            {
                "action": 'publish',
                "uri": "com.game.events.%s" % session['authid']
            }
        ]
        for rule in allowed:
            if action == rule['action'] and uri == rule['uri']:
                return True
        return False
