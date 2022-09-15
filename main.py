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
        x = self.rect.x
        y = self.rect.y
        self.image = pygame.Surface((self.l, 10))
        if self.l > 35:
            self.image.fill(GREEN)
        elif self.l > 15:
            self.image.fill(YELLOW)
        else:
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
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
    

    def update(self):
        self.rect.x += self.vec[0] * self.speed
        self.rect.y += self.vec[1] * self.speed
    

    def take_damage(self, damage):
        self.health -= damage
        self.health_bar.decrease((damage * 100) / self.total_health)
        if self.health < 1:
            self.health_bar.kill()
            self.kill()
            return "kill"



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
    

    def update(self):
        self.rect.x += self.dir_vec[0] * self.speed
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
        self.rect.x += self.vec[0] * self.speed
        self.rect.y += self.vec[1] * self.speed

    
    def shoot(self, all_sprites):
        if self.delay > 0:
            self.delay -= 1
            return
        bullet = Bullet(self.rect.centerx, self.rect.top, (1,0))
        all_sprites.add(bullet)
        self.bullets.add(bullet)
        self.delay = 5


def add_mob(all_sprites, mobs):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)
    all_sprites.add(mob.health_bar)

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('vithar')
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    person = Person()
    person.speed = 5
    all_sprites.add(person)
    mobs = pygame.sprite.Group()
    for i in range(3):
        add_mob(all_sprites, mobs)
    while 1:
        clock.tick(FPS)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        person.vec = (0, 0)
        if keys[pygame.K_UP]:
            person.vec = (0, -1)
        if keys[pygame.K_DOWN]:
            person.vec = (0, 1)
        if keys[pygame.K_LEFT]:
            person.vec = (-1, 0)
        if keys[pygame.K_RIGHT]:
            person.vec  = (1, 0)
        if keys[pygame.K_SPACE]:
            person.shoot(all_sprites)
        all_sprites.update()
        hits = pygame.sprite.groupcollide(mobs, person.bullets, False, True)
        for hit in hits:
            if hit.take_damage(1) == 'kill':
                add_mob(all_sprites, mobs)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
