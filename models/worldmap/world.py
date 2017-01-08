from mongoengine import StringField, Document, IntField, ReferenceField, ListField, dereference
from .constants import COLORS, BIOMES
import random
from models.worldmap.map import Map
from models.worldmap.voronoipoint import VoronoiPoint, get_voronoipoint

def get_world(name, seed, tilesize, octaves, *args, **kwargs):
    w = World.objects.filter(name=name).first()
    if not w:
        w = World(name, seed, tilesize, octaves, *args, **kwargs).save()
    return w

def get_worldlist(name, seed, tilesize, octaves, *args, **kwargs):
    return World.objects

class World(Document):
    name = StringField(required=True, unique=True)
    seed = IntField()
    tilesize = IntField()
    octaves = IntField()

    heightmap = ReferenceField(Map)
    tempmap = ReferenceField(Map)

    def __init__(self, name, seed, tilesize, octaves, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)

        self.name = name
        self.seed = seed
        self.tilesize = tilesize
        self.octaves = octaves

        if not self.heightmap and not self.tempmap:
            self._create_maps()

    def _create_maps(self):
        self.heightmap = Map(self.name + "_height", seed=self.seed, tilesize=self.tilesize, octaves=self.octaves,
                             steps=5).save()
        self.tempmap = Map(self.name + "_temp", seed=self.seed + 1, tilesize=self.tilesize, octaves=self.octaves * 3,
                           steps=6).save()

    def get_temperature(self, px_x, px_y):
        """
        get temperature for a pixel (coords on tilemap)

        :param px_x:
        :param px_y:
        :return:
        """
        return self.tempmap.get_pixel(px_x, px_y)

    def get_height(self, px_x, px_y):
        """
        get height of a pixel (coords on tilemap)

        :param px_x:
        :param px_y:
        :return:
        """
        return self.heightmap.get_pixel(px_x, px_y)

    def get_biome(self, px_x, px_y):
        temp = self.get_temperature(px_x, px_y)
        height = self.get_height(px_x, px_y)
        return BIOMES[height][temp]

    def _save_biome_map(self, tile_x, tile_y):
        h = self.heightmap.get_tile(tile_x, tile_y).data
        t = self.tempmap.get_tile(tile_x, tile_y).data

        # print([str(x) for x in self.heightmap.get_tile(tile_x, tile_y) if x >=4])

        biome_stats = dict.fromkeys(COLORS.keys(), 0)

        biomes = []
        for x in range(len(h)):
            color = COLORS.get(BIOMES[h[x]][t[x]], "255   0   0")
            biome_stats[BIOMES[h[x]][t[x]]] += 1
            if color is "255   0   0":
                print("undefined for height %s and temp %s" % (h[x], t[x]))
            biomes.append(color)

        pixels = self.tilesize ** 2
        for stat in biome_stats:
            biome_stats[stat] = str((biome_stats[stat] * 100) / pixels)
        print("biomes in percent:")

        keys = sorted(biome_stats.keys())
        for k in keys:
            print(" %s: %s" % (k, biome_stats[k]))
        save_biome_as_ppm(self.name, biomes, tile_x, tile_y, self.tilesize)

    def _pixel_to_tile_coords(self, pixel_x, pixel_y):
        """
        get the translate a coordinate on the WHOLE tilemap to coordinate on a SINGLE tile

        :param pixel_x:
        :param pixel_y:
        :return: (tile_x, tile_y)
        """
        tile_x = int(pixel_x / self.tilesize)
        tile_y = int(pixel_y / self.tilesize)

        return tile_x, tile_y

    def get_voronoi(self, x_on_tilemap, y_on_tilemap):
        return get_voronoipoint(self, x_on_tilemap, y_on_tilemap)



def save_biome_as_ppm(name, vals, tile_x, tile_y, tilesize):
    with open("%s_%s_%s.pgm" % (name, tile_x, tile_y), 'wt') as f:
        f.write('P3\n')
        f.write('%s %s\n' % (tilesize, tilesize))  # width, height
        f.write('255\n')  # max greyval
        f.write('\n'.join(val for val in vals) + '\n')
