import pygame
import random
import os
from laser import Laser


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, level=1):
        super().__init__()

        ### To display different enemy ships accordimg to the level
        if level == 1:
            self.display_width = pygame.display.get_surface().get_width()
            directory = os.path.dirname(os.path.abspath(__file__))
            self.image_path = os.path.join(directory,
                                           "../assets/red_enemy.png")
        """if level == 2:
            self.image_path = os.path.join(os.path.abspath(__file__),
                                           "../../assets/blue_enemy_ship.png")
        if level == 3:
            self.image_path = os.path.join(os.path.abspath(__file__),
                                           "../../assets/red_grey_ship.gif")"""
        
        # Loading and masking the image
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        # Checking the enemy ship remains in the screen area
        if pos[0] + self.image.get_width() >= self.display_width:
            pos = [0, pos[1]]
            pos[0] = self.display_width - self.image.get_width()
        self.rect = self.image.get_rect(topleft=pos)

        self.countdown = 200

    def move(self):
        self.rect.y += 1

    def shoot(self, lasers):
        if self.countdown == 0:
            lasers.add(Laser(self.rect.midbottom, "enemy"))
            self.countdown = 200

        if self.countdown > 0:
            self.countdown -= 1

    def laser_hit(self, lasers):
        for laser in lasers.sprites():
            if pygame.sprite.collide_mask(self, laser) and laser.team == "player":
                self.kill()
                laser.kill()

    def update(self, lasers):
        self.move()
        self.laser_hit(lasers)
