import pygame
import os
from laser import Laser


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, level=1):
        super().__init__()
        if level == 1:
            self.display_width = pygame.display.get_surface().get_width()
            self.image_path = os.path.join(os.path.abspath(__file__),
                                           "../../assets/red_enemy.png")
        """if level == 2:
            self.image_path = os.path.join(os.path.abspath(__file__),
                                           "../../assets/blue_enemy_ship.png")
        if level == 3:
            self.image_path = os.path.join(os.path.abspath(__file__),
                                           "../../assets/red_grey_ship.gif")"""

        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        if pos[0] + self.image.get_width() >= self.display_width:
            pos = [0, pos[1]]
            pos[0] = self.display_width - self.image.get_width()
        self.rect = self.image.get_rect(topleft=pos)

        self.countdown = 300

    def move(self):
        self.rect.y += 1

    def shoot(self, lasers):
        if self.countdown == 0 and self.rect.top > 0:  # Avoid enemies shooting before entering screen
            lasers.add(Laser(self.rect.midbottom, "enemy"))
            self.countdown = 300

        if self.countdown > 0:
            self.countdown -= 1

    def laser_hit(self, lasers):
        for laser in lasers.sprites():
            if pygame.sprite.collide_mask(self, laser) and laser.team == "player":
                self.kill()
                laser.kill()

    def destroy(self, enemies):  # Avoid having enemies spawn on top of each other
        for enemy in enemies.sprites():
            if enemy is self:
                pass
            elif pygame.sprite.collide_mask(self, enemy):
                enemy.kill()

    def update(self, lasers, enemies):
        self.move()
        self.shoot(lasers)
        self.laser_hit(lasers)
        self.destroy(enemies)
