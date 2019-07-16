import pygame
from const import *
from pygame.locals import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#class Wall(pygame.sprite.Sprite):
#    def __init__(self, rect, x, y, *, platform = False):
#        super().__init__()
#
#        self.image = pygame.Surface(rect)
#        self.image.fill(BLUE)
#
#        self.rect = self.image.get_rect()
#        self.rect.y = y
#        self.rect.x = x
#
#        self.platform = platform

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.imgs = {
            img: {
                d: pygame.image.load(f'{img}/{d}/1.png').convert_alpha()
                for d in (FWD, BACK)
            }
            for img in (RUN, JUMP, STAND)
        }
        self.imgs[RUNNING] = {
            d: [pygame.image.load(f'run/{d}/{n}.png').convert_alpha() for n in (2,3,4)]
            for d in (FWD, BACK)
        }

        self.run_ind   = 0
        self.run_cycle = True

        self.image  = self.imgs[STAND][FWD]
        self.rect   = self.image.get_rect()
        self.rect.y = FLOOR
        self.walls  = None

        self.fwd        = FWD
        self.if_moving  = False
        self.if_falling = False
        self.if_running = False

        self.jump_tick     = 0
        self.max_jump_tick = 5

    def animate(self):

        if self.if_falling:
            self.image = self.imgs[JUMP][self.fwd]

        elif self.if_moving:

            if not self.if_running:
                self.image = self.imgs[RUN][self.fwd]
                self.if_running = True
            else:
                self.image = self.imgs[RUNNING][self.fwd][self.run_ind]

                if self.run_cycle:
                    self.run_ind += 1
                else:
                    self.run_ind -= 1

                if self.run_ind == 2 and self.run_cycle:
                    self.run_cycle = False
                elif self.run_ind == 0 and not self.run_cycle:
                    self.run_cycle = True

        else:
            self.image = self.imgs[STAND][self.fwd]
            self.if_running = False

    def move(self, key_press):
        if key_press[K_SPACE] and self.jump_tick < self.max_jump_tick:
            if not self.if_falling:
                self.rect.move_ip(0, -50)
                self.if_falling = True
            else:
                self.rect.move_ip(0, -3)
            self.jump_tick += 1

            walls_hit = pygame.sprite.spritecollide(self, self.walls, False)

            if walls_hit:
                for wall in walls_hit:
                    self.rect.top = wall.rect.bottom
        else:
            self.rect.move_ip(0, 3)
            walls_hit = pygame.sprite.spritecollide(self, self.walls, False)

            if walls_hit:
                self.if_falling = False
                for wall in walls_hit:
                    self.rect.bottom = wall.rect.top
            else:
                self.if_falling = True

        move = 3 if self.if_moving else 1

        if key_press[K_d]:
            self.rect.move_ip(move, 0)
            self.if_moving = True
            self.fwd       = FWD
        elif key_press[K_a]:
            self.rect.move_ip(-move, 0)
            self.if_moving = True
            self.fwd       = BACK
        else:
            self.if_moving = False

        walls_hit = pygame.sprite.spritecollide(self, self.walls, False)

        for wall in walls_hit:
            if self.fwd == FWD:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.y >= FLOOR:
            self.rect.y = FLOOR
            self.if_falling = False

        if not self.if_falling and not key_press[K_SPACE]:
            self.jump_tick = 0

