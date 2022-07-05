import pygame
import os


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, team="player"):
        super().__init__()
        self.image_path = os.path.join(os.path.abspath(__file__),
                                       "../../assets/blue_laser.png")
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)

        self.team = team
        self.direction = -1
        if self.team == "enemy":
            self.direction = 1

    def move(self):
        self.rect.y += 5 * self.direction

    def destroy(self):
        if self.rect.bottom <= 0 or self.rect.top >= pygame.display.get_surface().get_height():
            self.kill()

    def update(self):
        self.move()
        self.destroy()
