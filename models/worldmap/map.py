from mongoengine import StringField, Document, IntField

from models.worldmap.tile import Tile
from collections import OrderedDict

cache = OrderedDict()
cachesize = 10000

class Map(Document):
    name = StringField(required=True, unique=True)
    seed = IntField()
    tilesize = IntField()
    octaves = IntField()
    steps = IntField()

    def __init__(self, name, seed, tilesize, octaves, steps, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        self.name = name
        self.seed = seed
        self.tilesize = tilesize
        self.octaves = octaves
        self.steps = steps

        self.tilecache = OrderedDict()
        self.cachesize = 1000

    def get_tile(self, tile_x, tile_y):
        """
        get a created tile or create a new one

        :param tile_x:
        :param tile_y:
        :return:
        """
        # check if its cached
        tile = self.tilecache.get((self.name, tile_x, tile_y), False)
        if tile:
            return tile

        tile = Tile.objects.filter(name=self.name, x=tile_x, y=tile_y).first()
        if not tile:
            tile = self._make_tile(tile_x, tile_y)
        self.tilecache[(self.name, tile_x, tile_y)] = tile
        while len(self.tilecache) > self.cachesize:
            self.tilecache.popitem(last=False)
        return tile

    def _make_tile(self, tile_x, tile_y, save=False):
        t = Tile(self.name, self.seed, self.tilesize, self.octaves, self.steps, tile_x, tile_y)
        # save_as_pgm(tile_x, tile_y)
        t.save()
        return t

    def get_pixel(self, x, y):
        """
        get the value for a specific pixel anywhere on the map
        creates the corresponding tile if needed

        :param x:
        :param y:
        :return:
        """
        tile_x = x / (self.tilesize)
        tile_y = y / (self.tilesize)

        x_on_tile = x % self.tilesize
        y_on_tile = y % self.tilesize

        neg_x = self.tilesize - (self.tilesize - x_on_tile) -1
        pos_x = x_on_tile

        neg_y = self.tilesize - (self.tilesize - y_on_tile) -1
        pos_y = y_on_tile

       # print('getting %s %s' % (x, y))

        if x < 0 and y < 0:
            x_on_tile = neg_x
            y_on_tile = neg_y
        elif x < 0 and y >= 0:
            x_on_tile = neg_x
            y_on_tile = pos_y
        elif x >= 0 and y < 0:
            x_on_tile = pos_x
            y_on_tile = neg_y
        elif x >= 0 and y >= 0:
            x_on_tile = pos_x
            y_on_tile = pos_y

        if tile_x < 0:
            tile_x -= 1

        if tile_y < 0:
            tile_y -= 1

        #print('pixel %s, %s results in tile %s, %s' % (x, y, tile_x, tile_y))

        tile = self.get_tile(int(tile_x), int(tile_y))
        try:
            return tile.get_pixel(x_on_tile, y_on_tile)
        except Exception as e:
            print('failed on %s %s' % (x_on_tile, y_on_tile))

    def save_as_pgm(self, tile_x, tile_y):
        name = self.name
        vals = self.get_tile(tile_x, tile_y).data
        tilesize = self.tilesize
        steps = self.steps
        with open("%s_%s_%s.pgm" % (name, tile_x, tile_y), 'wt') as f:
            f.write('P2\n')
            f.write('%s %s\n' % (tilesize, tilesize))  # width, height
            f.write('255\n')  # max greyval
            f.write('\n'.join(str(int(val / steps * 255)) for val in vals) + '\n')
