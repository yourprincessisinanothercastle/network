from pprint import pprint

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from models.users.user import get_user, User


class AuthenticatorSession(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      print("WAMP-Ticket dynamic authenticator joined: {}".format(details))

      def authenticate(realm, authid, details):
         print("WAMP-Ticket dynamic authenticator invoked: realm='{}', authid='{}', details=".format(realm, authid))
         pprint(details)

         u = get_user(authid)
         print('got %s' % u)
         if u:
            ticket = details['ticket']

            if not u.verify(ticket):
               raise ApplicationError(u'com.game.invalid_ticket',
                                      "could not authenticate session - invalid ticket '{}' for principal {}".format(ticket, authid))

            if realm and realm != u.realm:
               raise ApplicationError(u'com.example_invalid_realm',
                                      "user {} should join {}, not {}".format(authid, u.realm, realm))
            print('returning response...')
            res = {
               u'realm': u.realm,
               u'role': u.role,
               u'extra': {
                  u'my-custom-welcome-data': [1, 2, 3]
               }
            }
            print("WAMP-Ticket authentication success: {}".format(res))
            return res
         else:
            raise ApplicationError("com.game.no_such_user", "could not authenticate session - no such principal {}".format(authid))

      try:
         yield self.register(authenticate, 'com.game.authenticate')
         print("WAMP-Ticket dynamic authenticator registered!")
      except Exception as e:
         print("Failed to register dynamic authenticator: {0}".format(e))