import pygame
import os
import random
import sys
from player import Player
from enemy import Enemy


def collisions():
    for enemy in enemies.sprites():
        if pygame.sprite.collide_mask(player.sprite, enemy):
            player.sprite.health -= 25


def display_lives():
    global lives

    for enemy in enemies.sprites():
        if enemy.rect.top >= HEIGHT:
            enemy.kill()
            lives -= 1

    lives_font = pygame.font.SysFont('arial', 40)
    lives_display = lives_font.render(f"LIVES: {lives}", True, "white")
    screen.blit(lives_display, (10, 10))


if __name__ == "__main__":  # Only run if this file is called directly, not if it's imported

    game_active = False
    game_over = False
    lives = 5

    pygame.init()
    clock = pygame.time.Clock()
    fps = 60  # Max fps

    # Width, height of the playing window
    WIDTH, HEIGHT = 720, 670

    # Set the display of pygame:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Fighters")

    # Loading images:
    # Menu
    MENU_path = os.path.join(os.path.abspath(__file__), "../../assets/menu.png")
    MENU = pygame.image.load(MENU_path)

    # Background
    BG_1_path = os.path.join(os.path.abspath(__file__), "../../assets/space_bg.png")
    BG_1 = pygame.image.load(BG_1_path)

    # Sprite groups
    player = pygame.sprite.GroupSingle(Player())
    enemies = pygame.sprite.Group()
    lasers = pygame.sprite.Group()

    while True:  # Main loop
        for event in pygame.event.get():  # Event loop
            if event.type == pygame.QUIT:
                sys.exit()  # Check for X in window and stop program execution

        if game_active:
            screen.blit(BG_1, (0, 0))  # Blit background

            if random.randrange(0, 100) == 0:  # Create enemies randomly
                enemies.add(Enemy((random.randint(0, WIDTH), -1 * random.randint(100, 300))))

            player.update(lasers)  # I need lasers Group for some Player functions, so I pass it in
            player.draw(screen)

            enemies.update(lasers)
            enemies.draw(screen)

            lasers.update()
            lasers.draw(screen)

            collisions()
            display_lives()

            if player.sprite.health <= 0 or lives <= 0:
                game_over = True
                game_active = False
                lives = 5
                player.sprite.reset()
                enemies.empty()

        else:
            if game_over:
                screen.fill("black")
                game_over_font = pygame.font.SysFont('arial', 60)
                game_over_disp = game_over_font.render("BETTER LUCK NEXT TIME!!", True, "red")
                game_over_rect = game_over_disp.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(game_over_disp, game_over_rect)

                if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed().__contains__(True):
                    game_over = False  # Go back to menu when user clicks anywhere or presses any key

            else:
                screen.blit(MENU, (0, 0))

                if pygame.key.get_pressed()[pygame.K_p]:
                    game_active = True

                if pygame.key.get_pressed()[pygame.K_q]:
                    sys.exit()

        pygame.display.update()
        clock.tick(fps)  # Set max fps
