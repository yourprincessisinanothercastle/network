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

COLORS = {
    "snow":                         "rgb(255,255,255)",
    "tundra":                       "rgb(221,221,187)",
    "bare":                         "rgb(187,187,187)",
    "scorched":                     "rgb(153,153,153)",
    "taiga":                        "rgb(204,212,187)",
    "shrubland":                    "rgb(196,204,187)",
    "temperate_desert":             "rgb(228,232,202)",
    "temperate_rain_forest":        "rgb(164,196,168)",
    "temperate_deciduous_forest":   "rgb(180,201,169)",
    "grassland":                    "rgb(196,212,170)",
    "subtropical_desert":           "rgb(233,221,199)",
    "temperate desert":             "rgb(228,232,202)",
    "tropical_rainforest":          "rgb(156,187,169)",
    "tropical_seasonal_forest":     "rgb(169,204,164)",
    "ice":                          "rgb(30,250,250)",
    "water":                        "rgb(0,100,250)"
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

offset = 250

draw_polygon = (coords, biome) ->
    p = new Path2D();
    p.moveTo(coords[0][0]+offset, coords[0][1]+offset)
    for coord in coords
      p.lineTo(coord[0]+offset, coord[1]+offset)
    p.lineTo(coords[0][0]+offset, coords[0][1]+offset)
    ctx.fillStyle   = COLORS[biome]
    console.log(COLORS[biome])
    ctx.stroke()
    ctx.fill(p)
    p.closePath()

drawn_tiles = 0
tiles_to_draw = 100

drawn = []

get_and_draw = (x, y) ->

  if R.indexOf([x, y], drawn) < 0
    drawn.push([x, y])
    s.call('com.game.get_voronoi', [x, y]).then(
      (voronoi) ->
        console.log("vor:", voronoi)
        draw_polygon(voronoi.shape, voronoi.biome)
        drawn_tiles += 1
        for n in voronoi.neighbors
          if tiles_to_draw > drawn_tiles
            console.log('next...')
            get_and_draw(n[0], n[1])
        return
    ,
      (error) ->
        console.log("Call failed:", error)
    )
  else
    console.log(drawn)
    console.log([x, y] + ' already drawn')


connection.onopen = (session, details) ->
  console.log("connected session with ID " + session.id);
  console.log("authenticated using method '" + details.authmethod + "' and provider '" + details.authprovider + "'");
  console.log("authenticated with authid '" + details.authid + "' and authrole '" + details.authrole + "'");
  connected = true
  s = session

  get_and_draw(0, 0)

  return



connection.onclose = (reason, details) ->
  console.log("disconnected", reason, details.reason, details);
  connected = false
  return





ctx = canvas.getContext('2d');

painting = document.getElementById('paint');
paint_style = getComputedStyle(painting);
canvas.width = parseInt(paint_style.getPropertyValue('width'));
canvas.height = parseInt(paint_style.getPropertyValue('height'));

ctx.lineWidth = 1;
ctx.strokeStyle = '#00CC99';

console.log('connecting to ' + wsuri)
connection.open()