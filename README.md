# boring, uninteresting network stuff

this uses crossbar.io

```
pip install crossbar
cd app
crossbar start
```

this will start a webserver on localhost:8080
(then point your browser to localhost:8080)

what this does:

crossbar is a "router" for components in a websocket network. this starts a backend service, an authenticator, an authorizer and a dummy-gameloop.

the served index.html has a user "joe" preconfigured. he is allowed to post messages to a topic "com.game.events.joe" (where joe is always the current user. peter is not alowed to post on joes topic.)

joe posts a message there, the backend logs should log them.
