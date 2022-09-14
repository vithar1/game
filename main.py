import pygame
import sys


class Person:
    def __init__(self, name:str) -> None:
        self._name = name
        self.attack = 10
        self.x = 0
        self.y = 0
    
    
    def move(self, x, y):
        self.x = x
        self.y = y

    
    @property
    def name(self):
        return self._name
    


def main():
    x = 0
    y = 0
    speed = 5
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()
    person = Person('warlok')
    count = 0
    bol_len = 1000
    bolls = []
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y -= 1 * speed
        if keys[pygame.K_DOWN]:
            y += 1 * speed
        if keys[pygame.K_LEFT]:
            x -= 1 * speed
        if keys[pygame.K_RIGHT]:
            x += 1 * speed
        if keys[pygame.K_SPACE]:
            bolls.append([x+99, y+50, bol_len])
        screen.fill((255, 255, 255))
        deleted_b_i = []
        for i in range(len(bolls)):
            if bolls[i][2] > 0:
                bolls[i][2] -= speed * 2
                pygame.draw.rect(screen, (0,0, 128), (bolls[i][0]+bol_len-bolls[i][2], bolls[i][1], 10, 5))
            else:
                deleted_b_i.append(i)
        for i in deleted_b_i:
            del bolls[i]
        pygame.draw.rect(screen, (0,0, 128), (x, y, 100, 100))
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
