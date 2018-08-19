from Load import *
from GeneratorMap import *
import math, random

def hitbox(one, two):
    return one.hitbox.colliderect(two.rect)

def collision(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, hitbox)
        if hits:
            if hits[0].rect.centerx > sprite.hitbox.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hitbox.width / 2
            if hits[0].rect.centerx < sprite.hitbox.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hitbox.width / 2
            sprite.vel.x = 0
            sprite.hitbox.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, hitbox)
        if hits:
            if hits[0].rect.centery > sprite.hitbox.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hitbox.height / 2
            if hits[0].rect.centery < sprite.hitbox.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hitbox.height / 2
            sprite.vel.y = 0
            sprite.hitbox.centery = sprite.pos.y


class MeleeMob(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target):
        self.game = game
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((30,30))
        self.rect = self.image.get_rect()
        self.target = target

        self.hitbox = pygame.Rect(0, 0, 30, 30)
        self.hitbox.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = 300

        self.combat = random.choice([True, False])
        self.attackcounter = 0
        self.movecounter = 999999999

        # Mob's native room variables
        for u in range(len(dungeon.rooms)):
            if y > dungeon.rooms[u].row and y < dungeon.rooms[u].row + dungeon.rooms[u].height:
                if x > dungeon.rooms[u].col and x < dungeon.rooms[u].col + dungeon.rooms[u].width:
                    self.spawnx = dungeon.rooms[u].col * TILESIZE
                    self.spawny = dungeon.rooms[u].row * TILESIZE
                    self.spawncenterx = (dungeon.rooms[u].col + dungeon.rooms[u].width//2) * TILESIZE
                    self.spawncentery = (dungeon.rooms[u].row + dungeon.rooms[u].height//2) * TILESIZE
                    self.spawnw = dungeon.rooms[u].width * TILESIZE
                    self.spawnh = dungeon.rooms[u].height * TILESIZE
        self.rand_pointx = self.spawncenterx # default goto positions
        self.rand_pointy = self.spawncentery

    def avoid_mobs(self):
        # Tries not to collide with other mobs
        # Does not turn into 1 mob and will try to surround player
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                print(dist)
                if 0 < dist.length() < 50:
                    self.acc += dist.normalize()

    def move(self):
        # If in combat mode, chase player!
        if self.combat:
            self.speed = random.randint(2000, 3000)
            self.rot = (self.target.rect.center - self.pos).angle_to(vec(1, 0))

            # If in close-range, ATTACK!
            if pygame.sprite.spritecollide(self.game.player, self.game.mobs, False):
                print("ATTACK")
                self.combat = False

        # If passive, wander around and wait until ready for combat
        if not self.combat:
            # Waiting to be combat ready
            self.attackcounter += random.randint(0,3)
            if self.attackcounter > random.randint(350, 450):
                self.attackcounter = 0
                self.combat = True

            # Wandering around
            self.speed = random.randint(600, 800)
            self.movecounter += random.randint(0,3)
            if self.movecounter > random.randint(100, 200):
                # move to another point in the room
                self.movecounter = 0
                self.rand_pointx = random.randrange(int(self.spawnx + TILESIZE), int(self.spawnx + self.spawnw - TILESIZE))
                self.rand_pointy = random.randrange(int(self.spawny + TILESIZE), int(self.spawny + self.spawnh - TILESIZE))
            self.rot = ((self.rand_pointx, self.rand_pointy) - self.pos).angle_to(vec(1, 0))

        # Move to a point specified in the if statements above
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot) # if its vec(1,1) it circles around
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -3 # Friction
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hitbox.centerx = self.pos.x
        collision(self, self.game.walls, 'x')
        self.hitbox.centery = self.pos.y
        collision(self, self.game.walls, 'y')
        self.rect.center = self.hitbox.center

    def update(self):
        self.move()

class ShooterMob(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target):
        self.game = game
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((30,30))
        self.rect = self.image.get_rect()
        self.target = target

        self.hitbox = pygame.Rect(0, 0, 30, 30)
        self.hitbox.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = 100
        self.movetime = random.randint(100, 200)
        self.movecounter = 600
        self.attackcounter = 600

        # Mob's native room variables
        for u in range(len(dungeon.rooms)):
            if y > dungeon.rooms[u].row and y < dungeon.rooms[u].row + dungeon.rooms[u].height:
                if x > dungeon.rooms[u].col and x < dungeon.rooms[u].col + dungeon.rooms[u].width:
                    self.spawnx = dungeon.rooms[u].col * TILESIZE
                    self.spawny = dungeon.rooms[u].row * TILESIZE
                    self.spawncenterx = (dungeon.rooms[u].col + dungeon.rooms[u].width//2) * TILESIZE
                    self.spawncentery = (dungeon.rooms[u].row + dungeon.rooms[u].height//2) * TILESIZE
                    self.spawnw = dungeon.rooms[u].width * TILESIZE
                    self.spawnh = dungeon.rooms[u].height * TILESIZE
        self.rand_pointx = self.spawncenterx # default goto positions
        self.rand_pointy = self.spawncentery

    def avoid_mobs(self):
        # Tries not to collide with other mobs
        # Does not turn into 1 mob and will try to surround player
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                print(dist)
                if 0 < dist.length() < 50:
                    self.acc += dist.normalize()

    def move(self):
        self.attack()
        # If not close to player, move randomly and attack
        if math.hypot(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y) > 200:
            self.speed = 300
            self.movecounter += random.randint(0,3)
            if self.movecounter > random.randint(100, 200):
                # move to another point in the room
                self.movecounter = 0
                self.rand_pointx = random.randrange(int(self.spawnx + TILESIZE), int(self.spawnx + self.spawnw - TILESIZE))
                self.rand_pointy = random.randrange(int(self.spawny + TILESIZE), int(self.spawny + self.spawnh - TILESIZE))
            self.rot = ((self.rand_pointx, self.rand_pointy) - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.acc.scale_to_length(self.speed)

        # If close to player, move in the opposite direction
        elif math.hypot(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y) <= 200:
            self.speed = 700
            self.rot = (self.target.rect.center - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.acc.scale_to_length(-self.speed) # move in opposite direction

        self.acc += self.vel * -1 # Friction
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hitbox.centerx = self.pos.x
        collision(self, self.game.walls, 'x')
        self.hitbox.centery = self.pos.y
        collision(self, self.game.walls, 'y')
        self.rect.center = self.hitbox.center

    def attack(self):
        self.attackcounter += 1
        if self.attackcounter > 100:
            self.attackcounter = 0
            bullet = MobBullet(self.game, self, self.target)

    def update(self):
        self.move()

class MobBullet(pygame.sprite.Sprite):
    def __init__(self, game, user, target):
        self.game = game
        self.user = user
        self.target = target
        self.groups = game.all_sprites, game.mobbullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.weapon_img.copy()
        self.rect = self.image.get_rect()

        self.hitbox = pygame.Rect(0, 0, 30, 30)
        self.hitbox.center = self.rect.center
        self.pos = vec(user.pos.x, user.pos.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = 500

        self.rot = (self.target.rect.center - self.user.pos).angle_to(vec(1, 0))

    def update(self):
        self.image = pygame.transform.rotate(self.game.weapon_img, self.rot)
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1 # Friction
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
