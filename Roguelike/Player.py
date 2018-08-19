from Load import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 64, 64)
        self.hitbox.center = self.rect.center

        self.vx, self.vy = 0, 0
        self.speed = 300
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.attackcounter = 0
        self.attackpress = False

    def collision(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def controls(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vx = -self.speed
        if keys[pygame.K_d]:
            self.vx = self.speed
        if keys[pygame.K_w]:
            self.vy = -self.speed
        if keys[pygame.K_s]:
            self.vy = self.speed

    def attack(self):
        # Add camera coorindates with mouse coordinates to get map coordinates for mouse
        (self.mx, self.my) = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        (self.mx, self.my) = ((self.rect.x - (WIDTH / 2)) + self.mx, (self.rect.y - (HEIGHT / 2)) + self.my)
        self.attackcounter += 1
        if self.attackcounter > 10 and self.attackpress:
            self.attackcounter = 0
            bullet = Bullet(self.game, self, self.mx, self.my)



    def update(self):
        self.attack()
        self.controls()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collision('x')
        self.rect.y = self.y
        self.collision('y')

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, user, x, y):
        self.game = game
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.weapon_img.copy()
        self.rect = self.image.get_rect()

        self.rect.x = user.rect.center[0]
        self.rect.y = user.rect.center[1]

        self.posx = self.rect.center[0]
        self.posy = self.rect.center[1]
        self.changex = 0
        self.changey = 0
        self.dx = x - self.rect.center[0] # X-Distance
        self.dy = y - self.rect.center[1] # Y-Distance
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

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)
