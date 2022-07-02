import pygame
import os
# import time
import random
import sys

# pygame.font.init()
# Instead of initialising the fonts, it's better to initialise pygame directly:
pygame.init()

# Width, height of the playing window
WIDTH, HEIGHT = 720, 670

# Set the display of pygame:
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighters")

# Loading images:
# Menu
MENU_path = os.path.join(os.path.abspath(__file__), "../assets/menu.png")
MENU = pygame.image.load(MENU_path)

# 1. Player Ships
PLAYER_SHIP_1_path = os.path.join(os.path.abspath(__file__), "../assets/player_ship.png")
PLAYER_SHIP_1 = pygame.image.load(PLAYER_SHIP_1_path)

# 2. Enemy Ships
ENEMY_SHIP_1_path = os.path.join(os.path.abspath(__file__), "../assets/red_enemy.png")
ENEMY_SHIP_1 = pygame.image.load(ENEMY_SHIP_1_path)

# 3. Lasers
BLUE_LASERS_path = os.path.join(os.path.abspath(__file__), "../assets/blue_laser.png")
BLUE_LASERS = pygame.image.load(BLUE_LASERS_path)

# 4. Background
BG_1_path = os.path.join(os.path.abspath(__file__), "../assets/space_bg.png")
BG_1 = pygame.image.load(BG_1_path)
# Setting the path like this makes sure the file is found despite where main.py
# is called from.


# Making object classes:
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y -= vel

    def off_screen(self, height):
        return self.y > height or self.y < 0

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    # Initialising object parameters:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
        self.COOLDOWN = 40
        self.cnt = 0

    # Draw for the Ship:
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # To provide an interval between lasers:
    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP_1
        self.laser_img = BLUE_LASERS
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def shoot(self):
        self.cooldown()
        if self.cooldown_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def move_laser(self, objs, vel):
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, win):
        """pygame.draw.rect(win, (255, 0, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width(), 10))

        pygame.draw.rect(win, (0, 255, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            (self.ship_img.get_width() * (
                1 - (self.max_health - self.health) / self.max_health)), 10))"""
        # Simplifying a little:
        pos = (self.x, self.y + self.get_height() + 10)
        pygame.draw.rect(win, "red", (pos, (self.ship_img.get_width(), 10)))

        relative_health = self.health / self.max_health
        pygame.draw.rect(win, "green", (pos, (self.get_width() * relative_health, 10)))


# Enemy Ship
class Enemy(Ship):
    def __init__(self, x, y, level, health=100):
        super().__init__(x, y, health)
        self.ship_img = ENEMY_SHIP_1
        self.laser_img = BLUE_LASERS
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.level = level  # Give level argument some usage

    def shoot(self):
        self.cooldown()
        if self.cooldown_counter == 0:
            """laser = Laser(self.x + self.get_width() / 2 - 5,
                          self.y + self.get_height(), self.laser_img)"""
            # Simplify it:
            laser_x = self.x + self.get_width() / 2 - 5
            laser_y = self.y + self.get_height()
            laser = Laser(laser_x, laser_y, self.laser_img)

            self.lasers.append(laser)
            self.cooldown_counter = 1

    def move(self):
        vel = 1
        self.y += vel

    def move_laser(self, obj, vel):
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


# Defining collide:
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return not (obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is None)
    # Changing return statement so that None is not compared using equality operators


# Defining movement:
def move(player):
    ship_vel = 5
    key_press = pygame.key.get_pressed()
    if (key_press[pygame.K_a] or key_press[pygame.K_LEFT]) and (
            player.x - ship_vel > 0):  # LEFT
        player.x -= ship_vel

    if (key_press[pygame.K_d] or key_press[pygame.K_RIGHT]) and (
            player.x + ship_vel + player.get_width() < WIDTH):  # RIGHT
        player.x += ship_vel

    if (key_press[pygame.K_w] or key_press[pygame.K_UP]) and (
            player.y - ship_vel > 0):  # UP
        player.y -= ship_vel

    if (key_press[pygame.K_s] or key_press[pygame.K_DOWN]) and (
            player.y + ship_vel + player.get_height() < HEIGHT):  # DOWN
        player.y += ship_vel

    if key_press[pygame.K_SPACE]:
        player.shoot()


# Defining main:
def main():
    run = True  # Checks if the user has stopped the program or not
    game_over = False
    fps = 70
    level = 0
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 40)  # Font used for lives and level
    lost_font = pygame.font.SysFont('arial', 60)

    # Object parameters:
    player = Player(WIDTH / 2, HEIGHT - 70)
    enemies = []
    num_enemies = 5

    # Draw object on the game window:
    def redraw_window():
        WIN.blit(BG_1, (0, 0))

        # Lives and Level Display
        lives_disp = main_font.render(f"LIVES: {lives}", True, (255, 255, 255))
        level_disp = main_font.render(f"LEVEL: {level}", True, (255, 255, 255))
        WIN.blit(lives_disp, (10, 10))
        WIN.blit(level_disp, (WIDTH - level_disp.get_width() - 10, 10))

        # displaying Ship
        player.draw(WIN)

        # Enemy Ship
        for enemy_ship in enemies:
            enemy_ship.draw(WIN)

        # Game Over
        if game_over:
            game_over_disp = lost_font.render("Better luck Next Time!!", True, "red")
            menu()

            # After calling menu() the rest of lines (254-256) do not run. They only run
            # if the game is quit, which gives an error because pygame is already quit.
            """WIN.blit(game_over_disp, (WIDTH / 2 - game_over_disp.get_width() / 2,
                                      HEIGHT / 2 - game_over_disp.get_height() / 2))"""
            # Simplify it:
            game_over_disp_x = (WIDTH - game_over_disp.get_width()) / 2
            game_over_disp_y = (HEIGHT - game_over_disp.get_height()) / 2
            WIN.blit(game_over_disp, game_over_disp_x, game_over_disp_y)

        pygame.display.update()

    while run:
        clock.tick(fps)

        # Checking for lives and health:
        if lives == 0 or player.health <= 0:
            game_over = True

        # Deploying enemies:
        if len(enemies) == 0:
            level += 1
            num_enemies += 5
            for i in range(num_enemies):
                enemy = Enemy(random.randrange(100, WIDTH - 200),
                              random.randrange(-1000, -100), level)
                enemies.append(enemy)

        # Moving and removing enemies:
        for enemy in enemies:
            enemy.move()
            if random.randrange(0, 2400) == 2:
                enemy.shoot()

            # If player and enemy collide:
            if collide(player, enemy):
                player.health -= 25
                enemies.remove(enemy)
            enemy.move_laser(player, -2)

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Moving the deployed lasers:
        player.move_laser(enemies, 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Only using this stops the program with an error
                sys.exit()  # Stop execution of the program (without error)

        redraw_window()

        # Player Movements:
        move(player)


def menu():
    check = True
    while check:
        WIN.blit(MENU, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_p]:
                main()
            elif event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                check = False

    pygame.quit()
    sys.exit()  # This is not needed if the game is quit from the menu without being
    # played, but it is needed to overcome running lines 254-256 that would give an
    # error


menu()
