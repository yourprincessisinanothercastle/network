class Player:
    def __init__(self, name, color='#000000'):
        self.name = name
        self.color = color

        self.room = None

        self.coords = None

    def enter_room(self, room):
        room.players.append(self)
        self.room = room
