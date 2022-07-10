import pygame
import os
import random
import sys
from player import Player
from enemy import Enemy
from background import Background

# ----------------------------GLOBAL VARIABLES DEFAULT--------------------------------------------#
game_active = False
game_over = False
lives = 5
start_time = 0
score = 0
highscore = 0

WIDTH, HEIGHT = 720, 670
MAX_FPS = 60


class Game:
    def __init__(self):
        # -----------------------INITIATE PYGAME AND CLOCK----------------------------------------#
        pygame.init()
        self.clock = pygame.time.Clock()

        # -------------------------SCREEN DISPLAY AND MUSIC----------------------------------------#
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Fighters")

        directory = os.path.dirname(__file__)
        background_music_path = os.path.join(directory, "../assets/bg-music.wav")
        background_music = pygame.mixer.Sound(background_music_path)
        background_music.set_volume(0.3)
        background_music.play(-1)

        # -------------------------MENU AND BACKGROUND IMAGES LOAD---------------------------------#
        menu_path = os.path.join(directory, "../assets/menu.png")
        self.menu = pygame.image.load(menu_path).convert()

        # -----------------------------------TEXT-------------------------------------------------#
        game_over_font = pygame.font.SysFont('arial', 60)
        self.lives_font = pygame.font.SysFont('arial', 40)
        self.h_score_font = pygame.font.SysFont('arial', 20)

        self.game_over_disp = game_over_font.render("BETTER LUCK NEXT TIME!!", True, "red")
        self.game_over_rect = self.game_over_disp.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        # --------------------------------SPRITE GROUPS-------------------------------------------#
        self.player = pygame.sprite.GroupSingle(Player())
        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.bg = pygame.sprite.Group()

    # ---------------------------------DEFINE FUNCTIONS-------------------------------------------#
    def collisions(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.collide_mask(self.player.sprite, enemy):
                self.player.sprite.health -= 25
                enemy.kill()

    def display_lives(self):
        global lives

        for enemy in self.enemies.sprites():
            if enemy.rect.top >= HEIGHT:
                enemy.kill()
                lives -= 1

        lives_display = self.lives_font.render(f"LIVES: {lives}", True, "white")
        self.screen.blit(lives_display, (10, 10))

    def display_score(self):
        global score, start_time

        running_time = pygame.time.get_ticks()  # Returns the time in ms since pygame.init()
        score = int(0.01 * (running_time - start_time))  # start_time is the time at game start

        score_display = self.lives_font.render(f"SCORE: {score}", True, "white")
        self.screen.blit(score_display, (WIDTH - score_display.get_width() - 10, 10))

    def run(self):
        global game_active, game_over, lives, start_time, score, highscore
        # ----------------------------------MAIN LOOP----------------------------------------------#
        while True:
            # ------------------------------EVENT LOOP---------------------------------------------#
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if game_active:
                # ------------------------DRAW BACKGROUND------------------------------------------#
                self.screen.fill("black")
                if score < 0.5:
                    for i in range(100):
                        self.bg.add(Background("beginning"))
                if not random.randrange(0, 3):
                    self.bg.add(Background())
                self.bg.update()

                # --------------------------ENEMY SPAWN--------------------------------------------#
                if random.randrange(0, 50) == 0:
                    self.enemies.add(Enemy((random.randint(0, WIDTH), random.randint(-1000, -100))))

                # ----------------------UPDATE AND DRAW SPRITES-----------------------------------#
                self.player.update(self.lasers)  # I need lasers Group inside, I pass it in
                self.player.draw(self.screen)

                self.enemies.update(self.lasers, self.enemies)  # I need lasers and enemies groups
                self.enemies.draw(self.screen)

                self.lasers.update()
                self.lasers.draw(self.screen)

                # ----------------------------FUNCTIONS CALL---------------------------------------#
                self.collisions()
                self.display_lives()
                self.display_score()

                # --------------------------CHECK FOR GAME OVER------------------------------------#
                if self.player.sprite.health <= 0 or lives <= 0:
                    game_active = False
                    lives = 5
                    self.player.sprite.reset()
                    self.enemies.empty()
                    self.lasers.empty()
                    self.bg.empty()

            else:
                # ------------------------------GAME OVER SCREEN-----------------------------------#
                if score:
                    self.screen.fill("black")
                    self.screen.blit(self.game_over_disp, self.game_over_rect)

                    score_disp = self.lives_font.render(f"YOUR SCORE: {score}", True, "red")
                    score_rect = score_disp.get_rect(center=(WIDTH / 2, HEIGHT / 3))
                    self.screen.blit(score_disp, score_rect)

                    if score > highscore:
                        highscore = score

                    h_score_disp = self.h_score_font.render(f"HIGHSCORE: {highscore}", True, "red")
                    h_score_rect = h_score_disp.get_rect(center=(WIDTH / 2, 2 / 3 * HEIGHT))
                    self.screen.blit(h_score_disp, h_score_rect)

                    # -------------------GO BACK TO MENU AFTER DELAY------------------------------#
                    if not game_over:
                        pygame.display.update()
                        pygame.time.delay(1000)
                        game_over = True
                    else:
                        if pygame.mouse.get_pressed()[0] or (
                                pygame.key.get_pressed().__contains__(True)):
                            score = 0
                            game_over = False

                # -------------------------------MENU--------------------------------------------#
                else:
                    self.screen.blit(self.menu, (0, 0))

                    if pygame.key.get_pressed()[pygame.K_p]:
                        game_active = True
                        start_time = pygame.time.get_ticks()

                    if pygame.key.get_pressed()[pygame.K_q]:
                        sys.exit()

            # -------------------------UPDATE DISPLAY AND MAX FPS--------------------------------#
            pygame.display.update()
            self.clock.tick(MAX_FPS)
