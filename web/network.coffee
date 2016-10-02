console.log("Ok, AutobahnJS loaded", autobahn.version);

## authenticate using authid "joe"
user = "joe";
key = "123";

connected = false
s = false

# list of local events to send to the server
# will be set to [] after sending
local_events = []

# to store state of the room
room_data = {
    # id: data
}

# puffer to store events for a room
# gets merged to room_data as often as possible
room_events = {
    # id: []
}

onchallenge = (session, method, extra) ->
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

add_room_events = (args, kwargs, details) ->
    """
    callback for the specific room events
    """
    #console.log('incoming event...: ' + args)
    room_events[room_id].push({args, kwargs, details})

set_room_data = (room_id, data) ->
    """
    set the room data for a joined room.
    """
    rooms[room_id] = data


join_room = (room_id, data) ->
    """
    let this client join a room
    called via rpc from the server.

    subscribes to the room events,
    sets room data
    """
    set_room_data(room_id, data)
    session.subscribe('com.game.rooms.' + room_id, add_room_events)


connection.onopen = (session, details) ->
    console.log("connected session with ID " + session.id);
    console.log("authenticated using method '" + details.authmethod + "' and provider '" + details.authprovider + "'");
    console.log("authenticated with authid '" + details.authid + "' and authrole '" + details.authrole + "'");
    connected = true
    s = session
    session.register('com.game.join_room.' + user, join_room)  # RPC: backend can set room data on client
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
    #console.log('adding ' +  event)
    events.push(event)
    
