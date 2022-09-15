import pygame
import sys


YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WIDTH = 1080
HEIGHT = 700
FPS = 60



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
        if self.rect.x > 1000:
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

    
    def update(self):
        self.rect.x += self.vec[0] * self.speed
        self.rect.y += self.vec[1] * self.speed

    
    def shoot(self, all_sprites):
        bullet = Bullet(self.rect.centerx, self.rect.top, (1,0))
        all_sprites.add(bullet)
        self.bullets.add(bullet)
    

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
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
