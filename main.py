from re import I
from unittest import runner
import pygame
import sys
import random


YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 1080
HEIGHT = 700
FPS = 60


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.l = 50
        self.rect.x = x 
        self.rect.y = y
    

    def decrease(self, procent):
        self.l -= int(50/100*procent)
        if self.l < 1:
            return
        self.image = pygame.Surface((self.l, 10))
        if self.l > 35:
            self.image.fill(GREEN)
        elif self.l > 15:
            self.image.fill(YELLOW)
        else:
            self.image.fill(RED)


    def follow(self, x, y):
        self.rect.x = x
        self.rect.y = y



class Mob(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(RED)
        self.bullets = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.attack = 10
        self.total_health = random.randint(1, 10)
        self.health = self.total_health
        self.vec = (0,0) 
        self.speed = 0
        self.rect.x = random.randint(100, WIDTH) 
        self.rect.y = random.randint(100, HEIGHT) 
        self.health_bar = HealthBar(self.rect.x, self.rect.y - 30)
        self.move_time = 0
    

    def update(self):
        if 0 < self.rect.x + self.vec[0] * self.speed < WIDTH:
            self.rect.x += self.vec[0] * self.speed
        if 0 < self.rect.y + self.vec[1] * self.speed < HEIGHT:
            self.rect.y += self.vec[1] * self.speed
        self.health_bar.follow(self.rect.x, self.rect.y - 30)
        
    

    def take_damage(self, damage):
        self.health -= damage
        self.health_bar.decrease((damage * 100) / self.total_health)
        if self.health < 1:
            self.health_bar.kill()
            self.kill()
            return "kill"


    def move(self):
        if self.move_time > 0:
            self.move_time -= 1
        else:
            self.move_time = random.randint(20, 40) 
            self.vec = (random.randint(-1, 1), random.randint(-1, 1))
            self.speed = random.randrange(1, 3)
    

    def shoot(self, all_sprites):
        if random.randint(0, 60) == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, (1,0))
            bullet.dir = -1
            all_sprites.add(bullet)
            self.bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_vec) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.dir_vec = dir_vec
        self.speed = 15
        self.dir = 0
    

    def update(self):
        self.rect.x += self.dir_vec[0] * self.speed * self.dir
        self.rect.y += self.dir_vec[1] * self.speed
        if self.rect.x > WIDTH:
            self.kill()


class Person(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.bullets = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.attack = 10
        self.health = 100
        self.vec = (0,0) 
        self.speed = 0
        self.rect.x = 0
        self.rect.y = 0
        self.delay = 0

    
    def update(self):
        if 0 < self.rect.x + self.vec[0] * self.speed < WIDTH:
            self.rect.x += self.vec[0] * self.speed
        if 0 < self.rect.y + self.vec[1] * self.speed < HEIGHT:
            self.rect.y += self.vec[1] * self.speed

    
    def shoot(self, all_sprites, dir):
        if self.delay > 0:
            self.delay -= 1
            return
        bullet = Bullet(self.rect.centerx, self.rect.centery, (1,0))
        bullet.dir = dir
        all_sprites.add(bullet)
        self.bullets.add(bullet)
        self.delay = 5
    

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH+40, HEIGHT+40))
        pygame.display.set_caption('vithar')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.person = Person()
        self.person.speed = 5
        self.all_sprites.add(self.person)
        self.mobs = pygame.sprite.Group()
        self.score_font = pygame.font.Font(None, 56)
        self.score_count = 0
        self.init_mobs(3)


    def init_mobs(self, number):
        for i in range(number):
            self.add_mob()


    def add_mob(self):
        mob = Mob()
        self.all_sprites.add(mob)
        self.mobs.add(mob)
        self.all_sprites.add(mob.health_bar)
    

    def _set_score(self, score):
        self.score = self.score_font.render('score: {}'.format(score), 1, (180, 180, 180))
        self.screen.blit(self.score, (0, HEIGHT-30))
    

    def _key_handle(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        self.person.vec = (0, 0)
        if keys[pygame.K_UP]:
            self.person.vec = (0, -1)
        if keys[pygame.K_DOWN]:
            self.person.vec = (0, 1)
        if keys[pygame.K_LEFT]:
            self.person.vec = (-1, 0)
        if keys[pygame.K_RIGHT]:
            self.person.vec  = (1, 0)
        if keys[pygame.K_r]:
            self.person.shoot(self.all_sprites, 1)
        if keys[pygame.K_e]:
            self.person.shoot(self.all_sprites, -1)
    

    def _collide_handler(self):
        hits = pygame.sprite.groupcollide(self.mobs, self.person.bullets, False, True)
        for hit in hits:
            if hit.take_damage(1) == 'kill':
                self.score_count += 1
                self.add_mob()
        for mob in self.mobs:
            person_hit = pygame.sprite.spritecollide(self.person, mob.bullets, True)
            if person_hit:
                self._end_game()
                break 

    
    def _end_game(self):
        end = True
        while end:
            self.screen.fill((30, 30, 30))
            f1 = pygame.font.Font(None, 86)
            text1 = f1.render('Игра окончена!', 1, (180, 180, 180))
            self.screen.blit(text1, (WIDTH/2-200, HEIGHT/2-100))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                end = False
                self.person.rect.x = 0
                self.person.rect.y = 0
                self.score_count = 0
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()


    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self._key_handle()
            for mob in self.mobs:
                mob.move()
                mob.shoot(self.all_sprites)
            self.all_sprites.update()
            self._collide_handler()
            self.screen.fill((30, 30, 30))
            self.all_sprites.draw(self.screen)
            self._set_score(self.score_count)
            pygame.display.flip()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
