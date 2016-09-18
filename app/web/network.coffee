console.log("Ok, AutobahnJS loaded", autobahn.version);

## authenticate using authid "joe"
user = "joe";
key = "123";

connected = false
s = false

events = []
incoming_events = []

onchallenge = (session, method, extra) ->
        #console.log("onchallenge", method, extra);

        if (method == "wampcra")
            console.log("onchallenge: authenticating via '" + method + "' and challenge '" + extra.challenge + "'");

            return autobahn.auth_cra.sign(key, extra.challenge);
        else
            throw "don't know how to authenticate using '" + method + "'";

wsuri = ''
if (document.location.origin == "file://")
    wsuri = "ws://127.0.0.1:8080/ws";
else
    if document.location.protocol == "http:"
        protocol = 'ws:'
    else
        protocol = 'wss:'
    wsuri = protocol + "//" + document.location.host + "/ws";

connection = new autobahn.Connection({
    url: wsuri,
    realm: 'realm1',

    # the following attributes must be set of WAMP-CRA authentication
    #
    authmethods: ["wampcra"],
    authid: user,
    onchallenge: onchallenge
});



connection.onopen = (session, details) ->

    console.log("connected session with ID " + session.id);
    console.log("authenticated using method '" + details.authmethod + "' and provider '" + details.authprovider + "'");
    console.log("authenticated with authid '" + details.authid + "' and authrole '" + details.authrole + "'");
    connected = true
    s = session
    console.log(session.subscribe('com.game.rooms.0.0',
        (args, kwargs, details) ->
            console.log('incoming event...: ' + args)
            incoming_events.push({args, kwargs, details})
            return))
    return

connection.onclose = (reason, details) ->
    console.log("disconnected", reason, details.reason, details);
    connected = false
    return

send = (event_dict) ->
        events_topic = 'com.game.events.' + user
        console.log('sending ' + event_dict + ' to ' + events_topic)
        if connected
            console.log()
            s.publish(events_topic, [event_dict], {}, {acknowledge: true})
        else
            console.log('not connected...')
        return

console.log('connecting to ' + wsuri)
connection.open()

append_event = (event) ->
    console.log('adding ' +  event)
    events.push(event)
    


process_incoming = () ->
    #console.log('processing incoming')
    for event in incoming_events
        console.log(event)
        if event['args'][0]['t'] == 'draw'
            draw(event['args'][0]['coords']['x'], event['args'][0]['coords']['y'])
    incoming_events = []


tick = () ->
    if events.length != 0
        console.log('sending ' + events.length + ' events')
    for event in events
        send(event)
    events = []
    process_incoming()
    # Schedule this.tick to be invoked again
    # in 16 milliseconds (around 60 ticks per second).
    setTimeout(tick, 16);


tick()