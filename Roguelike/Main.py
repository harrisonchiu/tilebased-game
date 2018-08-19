from Load import *
from Player import *
from Room import *
from Mobs import *
from GeneratorMap import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.map = Map(path.join(dir1, 'GeneratedMap.txt'))
        self.wallhoriz_img = pygame.image.load(path.join(imagesdir, "wallhoriz.png")).convert_alpha()
        self.wallvertic_img = pygame.image.load(path.join(imagesdir, "wallvertical.png")).convert_alpha()
        self.weapon_img = pygame.image.load(path.join(imagesdir, "weapon.png")).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.mobbullets = pygame.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile != '0' and tile != '2' and tile != '3': # FLOOR
                    Floor(self, col, row)
                if tile == '2': # HORIZONTAL WALL
                    Wall(self, col, row, 2, self.wallhoriz_img)
                if tile == '3': # VERTICAL WALL
                    Wall(self, col, row, 3, self.wallvertic_img)
                if tile == '4':
                    Door(self, col, row)
                if tile == '8':
                    self.player = Player(self, col, row)
                    self.mob = ShooterMob(self, col-3, row+3, self.player)
                    #self.mob2 = MeleeMob(self, col+2, row+3, self.player)
        self.camera = Camera(self.map.width, self.map.height)

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        # Mob bullets hit walls
        hits = pygame.sprite.groupcollide(self.walls, self.mobbullets, False, True)
        if hits:
            # Add bullet explosion
            pass


    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.floors:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.attackpress = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.attackpress = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.draw()
            self.update()

    def quit(self):
        pygame.quit()
        sys.exit()

# create the game object
g = Game()
while True:
    g.new()
    g.run()
