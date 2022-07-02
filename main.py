import pygame
import os
# import time
import random


pygame.font.init()

# Width , height of the playing window
WIDTH, HEIGHT = 720, 670

# Set the display of pygame
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighters")

# Loading images
# Menu
MENU = pygame.image.load(os.path.join('assets', 'menu.png'))
# 1. Player Ships
PLAYER_SHIP_1 = pygame.image.load(os.path.join('assets', 'player_ship.png'))

# 2. Enemy Ships
ENEMY_SHIP_1 = pygame.image.load(os.path.join('assets', 'red_enemy.png'))

# 3. Lasers
BLUE_LASERS = pygame.image.load(os.path.join("assets", "blue_laser.png"))

# 4. Background
BG_1 = pygame.image.load(os.path.join(os.path.abspath(__file__), "../assets/space_bg.png"))


# Making Object classes
class Laser:
    def __init__(self, x ,y , img) :
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window) :
        window.blit(self.img, (self.x , self.y))

    def move(self,vel) :
        self.y -= vel 

    def off_screen(self, height) :
        return self.y > height and self.y < 0

    def collision(self,obj) :
        return collide(self,obj)


class ship:
    COOLDOWN = 40
    #initialising object parameters
    def __init__(self,x,y,health=100) :
        self.x = x
        self.y = y 
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
        self.cnt = 0

    #Draw for the ship
    def draw(self,window) :
        window.blit(self.ship_img,(self.x , self.y))
        for laser in self.lasers :
            laser.draw(window) 
    #For providing interval between lasers
    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN :
            self.cooldown_counter = 0 
        elif self.cooldown_counter > 0 :
            self.cooldown_counter += 1

    def get_width(self) :
        return self.ship_img.get_width()

    def get_height(self) :
        return self.ship_img.get_height()

class Player(ship) :
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP_1
        self.laser_img = BLUE_LASERS
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def shoot(self) :
        self.cooldown()
        if self.cooldown_counter == 0 :
            laser = Laser(self.x ,self.y , self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def move_laser(self,objs,vel) :  
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT) :
                self.lasers.remove(laser)
            else:
                for obj in objs :
                    if (laser.collision(obj)) :
                        objs.remove(obj)
                        self.lasers.remove(laser)
    def draw (self,window) :
        super().draw(window)
        self.health_bar(window)
    
    def health_bar(self,win) :
        pygame.draw.rect(win,(255,0,0),(self.x , self.y + self.ship_img.get_height() + 10 ,self.ship_img.get_width() , 10 ))
        pygame.draw.rect(win,(0,255,0),(self.x , self.y + self.ship_img.get_height() + 10 ,(self.ship_img.get_width())*(1-(self.max_health-self.health)/self.max_health) , 10 ))
                          

# Eneny SHip
class Enemy (ship) :
    def __init__(self, x, y, level, health=100):
        super().__init__(x, y, health)
        self.ship_img = ENEMY_SHIP_1
        self.laser_img = BLUE_LASERS
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def shoot(self) :
        self.cooldown()
        if self.cooldown_counter == 0 :
            laser = Laser(self.x + self.get_width()/2 -5 ,self.y + self.get_height() , self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def move(self) :
        vel = 1
        self.y +=vel

    def move_laser(self,obj,vel) :
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT) :
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -=10
                self.lasers.remove(laser)

#defining collide
def collide(obj1,obj2) :
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None

#defining movemet
def move (player,key_press) :
    ship_vel = 5
    key_press = pygame.key.get_pressed()
    if (key_press[pygame.K_a] or key_press[pygame.K_LEFT]) and player.x - ship_vel > 0: #LEFT
        player.x-=ship_vel
    if (key_press[pygame.K_d] or key_press[pygame.K_RIGHT]) and player.x + ship_vel + player.get_width() < WIDTH : #RIGHT
        player.x+=ship_vel
    if (key_press[pygame.K_w] or key_press[pygame.K_UP]) and player.y - ship_vel > 0 : # UP
        player.y-=ship_vel
    if (key_press[pygame.K_s] or key_press[pygame.K_DOWN]) and player.y + ship_vel + player.get_height() < HEIGHT : # Down
        player.y+=ship_vel
    if (key_press[pygame.K_SPACE]) :
        player.shoot()          


#defing main
def main():
    run = True # Checks if the user has stopped the program or not
    lost = False
    FPS = 70 
    level = 0
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans",40) #Font used for lives and level
    lost_font = pygame.font.SysFont('arial',60)
    #Objct parameters
    player = Player(WIDTH/2, HEIGHT-70) 
    enemies = []
    num_enemies = 5
    
    #Draws object on the console window
    def redraw_window(): 
        WIN.blit(BG_1,(0,0))
        
        #Lives and Level Display
        lives_disp = main_font.render(f"LIVES: {lives}",1,(255,255,255))
        level_disp = main_font.render(f"LEVEL: {level}",1,(255,255,255))
        WIN.blit(lives_disp,(10,10))
        WIN.blit(level_disp,(WIDTH-level_disp.get_width() -10, 10))    

        #displaying ship
        player.draw(WIN)

        #Enemy Ship
        for enemy in enemies :
            enemy.draw(WIN)

        #Game Lost
        if lost :
            lost_disp = lost_font.render("Better luck Next Time!!",1,(255,0,0))
            menu()
            WIN.blit(lost_disp,(WIDTH/2 - lost_disp.get_width()/2 ,HEIGHT/2 - lost_disp.get_height()/2))

        pygame.display.update()
    
    
     
    while (run) :
        clock.tick(FPS)
        

        #Checking for lives and health
        if ( lives == 0 or player.health <= 0) :
            lost = True 
        # Deploying enemenies
        if len(enemies) == 0 :
            level+=1
            num_enemies+=5
            for i in range(num_enemies) :
                enemy = Enemy(random.randrange(100 ,WIDTH-200),random.randrange(-1000,-100),level)
                enemies.append(enemy)
        
        # Moving and removing enemies
        for enemy in enemies:
            enemy.move()
            if random.randrange(0,2400) == 2 :
                enemy.shoot()
            # IF player and enemy collide
            if (collide(player,enemy)) :
                player.health -= 25 
                enemies.remove(enemy)
            enemy.move_laser(player,-2)
            # enemy.move_laser(7,player)
            if enemy.y + enemy.get_height() > HEIGHT :
                lives -= 1
                enemies.remove(enemy)
        
        #Moving the deployed lasers        
        player.move_laser(enemies,4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        
        
        redraw_window ()
        #Player Movemets
        key_press = pygame.key.get_pressed()
        move(player,key_press)

def menu() :
    check = True 
    while(check) :
        WIN.blit(MENU,(0,0)) 
        pygame.display.update()
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_p] :
                main()
            elif event.type == pygame.QUIT :
                check = False
            elif pygame.key.get_pressed()[pygame.K_q] :
                check = False

    pygame.quit()
            
menu()
            
