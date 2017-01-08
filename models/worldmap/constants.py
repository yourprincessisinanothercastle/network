# http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/#biomes
BIOMES = [[0 for x in range(6)] for y in range(5)]  # will have coords: height, temp

BIOMES[0][0] = "ice"  # dry, low
BIOMES[0][1] = "ice"
BIOMES[0][2] = "water"
BIOMES[0][3] = "water"
BIOMES[0][4] = "water"
BIOMES[0][5] = "water"

BIOMES[1][0] = "subtropical_desert"  # dry, low
BIOMES[1][1] = "grassland"
BIOMES[1][2] = "tropical_seasonal_forest"
BIOMES[1][3] = "tropical_seasonal_forest"
BIOMES[1][4] = "tropical_rainforest"
BIOMES[1][5] = "tropical_rainforest"

BIOMES[2][0] = "temperate desert"
BIOMES[2][1] = "grassland"
BIOMES[2][2] = "grassland"
BIOMES[2][3] = "temperate_deciduous_forest"
BIOMES[2][4] = "temperate_deciduous_forest"
BIOMES[2][5] = "temperate_rain_forest"

BIOMES[3][0] = "temperate_desert"
BIOMES[3][1] = "temperate_desert"
BIOMES[3][2] = "shrubland"
BIOMES[3][3] = "shrubland"
BIOMES[3][4] = "taiga"
BIOMES[3][5] = "taiga"

BIOMES[4][0] = "scorched"
BIOMES[4][1] = "bare"
BIOMES[4][2] = "tundra"
BIOMES[4][3] = "tundra"
BIOMES[4][4] = "snow"
BIOMES[4][5] = "snow"


COLORS = {
    "snow":                         "255 255 255",
    "tundra":                       "221 221 187",
    "bare":                         "187 187 187",
    "scorched":                     "153 153 153",
    "taiga":                        "204 212 187",
    "shrubland":                    "196 204 187",
    "temperate_desert":             "228 232 202",
    "temperate_rain_forest":        "164 196 168",
    "temperate_deciduous_forest":   "180 201 169",
    "grassland":                    "196 212 170",
    "subtropical_desert":           "233 221 199",
    "temperate desert":             "228 232 202",
    "tropical_rainforest":          "156 187 169",
    "tropical_seasonal_forest":     "169 204 164",
    "ice":                          "30  250 250",
    "water":                        "0   100 250"
}

BASE_FREQUENCE = 2.0

TILESIZE = 32
