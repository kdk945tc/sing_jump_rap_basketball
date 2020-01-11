import pygame as pg
from settings import *
from characters import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.mixer.music.load("sound/bg.mp3")
        pg.mixer.music.set_volume(0.2)
        self.jumpSound = pg.mixer.Sound("sound/jump.wav")
        self.hitSound = pg.mixer.Sound("sound/hit.wav")
        self.fallSound = pg.mixer.Sound("sound/fall.wav")

        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.font = pg.font.Font("font.ttf", 50)
        self.running = True
        self.new()
        self.show_start_screen()

    def new(self):
        pg.mixer.music.play(0)
        self.sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.cxk = pg.sprite.Group()
        self.backgrounds = pg.sprite.Group()

        self.player = Player()
        self.sprites.add(self.player)
        self.cxk.add(self.player)

        self.playerBottom = PlayerBottom(self.player.get_player_rect())
        self.sprites.add(self.playerBottom)
        self.players.add(self.playerBottom)

        for i in range(2):
            b = BackGround(HEIGHT - i * (WIDTH * 2))
            self.sprites.add(b)
            self.backgrounds.add(b)

        for i in range(int(HEIGHT / 100)):
            p = Platform(random.randint(100, WIDTH - 100), i * 100, random.randint(100, 300))
            self.sprites.add(p)
            self.platforms.add(p)

        self.base = Platform(WIDTH / 2, HEIGHT - 20, WIDTH)
        self.sprites.add(self.base)
        self.platforms.add(self.base)

        self.background = BackGround()
        self.sprites.add(self.background)
        self.backgrounds.add(self.background)

        self.hits = []
        self.score = 0
        self.level = 0
        self.diffculty = 0

        self.mainLoopRunning = True

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False

    def draw_text(self, text, size, x, y, color = (180, 200, 250)):
        font = pg.font.Font("font.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.screen.fill((0,0,0))
        self.draw_text("Singing Jumping", 40, WIDTH/2, HEIGHT/4 - 50, (234, 255, 0))
        self.draw_text("Dribbler", 80, WIDTH / 2, HEIGHT / 4, (255,15,213))
        self.draw_text("Press Enter to start...", 30, WIDTH / 2, HEIGHT * 4 / 5)
        pg.display.flip()
        self.wait_for_key()

    def show_end_screen(self):
        self.screen.fill((0,0,0))
        self.draw_text("Game Over", 80, WIDTH/2, HEIGHT/4)
        self.draw_text("Press Enter to continue...", 30, WIDTH / 2, HEIGHT * 4 / 5)
        self.draw_text("Score: " + str(self.level), 30, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()

    def run(self):
        while True:
            self.events()
            if self.running:
                self.clock.tick(FPS)
                self.update()
                self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jumpUp()
                    self.jumpSound.play()
                if event.key == pg.K_p:
                    self.running = not self.running

    def update(self):
        for plat in self.platforms:
            plat.rect.y += self.diffculty
            for plat in self.platforms:
                if plat.rect.top > HEIGHT:
                    plat.kill()
        self.player.rect.y += self.diffculty

        self.playerBottom.updatePos(self.player.get_player_rect())
        hits = pg.sprite.spritecollide(self.playerBottom, self.platforms, False)
        if (- self.player.voly * self.player.jpSeq + self.player.jpSeq ** 2) > 0:
            if hits:
                self.hits = hits
                self.player.rect.bottom = self.hits[-1].rect.top
                self.player.jumpStop()
                self.hitSound.play()
        else:
            if not self.hits:
                pass
            else:
                if self.playerBottom.rect.left > self.hits[-1].rect.right or self.playerBottom.rect.right < self.hits[-1].rect.left:
                    if self.player.rect.bottom == self.hits[-1].rect.top:
                        self.player.fall()

        if self.player.rect.top < HEIGHT / 5:
            self.score -= (- self.player.voly * self.player.jpSeq + self.player.jpSeq ** 2)
            self.level = int(self.score / HEIGHT)
            if self.level <= 100:
                self.diffculty = int(self.level / 10)
            else:
                self.diffculty = 10
            self.player.rect.y -= (- self.player.voly * self.player.jpSeq + self.player.jpSeq ** 2)
            for plat in self.platforms:
                plat.rect.y -= (- self.player.voly * self.player.jpSeq + self.player.jpSeq ** 2)
                if plat.rect.top > HEIGHT:
                    plat.kill()

            for bgs in self.backgrounds:
                bgs.rect.y -= (- self.player.voly * self.player.jpSeq + self.player.jpSeq ** 2)
                if bgs.rect.top >= HEIGHT + 50:
                    g = BackGround(bgs.rect.top - WIDTH * 2)
                    self.backgrounds.add(g)
                    bgs.kill()

        if self.player.rect.top > HEIGHT:
            self.player.kill()
            self.fallSound.play()
            self.show_end_screen()
            self.new()

        while len(self.platforms) <= int(HEIGHT / 100):
            p = Platform(random.randint(100 - self.diffculty * 5, WIDTH - self.diffculty * 5),
                         - random.randint(0, 50),
                         random.randint(100 - self.diffculty * 5, 200 - self.diffculty * 10),
                         20)
            self.platforms.add(p)
            self.sprites.add(p)

        self.sprites.update()

    def draw(self):
        self.backgrounds.draw(self.screen)
        self.platforms.draw(self.screen)
        self.cxk.draw(self.screen)
        text = self.font.render("Level: " + str(self.level), True, (180, 200, 250))
        self.screen.blit(text, (10, 10))
        pg.display.update()


g = Game()
while g.mainLoopRunning:
    g.run()
pg.quit()
