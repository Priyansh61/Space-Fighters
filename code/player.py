import pygame
import os
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, health=100, speed=10):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.image_path = os.path.join(os.path.abspath(__file__),
                                       "../../assets/player_ship.png")
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = (self.display.get_width() / 2, 0.75 * self.display.get_height())
        self.rect = self.image.get_rect(center=self.pos)

        self.max_health = health
        self.health = health
        self.speed = speed

        self.countdown = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.display.get_width():
            self.rect.right = self.display.get_width()
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.display.get_height():
            self.rect.bottom = self.display.get_height()

    def health_bar(self):
        pos = (self.rect.x, self.rect.y + self.image.get_height() + 10)
        pygame.draw.rect(self.display, "red", (pos, (self.image.get_width(), 10)))

        relative_health = self.health / self.max_health
        pygame.draw.rect(self.display, "green",
                         (pos, (self.image.get_width() * relative_health, 10)))

    def shoot(self, lasers):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.countdown == 0:
            lasers.add(Laser((self.rect.centerx, self.rect.top - 10)))
            self.countdown = 40

        if self.countdown > 0:
            self.countdown -= 1

    def laser_hit(self, lasers):
        for laser in lasers.sprites():
            if pygame.sprite.collide_mask(self, laser):
                self.health -= 25
                laser.kill()

    def update(self, lasers):
        self.move()
        self.health_bar()
        self.shoot(lasers)
        self.laser_hit(lasers)

    def reset(self):
        self.rect.center = self.pos
        self.health = self.max_health
