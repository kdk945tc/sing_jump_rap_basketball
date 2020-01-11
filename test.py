import pygame as pg
import os


WIDTH = 600
HEIGHT = 800
FPS = 30

pg.init()
clock = pg.time.Clock()
pg.display.set_caption("Test Game")
screen = pg.display.set_mode((WIDTH, HEIGHT))
sprites = pg.sprite.Group()

cxkStand = []
for i in os.listdir("img/cxk/stand"):
    m = pg.image.load("img/cxk/stand/" + i)
    m = pg.transform.scale(m, (360, 200))
    cxkStand.append(m)

cxkWalk = []
for i in os.listdir("img/cxk/walk"):
    m = pg.image.load("img/cxk/walk/" + i)
    m = pg.transform.scale(m, (360, 200))
    cxkWalk.append(m)

cxkJump = []
for i in os.listdir("img/cxk/jump"):
    m = pg.image.load("img/cxk/jump/" + i)
    m = pg.transform.scale(m, (360, 200))
    cxkJump.append(m)

cxkJumploop = []
for i in os.listdir("img/cxk/jumploop"):
    m = pg.image.load("img/cxk/jumploop/" + i)
    m = pg.transform.scale(m, (360, 200))
    cxkJumploop.append(m)


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.imgSeq = 0
        self.jpSeq = 0
        self.stand = True
        self.walk = False
        self.walkEnd = True
        self.jump = False
        self.hit = False
        self.height = 100
        self.image = cxkStand[self.imgSeq]
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - self.height

    def jumpUp(self):
        self.jump = True

    def update(self):
        speed = 0
        keystate = pg.key.get_pressed()
        # 行走状态
        if keystate[pg.K_LEFT] or keystate[pg.K_RIGHT]:
            # 判断哪个键被按下
            if keystate[pg.K_LEFT]:
                speed -= 10
            if keystate[pg.K_RIGHT]:
                speed += 10
            # 之前为行走状态
            if self.walk:
                self.imgSeq += 1
                self.imgSeq %= len(cxkWalk)
                self.image = cxkWalk[self.imgSeq]
            # 之前为站立状态
            else:
                # 之前行走已完成
                if self.walkEnd:
                    self.imgSeq = 0
                    self.walk = True
                    self.stand = False
                else:
                    self.walk = True
                    self.stand = False
                    self.imgSeq += 1
                    self.imgSeq %= len(cxkWalk)
                self.image = cxkWalk[self.imgSeq]
            # 判断是否完成动作
            if self.imgSeq >= len(cxkWalk) - 1:
                self.walkEnd = True
            else:
                self.walkEnd = False
        # 站立状态
        else:
            # 已经走完
            if self.walkEnd:
                # 之前的状态为站立
                if self.stand:
                    self.imgSeq += 1
                    self.imgSeq %= len(cxkStand)
                    self.image = cxkStand[self.imgSeq]
                # 之前的状态为行走
                else:
                    self.imgSeq = 0
                    self.image = cxkStand[self.imgSeq]
                    self.walk = False
                    self.stand = True
            # 还未走完
            else:
                # 之前的状态为站立
                if self.stand:
                    self.imgSeq += 1
                    self.imgSeq %= len(cxkWalk)
                    self.image = cxkWalk[self.imgSeq]
                    # 判断是否完成动作
                    if self.imgSeq >= len(cxkWalk) - 1:
                        self.walkEnd = True
                    else:
                        self.walkEnd = False

                # 之前的状态为行走
                else:
                    self.imgSeq += 1
                    self.imgSeq %= len(cxkWalk)
                    self.image = cxkWalk[self.imgSeq]
                    # 判断是否完成动作
                    if self.imgSeq >= len(cxkWalk) - 1:
                        self.walkEnd = True
                    else:
                        self.walkEnd = False
                    self.walk = False
                    self.stand = True
        self.rect.x += speed
        if self.rect.left > WIDTH - self.rect.width / 4:
            self.rect.right = self.rect.width / 4
        elif self.rect.right < self.rect.width / 4:
            self.rect.left = WIDTH - self.rect.width / 4
        # 跳跃状态
        if self.jump:
            self.jpSeq += 1
            self.rect.bottom = HEIGHT - self.height - (len(cxkJump) - 1) * self.jpSeq + self.jpSeq ** 2
            if self.jpSeq <= len(cxkJump) - 1:
                self.image = cxkJump[self.jpSeq]
            elif self.jpSeq >= len(cxkJump) - 1:
                self.image = cxkJumploop[(self.jpSeq - len(cxkJump)) % len(cxkJumploop)]

            if self.jpSeq == len(cxkJump) - 1:
                self.jump = False
                self.imgSeq = 0
                self.jpSeq = 0


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(w, h)
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y

    def update(self):
        pass


class Background(pg.sprite.Sprite):
    def __init__(self, y):
        pg.sprite.Sprite.__init__(self)

    def update(self):
        pass


player = Player()
sprites.add(player)

while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jumpUp()
    screen.fill((0, 0, 0))
    sprites.update()
    sprites.draw(screen)
    pg.display.update()
