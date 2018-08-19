from Load import *
from GeneratorBSP import *
from random import randint
import math

class Goblin(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target): #weapon too
        self.game = game
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((TILESIZE - int(TILESIZE/2), TILESIZE - int(TILESIZE/2)))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.target = target
        #self.x = x
        #self.y = y
        #self.rect.x = x * TILESIZE
        #self.rect.y = y * TILESIZE

        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = 30

    def stuff(self):
            # self.speedx, self.speedy = 1, 1
            # self.vx, self.vy = 0, 0
            # self.movetime = 100
            # self.attacktime = 0

            # Find the center of their original room
            # This will be used to find the radius it wanders in (to prevent ai from moving into corners)
            for u in range(len(dungeon.rooms)):
                if y > dungeon.rooms[u].row and y < dungeon.rooms[u].row + dungeon.rooms[u].height:
                    if x > dungeon.rooms[u].col and y < dungeon.rooms[u].col + dungeon.rooms[u].width:
                        self.spawnx = (dungeon.rooms[u].col + dungeon.rooms[u].width//2) * TILESIZE
                        self.spawny = (dungeon.rooms[u].row + dungeon.rooms[u].height//2) * TILESIZE
                        self.spawnw = (dungeon.rooms[u].width - dungeon.rooms[u].width/1.9) * TILESIZE
                        self.spawnh = (dungeon.rooms[u].height - dungeon.rooms[u].height/1.9) * TILESIZE
    def move(self):
        # If close to player, chase him
        if math.hypot(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y) < 300:
            self.attack()
            if self.rect.x < self.target.rect.x:
                self.vx = self.speedx
            elif self.rect.x > self.target.rect.x:
                self.vx = -self.speedx
            elif self.rect.x == self.target.rect.x:
                self.vx = 0 # to prevent wobbling

            if self.rect.y < self.target.rect.y:
                self.vy = self.speedy
            elif self.rect.y > self.target.rect.y:
                self.vy = -self.speedy
            elif self.rect.y == self.target.rect.y:
                self.vy = 0 # to prevent wobbling

        # If not chasing and in moving radius (slightly smaller than the room), move randomly
        elif math.hypot(self.spawnx - self.rect.x, self.spawny - self.rect.y) < min(self.spawnw, self.spawnh):
            rand_move = randint(1,5)
            self.movetime += 1
            if self.movetime > 100:
                self.movetime = 0
                if rand_move == 1:
                    self.vx = self.speedx
                if rand_move == 2:
                    self.vx = -self.speedx
                if rand_move == 3:
                    self.vy = self.speedy
                if rand_move == 4:
                    self.vy = -self.speedy
                if rand_move == 5:
                    self.vx, self.vy = 0, 0

        # If not chasing and out of spawn radius, go back near spawn
        else:
            if self.rect.x < self.spawnx:
                self.vx = self.speedx
            elif self.rect.x > self.spawnx:
                self.vx = -self.speedx
            elif self.rect.x == self.spawnx:
                self.vx = 0 # to prevent wobbling

            if self.rect.y < self.spawny:
                self.vy = self.speedy
            elif self.rect.y > self.spawny:
                self.vy = -self.speedy
            elif self.rect.y == self.spawny:
                self.vy = 0 # to prevent wobbling

    def attack(self):
        self.attacktime += 1
        if self.attacktime > 50:
            self.attacktime = 0
            bullet = EnemyBullets(self.game, self.rect.center[0], self.rect.center[1], self.target)

    def wallcollision(self):
        hits = pygame.sprite.groupcollide(self.game.mobs, self.game.walls, False, False)
        if hits:
            if self.vx > 0:
                self.x = hits[0].rect.left - self.rect.width
            if self.vx < 0:
                self.x = hits[0].rect.right
            self.vx = 0
            self.rect.x = self.x

            if self.vy > 0:
                self.y = hits[0].rect.top - self.rect.height
            if self.vy < 0:
                self.y = hits[0].rect.bottom
            self.vy = 0
            self.rect.y = self.y

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < TILESIZE*2:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.target.rect.center - self.pos).angle_to(vec(1, 0))
        #self.image = pygame.transform.rotate(pygame.Surface((TILESIZE - int(TILESIZE/2), TILESIZE - int(TILESIZE/2))), self.rot)
        #self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * 0.06
        self.pos += self.vel * 0.06 + 0.5 * self.acc * 0.06 ** 2
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.wallcollision()
        print(self.rect.center, self.target.rect.center)


        # self.move()
        # self.rect.x += self.vx
        # self.rect.y += self.vy
        # self.collision()

class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target):
        self.game = game
        self.groups = game.all_sprites, game.enemybullets
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((5,5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.posx = self.rect.x
        self.posy = self.rect.y
        self.changex = 0
        self.changey = 0
        self.dx = target.rect.x - self.rect.x # X-Distance
        self.dy = target.rect.y - self.rect.y # Y-Distance
        self.dist = math.sqrt(self.dx ** 2 + self.dy ** 2) # Total Distance between Enemy and Player
        self.dx = (self.dx / self.dist) * 10
        self.dy = (self.dy / self.dist) * 10
        self.changex += self.dx
        self.changey += self.dy

        self.lifespan = 0

    def update(self):
        self.posx += self.changex
        self.posy += self.changey
        self.rect.x = self.posx
        self.rect.y = self.posy

        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if self.lifespan > 50:
            self.kill()
        self.lifespan += 1
