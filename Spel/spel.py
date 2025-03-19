#TODO:   1.s lägg till or (w,a,s,d) för att röra sig

import pygame
import random

# Initiera pygame, mixer
pygame.init()
pygame.mixer.init()

# definerar ljuden
sword_sound = pygame.mixer.Sound("sword.mp3")
potion_sound = pygame.mixer.Sound("potion.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")
death_sound = pygame.mixer.Sound("death.mp3")

# Skärmstorlek
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Slayer")

# Färger i färgkoden RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
PURPLE = (200, 0, 200)

player_size = 60 #storlek 60
monster_size = 60 #storlek 60
potion_size = 60 #storlek 60

# Ladda sprites
try:
    player_img = pygame.image.load("player.png")
    player_img = pygame.transform.scale(player_img, (player_size, player_size))
except FileNotFoundError:
    player_img = pygame.Surface((player_size, player_size))
    player_img.fill(BLUE)

try:
    monster_img = pygame.image.load("monster.png")
    monster_img = pygame.transform.scale(monster_img, (monster_size, monster_size))
except FileNotFoundError:
    monster_img = pygame.Surface((monster_size, monster_size))
    monster_img.fill(RED)

try:
    potion_img = pygame.image.load("potion.png")
    potion_img = pygame.transform.scale(potion_img, (potion_size, potion_size))
except FileNotFoundError:
    potion_img = pygame.Surface((potion_size, potion_size))
    potion_img.fill(PURPLE)

# Typsnitt
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Spelklasser
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 40
        self.health = 100
        self.attack = 10
        self.inventory = {"Potion": 2}
        self.xp = 0
        self.level = 1
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self):
        screen.blit(player_img, (self.x, self.y))
    
    def roll_dice(self):
        return random.randint(1, 20)
    
    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.level * 10:
            self.level += 1
            self.attack += 5
            self.health += 20
            self.xp = 0

    def use_item(self, item):
        if item == "Potion" and self.inventory.get("Potion", 0) > 0:
            self.health += 20
            self.inventory["Potion"] -= 1
            return True
        return False

try:
    background_img = pygame.image.load("background.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Justera storleken om det behövs
except FileNotFoundError:
    background_img = pygame.Surface((WIDTH, HEIGHT))  # Om filen inte finns, skapa en vit bakgrund
    background_img.fill(WHITE)

def battle(player, monster):
    battle_active = True
    while battle_active:
        screen.fill(BLACK)
        draw_text(f"Monster HP: {monster.health}", 50, 50, RED)
        draw_text(f"Player HP: {player.health}", 50, 100, GREEN)
        draw_text("Press SPACE to attack, P to use Potion", 50, 200, WHITE)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attack_roll = player.roll_dice()
                    if attack_roll > 10:
                        monster.health -= player.attack
                        pygame.mixer.Sound.play(sword_sound)
                        draw_text(f"Hit! Monster HP: {monster.health}", 50, 300, GREEN)
                        pygame.display.flip()
                        pygame.time.delay(1250)
                    else:
                        player.health -= 10
                        pygame.mixer.Sound.play(hit_sound)
                        draw_text(f"Missed! You took 10 damage. HP: {player.health}", 50, 300, RED)
                        pygame.display.flip()
                        pygame.time.delay(1250)
                    
                if monster.health <= 0:
                    player.gain_xp(10)
                    screen.fill(BLACK)  # Rensa skärmen så inga gamla texter syns
                    draw_text("You killed the monster!", 50, 300, GREEN)  # Ändra till grön om det är en vinst
                    pygame.mixer.Sound.play(death_sound)
                    pygame.display.flip()
                    pygame.time.delay(2000)  # Låter texten visas tydligare
                    battle_active = False
                elif event.key == pygame.K_p:
                    if player.use_item("Potion"):
                        draw_text(f"You used a Potion! HP: {player.health}", 50, 300, PURPLE)
                        pygame.mixer.Sound.play(potion_sound)
                    else:
                        draw_text("No Potions left!", 50, 300, RED)
                    pygame.display.flip()
                    pygame.time.delay(1250)

# Monster-klass
class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.health = 30
    
    def draw(self):
        screen.blit(monster_img, (self.x, self.y))

# Potion-klass
class Potion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.visible = True

    def draw(self):
        if self.visible:
            screen.blit(potion_img, (self.x, self.y))

def check_collision(player, monster):
    return (player.x < monster.x + monster.size and
            player.x + player.size > monster.x and
            player.y < monster.y + monster.size and
            player.y + player.size > monster.y)

def check_collision(player, potion):
    return (player.x < potion.x + potion.size and
            player.x + player.size > potion.x and
            player.y < potion.y + potion.size and
            player.y + player.size > potion.y)

# Spelinstanser
player = Player()
monster = Monster(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
potion = Potion(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))

# Spel-loop
running = True
clock = pygame.time.Clock()
while running:
    screen.blit(background_img, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        player.move(5, 0)
    if keys[pygame.K_UP]:
        player.move(0, -5)
    if keys[pygame.K_DOWN]:
        player.move(0, 5)
    
    # Kolla efter kollision monster
    if check_collision(player, monster):
        battle(player, monster)
        monster = Monster(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))

    # Kolla efter kollision potion
    if check_collision(player, potion):
        player.inventory["Potion"] += 1
        pygame.mixer.Sound.play(potion_sound)
        potion.visible = False  # Gömmer potionen
        potion.x, potion.y = -100, -100  # Flyttar bort potionen från spelområdet
        


    if player.x >= WIDTH:
        monster = Monster(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        potion = Potion(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        player.x = 0
    elif player.x <= 0:
        monster = Monster(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        potion = Potion(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        player.x = WIDTH

    if player.y >= HEIGHT:
        monster = Monster(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        potion = Potion(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        player.y = 0
    elif player.y <= 0:
        monster = Monster(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        potion = Potion(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        player.y = HEIGHT

    player.draw()
    monster.draw()
    potion.draw()
    
    draw_text(f"XP: {player.xp}  Level: {player.level}  Potions: {player.inventory.get('Potion', 0)}", 50, HEIGHT - 50, WHITE)
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()