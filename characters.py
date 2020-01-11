import pygame as pg
import random
from settings import *
import os

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


class PlayerBottom(pg.sprite.Sprite):
    def __init__(self, rect):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.bottom = rect.bottom
        self.image.fill((255, 255, 255, 0))

    def updatePos(self, rect):
        self.rect.x = rect.x
        self.rect.bottom = rect.bottom
        self.rect.width = rect.width
        self.rect.height = rect.height


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.imgSeq = 0
        self.jpSeq = 0
        self.stand = True
        self.walk = False
        self.walkEnd = True
        self.jump = True
        self.hit = False
        self.height = 100
        self.voly = 0
        self.image = cxkStand[self.imgSeq]
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - self.height

    def jumpUp(self):
        self.jump = True
        self.voly = 12

    def fall(self):
        self.jump = True
        self.voly = 5

    def jumpStop(self):
        self.jump = False
        self.voly = 0
        self.jpSeq = 0

    def update(self):
        speed = 0
        keystate = pg.key.get_pressed()
        # 行走状态
        if keystate[pg.K_LEFT] or keystate[pg.K_RIGHT]:
            # 判断哪个键被按下
            if keystate[pg.K_LEFT]:
                speed -= 20
            if keystate[pg.K_RIGHT]:
                speed += 20
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
        if self.rect.centerx > WIDTH + 30:
            self.rect.centerx = 0
        elif self.rect.centerx <= 0:
            self.rect.centerx = WIDTH + 30


        # 跳跃状态
        if self.jump:
            self.jpSeq += 1
            self.rect.bottom += - self.voly * self.jpSeq + self.jpSeq ** 2
            if self.jpSeq <= len(cxkJump) - 1:
                self.image = cxkJump[self.jpSeq]
            elif self.jpSeq >= len(cxkJump) - 1:
                self.image = cxkJumploop[(self.jpSeq - len(cxkJump)) % len(cxkJumploop)]
        else:
            self.rect.bottom += self.jpSeq ** 2

    def get_player_rect(self):

        new_rect = self.rect.copy()
        new_rect.width = 20
        if (- self.voly * self.jpSeq + self.jpSeq ** 2) > 0:
            new_rect.height = (- self.voly * self.jpSeq + self.jpSeq ** 2)
        else:
            new_rect.height = 10

        new_rect.centerx += 140
        new_rect.bottom += self.rect.height - new_rect.height

        return new_rect

pt = []
for i in os.listdir("img/platform"):
    m = pg.image.load("img/platform/" + i)
    pt.append(m)


class Platform(pg.sprite.Sprite):
    def __init__(self, x=WIDTH / 2, y= HEIGHT - 300, w=200, h=30):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pt[0], (w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        pass


class BasePlatform(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((800, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 20)
        self.image.fill((0, 255, 0))

    def update(self):
        pass


bg = []
for i in os.listdir("img/bg"):
    m = pg.image.load("img/bg/" + i)
    m = pg.transform.scale(m, (WIDTH, WIDTH*2))
    bg.append(m)


class BackGround(pg.sprite.Sprite):
    def __init__(self, bottom=HEIGHT):
        pg.sprite.Sprite.__init__(self)
        self.image = bg[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.left = 0
