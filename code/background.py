import pygame
import random


class Background(pygame.sprite.Sprite):
    def __init__(self, moment=""):
        super().__init__()
        self.display = pygame.display.get_surface()

        if moment == "beginning":
            self.y_range_max = self.display.get_height()
        else:
            self.y_range_max = 0

        self.pos = (random.randrange(0, self.display.get_width()),
                    random.randrange(-10, self.y_range_max))
        self.rad = random.randrange(1, 3)

        self.speed = random.randrange(1, 6) * 0.1

    def update(self):
        self.pos = (self.pos[0], self.pos[1] + self.speed)
        if self.pos[1] <= self.display.get_height():
            pygame.draw.circle(self.display, "white", self.pos, self.rad)
