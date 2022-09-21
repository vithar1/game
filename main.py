import pygame
import sys
import random

'''
    add a miner
    the structure of this project more wrong than i think.
    You need to separate logic of game and sprites. 
    Class with sprite has to placed separated from class for game logic.
'''


YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 1080
HEIGHT = 700
FPS = 60


class Spritesheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, scale = None, colorkey = None):
        'Loads image from x,y,x+offset,y+offset'
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        # error this. All black elements on sprite will be invision
        image.set_colorkey((0,0,0))
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        if scale is None:
            return image
        return pygame.transform.scale(image, scale)

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, scale = None, colorkey = None):
        'Loads multiple images, supply a list of coordinates' 
        return [self.image_at(rect, scale, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, scale = None, colorkey = None):
        'Loads a strip of images and returns them as a list'
        tups = [(rect[0], rect[1]+rect[3]*i, rect[2], rect[3])
                for i in range(image_count)]
        return self.images_at(tups, scale, colorkey)


class SpriteStripAnim:
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, rect, count, scale = None, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = Spritesheet(filename)
        self.images = ss.load_strip(rect, count, scale, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames


    def iter(self):
        self.i = 0
        self.f = self.frames
        return self


    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image


    def __add__(self, ss):
        self.images.extend(ss.images)
        return self


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_vec) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.ss = Spritesheet('sprites/fire_balls/fireboll.png')
        self.image = self.ss.image_at((0,0,190, 190), (30, 30))
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


class FireBullet(pygame.sprite.Sprite):
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


class FireBoll:
    def __init__(self) -> None:
        self.delay = 0


    def shoot(self, dir, from_cords) -> list:
        if self.delay > 0:
            self.delay -= 1
            return []
        bullet = Bullet(*from_cords, dir)
        self.delay = 5
        return [bullet, ]


class Flamethrower:
    def __init__(self) -> None:
        pass


    def shoot(self, dir, from_cords) -> list:
        bullets = []
        for i in range(2):
            bullet = Bullet(*from_cords, (dir, random.uniform(0, 0.6) - 0.3))
            bullets.append(bullet)
        return bullets


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
        self.s_left_move = SpriteStripAnim('sprites/vampire3.png',
            (19, 23, 12, 24), 8, (45, 80), loop=True, frames=12).iter()
        self.s_right_move = SpriteStripAnim('sprites/vampire3.png',
            (19, 23, 12, 24), 8, (45, 80), loop=True, frames=12).iter()
        self.s_up_move = SpriteStripAnim('sprites/vampire3.png',
            (19, 23, 12, 24), 8, (45, 80), loop=True, frames=12).iter()
        self.s_down_move = SpriteStripAnim('sprites/vampire3.png',
            (19, 23, 12, 24), 8, (45, 80), loop=True, frames=12).iter()
        self.image = self.s_left_move.next()
        self.bullets = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.attack = 10
        self.total_health = random.randint(1, 10)
        self.health = self.total_health
        self.vec = (-1,0) 
        self.speed = 0
        self.rect.x = random.randint(100, WIDTH) 
        self.rect.y = random.randint(100, HEIGHT) 
        self.health_bar = HealthBar(self.rect.x, self.rect.y - 30)
        self.move_time = 0
        self.sc = 0
    

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
            self.vec = (self.vec[0]*-1, self.vec[1])
            self.speed = random.randrange(1, 3)
    

    def shoot(self, all_sprites):
        if random.randint(0, 60) == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, (-1,0))
            all_sprites.add(bullet)
            self.bullets.add(bullet)


class Person(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.s_left_move = SpriteStripAnim('sprites/vampire3.png',
            (19, 23, 12, 24), 4, (45, 80), loop=True, frames=10).iter()
        self.s_down_move = SpriteStripAnim('sprites/vampire3.png',
            (33, 23, 15, 24), 4, (45, 80), loop=True, frames=10).iter()
        self.s_right_move = SpriteStripAnim('sprites/vampire3.png',
            (49, 23, 12, 24), 4, (45, 80), loop=True, frames=10).iter()
        self.s_up_move = SpriteStripAnim('sprites/vampire3.png',
            (64, 23, 15, 24), 4, (45, 80), loop=True, frames=10).iter()
        self.image = self.s_down_move.next()
        self.bullets = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.attack = 10
        self.health = 100
        self.vec = (0,0) 
        self.speed = 0
        self.rect.x = 0
        self.rect.y = 0
        self.delay = 0
        self.weapon = FireBoll()
        self.dir = (0,1)
        # self.weapon = Flamethrower()

    
    def update(self):
        if self.vec[0] > 0.5:
            self.image = self.s_right_move.next()
        if self.vec[0] < -0.5:
            self.image = self.s_left_move.next()
        if self.vec[1] > 0.5:
            self.image = self.s_down_move.next()
        if self.vec[1] < -0.5:
            self.image = self.s_up_move.next()
        if 0 < self.rect.x + self.vec[0] * self.speed < WIDTH:
            self.rect.x += self.vec[0] * self.speed
        if 0 < self.rect.y + self.vec[1] * self.speed < HEIGHT:
            self.rect.y += self.vec[1] * self.speed
        if self.vec != (0,0):
            self.dir = self.vec

    
    def shoot(self, all_sprites):
        for bullet in self.weapon.shoot(self.dir, (self.rect.centerx, self.rect.centery)):
            all_sprites.add(bullet)
            self.bullets.add(bullet)


class FlorePeace(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.ss = Spritesheet('sprites/Texture/stone.png')
        self.image = self.ss.image_at((0,0,96, 96))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    
    def update(self):
        pass


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH+40, HEIGHT+40))
        pygame.display.set_caption('vithar')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        for i in range(int(HEIGHT/96)+1):
            for j in range(int(WIDTH/96)+1):
                self.all_sprites.add(FlorePeace((j*96,i*96)))
        self.person = Person()
        self.person.speed = 3
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
        if keys[pygame.K_SPACE]:
            self.person.shoot(self.all_sprites)
    

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
            # self.screen.fill((30, 30, 30))
            self.all_sprites.draw(self.screen)
            self._set_score(self.score_count)
            pygame.display.flip()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
