from mongoengine import StringField, Document, IntField, ReferenceField, ListField
from noise.perlin import SimplexNoise

import random

from .constants import BASE_FREQUENCE



class Tile(Document):
    tilesize = IntField()
    data = ListField(IntField(), default=list)
    name = StringField()
    seed = IntField()
    octaves = IntField()
    steps = IntField()
    x = IntField()
    y = IntField()

    def __init__(self, name, seed, tilesize, octaves, steps, x, y, *args, **kwargs):
        """
        generate a tile

        :param tile_x:
        :param tile_y:
        :param save:
        :return:
        """
        Document.__init__(self, *args, **kwargs)

        self.name = name
        self.seed = seed
        self.tilesize = tilesize
        self.octaves = octaves
        self.steps = steps

        self.r = random.Random(self.seed)

        # shuffle the permutation list
        self.n = SimplexNoise()
        perm_list = list(self.n.permutation)
        self.r.shuffle(perm_list)
        self.n.permutation = tuple(perm_list)

        self.freq = BASE_FREQUENCE * self.octaves  # size of the blobs

        self.x = x
        self.y = y

        if not self.data:
            #print('creating new tile for %s: %s, %s' % (name, x, y))
            self.generate()

    def generate(self):
        tile_x = self.x
        tile_y = self.y

        vals = []
        for y in range(self.tilesize):
            for x in range(self.tilesize):
                value = self.n.noise2((x + self.tilesize * tile_x) / self.freq, (y + self.tilesize * tile_y) / self.freq)
                # print('val: %s' % value)
                vals.append(int(value * (self.steps / 2) + (
                    self.steps / 2)))  # scale up & shift negative values above zero and append
        # print(self.name + ' '.join([str(x) for x in vals if x >= 4]))
        self.data = vals

    def get_pixel(self, x, y):
        return self.data[y * self.tilesize + x]
