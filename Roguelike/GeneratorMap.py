"""MAP GENERATOR W/ CORRIDORS"""

from Load import *
from math import sqrt
from random import random, randrange, randint, choice

class Dungeon:
    def __init__(self, obj):
        self.object = obj

    def get_map(self):
        return self.object

class Room:
    def __init__(self, row, col, height, width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width

class DungeonGenerator:
    def __init__(self, width, height):
        self.minimum = 30 # Max sections
        self.width = width
        self.height = height
        self.leaves = []
        self.dungeon = []
        self.rooms = []
        self.level = []

        # Fill Dungeon with void to be filled up later
        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(Dungeon(0))
            self.dungeon.append(row)

    def split_horizontal(self, min_row, min_col, max_row, max_col):
        split = (min_row + max_row) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, split, max_col)
        self.random_split(split + 1, min_col, max_row, max_col)

    def split_vertical(self, min_row, min_col, max_row, max_col):
        split = (min_col + max_col) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, max_row, split)
        self.random_split(min_row, split + 1, max_row, max_col)

    def random_split(self, min_row, min_col, max_row, max_col):
        # Keep splitting until it reaches the minimum leaf size
        seg_height = max_row - min_row
        seg_width = max_col - min_col

        if seg_height < self.minimum and seg_width < self.minimum:
            self.leaves.append((min_row, min_col, max_row, max_col))
        # Split leaf specifically if it is too rectangle-ish (not square enough)
        elif seg_height < self.minimum and seg_width >= self.minimum:
            self.split_vertical(min_row, min_col, max_row, max_col)
        elif seg_height >= self.minimum and seg_width < self.minimum:
            self.split_horizontal(min_row, min_col, max_row, max_col)
        else:
            # Otherwise split randomly
            if random() < 0.5:
                self.split_horizontal(min_row, min_col, max_row, max_col)
            else:
                self.split_vertical(min_row, min_col, max_row, max_col)

    def create_rooms(self):
        for leaf in self.leaves:
            if random() > 0.80: continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            room_width = round(randrange(75, 76) / 100 * section_width)
            room_height = round(randrange(65, 66) / 100 * section_height)

            if section_height > room_height:
                room_start_row = leaf[0] + randrange(section_height - room_height)
            else:
                room_start_row = leaf[0]

            if section_width > room_width:
                room_start_col = leaf[1] + randrange(section_width - room_width)
            else:
                room_start_col = leaf[1]
            self.rooms.append(Room(room_start_row, room_start_col, room_height, room_width))
            for r in range(room_start_row, room_start_row + room_height):
                for c in range(room_start_col, room_start_col + room_width):
                    self.dungeon[r][c] = Dungeon(1)

    def adjacent_rooms(self, room1, room2):
        # Which rooms are adjacent to each other
        adj_rows = []
        adj_cols = []

        for r in range(room1.row, room1.row + room1.height):
            if r >= room2.row and r < room2.row + room2.height:
                adj_rows.append(r)
        for c in range(room1.col, room1.col + room1.width):
            if c >= room2.col and c < room2.col + room2.width:
                adj_cols.append(c)

        return (adj_rows, adj_cols)

    def distance(self, room1, room2):
        # The distance between the adjacent rooms
        center1 = (room1.row + room1.height // 2, room1.col + room1.width // 2)
        center2 = (room2.row + room2.height // 2, room2.col + room2.width // 2)

        return sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)

    def create_corridors(self, room1, room2):
        if room2[2] == 'rows':
            try:
                rowtemp = randint(3, len(room2[1]) - 3) # Make corridors more in the middle
                row = room2[1][rowtemp]
            except Exception:
                rowtemp = randint(2, len(room2[1]) - 2)
                row = room2[1][rowtemp]
            except Exception:
                row = choice(room2[1])

            # Figure out which room is to the left of the other
            if room1.col + room1.width < room2[0].col:
                start_col = room1.col + room1.width
                end_col = room2[0].col
            else:
                start_col = room2[0].col + room2[0].width
                end_col = room1.col
            # Carve space in corridor
            for u in range(row-1, row+2): # This for loop makes the corridor bigger
                for c in range(start_col, end_col):
                    self.dungeon[u][c] = Dungeon(1)
                    self.dungeon[row-1][c] = Dungeon(2) # Add walls in corridors
                    self.dungeon[row+1][c] = Dungeon(2)

            # Create Doors
            if end_col - start_col >= 2:
                self.dungeon[row][start_col] = Dungeon(4)
                self.dungeon[row][end_col - 1] = Dungeon(4)
            elif start_col == end_col - 1:
                self.dungeon[row][start_col] = Dungeon(4)

        else:
            try:
                coltemp = randint(3, len(room2[1]) - 3) # Make corridors more in the middle
                col = room2[1][coltemp]
            except Exception:
                coltemp = randint(2, len(room2[1]) - 2)
                col = room2[1][coltemp]
            except Exception:
                col = choice(room2[1])

            # Figure out which room is above the other
            if room1.row + room1.height < room2[0].row:
                start_row = room1.row + room1.height
                end_row = room2[0].row
            else:
                start_row = room2[0].row + room2[0].height
                end_row = room1.row
            # Carve space in corridor
            for u in range(col-1, col+2):
                for r in range(start_row, end_row):
                    self.dungeon[r][col] = Dungeon(1)
                    self.dungeon[r][col-1] = Dungeon(3) # Add walls in corridors
                    self.dungeon[r][col+1] = Dungeon(3)

            # Create Doors
            if end_row - start_row >= 2:
                self.dungeon[start_row][col] = Dungeon(4)
                self.dungeon[end_row - 1][col] = Dungeon(4)
            elif start_row == end_row - 1:
                self.dungeon[start_row][col] = Dungeon(4)

    def connect_groups(self, groups, room_dict):
        # Find two nearby rooms that are in different groups
        # Carve corridor between them to merge them
        shortest_distance = 99999
        start = None
        start_group = None
        nearest = None

        for group in groups:
            for room in group:
                key = (room.row, room.col)
                for other in room_dict[key]:
                    if not other[0] in group and other[3] < shortest_distance:
                        shortest_distance = other[3]
                        start = room
                        nearest = other
                        start_group = group

        self.create_corridors(start, nearest)

        # Merge the groups
        other_group = None
        for group in groups:
            if nearest[0] in group:
                other_group = group
                break

        start_group += other_group
        groups.remove(other_group)

    def connect_rooms(self):
        groups = []
        room_dict = {}
        for room in self.rooms:
            key = (room.row, room.col)
            room_dict[key] = []
            for other in self.rooms:
                other_key = (other.row, other.col)
                if key == other_key: continue
                adj = self.adjacent_rooms(room, other)
                if len(adj[0]) > 0:
                    room_dict[key].append((other, adj[0], 'rows', self.distance(room, other)))
                elif len(adj[1]) > 0:
                    room_dict[key].append((other, adj[1], 'cols', self.distance(room, other)))

            groups.append([room])
        while len(groups) > 1:
            self.connect_groups(groups, room_dict)

    def generate_map(self):
        # Run functions
        self.random_split(1, 1, self.height - 1, self.width - 1)
        self.create_rooms()
        self.connect_rooms()

        # Create a 2D array of the level
        for r in range(self.height):
            self.row = []
            for c in range(self.width):
                self.row.append(self.dungeon[r][c].get_map())
            self.level.append(self.row)

        # Spawn things in the center of rooms
        # 0 - Void | 1 - Floor | 2 - Horizontal Wall | 3 - Vertical Wall | 4 - Door
        # 8 - Player Spawn
        # 9 - End Portal
        self.level[self.rooms[0].row + self.rooms[0].height//2 ][self.rooms[0].col + self.rooms[0].width//2] = 8
        self.level[self.rooms[-1].row + self.rooms[-1].height//2 ][self.rooms[-1].col + self.rooms[-1].width//2] = 9

        # Add walls to all rooms
        # Add if the map is filled with void instead of walls
        for u in range(len(self.rooms)):
            # Add vertical walls on the left and right outside of the room
            for i in range(self.rooms[u].row-1, self.rooms[u].row + self.rooms[u].height):
                # Do not put wall if there is a door
                if self.level[i][self.rooms[u].col-1] != 4:
                    self.level[i][self.rooms[u].col-1] = 3
                if self.level[i][self.rooms[u].col+self.rooms[u].width] != 4:
                    self.level[i][self.rooms[u].col+self.rooms[u].width] = 3
            # Add horizontal walls on the top and bottom outside of the room
            for v in range(self.rooms[u].col, self.rooms[u].col + self.rooms[u].width):
                # If different walls are used for horizontal and vertical to make it more 3D
                # The corner walls must be changed to make it visual accurate
                if self.level[self.rooms[u].row-1][v] != 4:
                    self.level[self.rooms[u].row-1][v] = 2
            for m in range(self.rooms[u].col-1, self.rooms[u].col + self.rooms[u].width+1):
                # Do not put wall if there is a door
                if self.level[self.rooms[u].row+self.rooms[u].height][m] != 4:
                    self.level[self.rooms[u].row+self.rooms[u].height][m] = 2

        # Final edit in the map to avoid being overridden by other loops
        for r in range(MAPHEIGHT):
            for c in range(MAPWIDTH):
                # Walls must be changed if using different horizontal and vertical walls image
                if self.level[r][c] == 4:
                    # If it is a horizontal corridor
                    if self.level[r][c-1] == 1 or self.level[r][c+1] == 1:
                        self.level[r-1][c] = 2
                    # If it is a vertical corridor
                    elif self.level[r+1][c+1] == 2 or self.level[r+1][c+1] == 3:
                        self.level[r][c-1] = 3
                        self.level[r][c+1] = 3


        # Reshape and iterate the array as a string on a file to be read
        with open(path.join(dir1, 'GeneratedMap.txt'), 'w') as f:
            for i in range(MAPHEIGHT):
                for u in range(MAPWIDTH):
                    if u % MAPWIDTH == 0:
                        f.write("\n")
                    f.write(str(self.level[i][u]))

dungeon = DungeonGenerator(MAPWIDTH, MAPHEIGHT)
dungeon.generate_map()
