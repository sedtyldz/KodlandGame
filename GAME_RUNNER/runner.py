import pgzrun
import sys  # we need this to exit the game
import random
from pgzhelper import *  # we need this to resize the images

#Game Constants
WIDTH = 1000
HEIGHT = 600
score = 0

#Game Variables
menuView = True
soundMode = False
run = False

# Sound and Text box
sound_on = Actor("sound_on", center=(500, 430))
sound_off = Actor("sound_off", center=(500, 430))
play_rect = Rect((450, 250), (100, 50))
exit_rect = Rect((450, 320), (100, 50))
click = Rect((450, 390), (100, 50))

# Classes
class ship:
    def __init__(self, image, pos):
        self.asset = Actor(image, pos)
        self.images = ["ship1", "ship2", "ship3", "ship4"]
        self.current_frame = 0
        self.point1 = random.randint(70, 970)
        self.point2 = random.randint(70, 970)
        self.fps = 60
        self.laser_list = []

    def draw(self):
        self.asset.draw()
        for laser in self.laser_list:
            laser.draw()

    def shot(self):
        if abs(self.asset.x - self.point1) < 4 or abs(self.asset.x - self.point2) < 4:
            laser = Laser(self.asset.x, self.asset.y)
            sounds.bgsong.stop()
            sounds.shot.play()
            if soundMode:
                sounds.bgsong.play()
            self.laser_list.append(laser)

    def update(self):
        self.asset.x -= 4
        if self.asset.x < -30:
            self.asset.x = WIDTH + random.randint(10, 50)
            self.asset.y = random.randint(60, 200)
            self.update_shot_points()
        self.shot()
        for laser in self.laser_list:
            laser.update()

    def update_shot_points(self):
        self.point1 = random.randint(70, 970)
        self.point2 = random.randint(70, 970)

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.asset.image = self.images[self.current_frame]

class Laser:
    def __init__(self, x, y):
        self.actor = Actor("laser")
        self.actor.x = x
        self.actor.y = y
        self.actor.angle = 90

    def update(self):
        self.actor.y += 5
        if self.actor.y < 0:
            ship.laser_list.remove(self)

    def draw(self):
        self.actor.draw()

class spider:
    def __init__(self, image, pos):
        self.asset = Actor(image, pos)
        self.images = ["spider1", "spider2", "spider3"]
        self.current_frame = 0
        self.fps = 60

    def draw(self):
        self.asset.draw()

    def update(self):
        self.asset.x -= 8
        if self.asset.x < -30:
            self.asset.x = WIDTH + random.randint(10, 50)

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.asset.image = self.images[self.current_frame]

class Hero:
    def __init__(self, x, y):
        self.asset = Actor("stand", (x, y))

        self.run_images = ["run1", "run2", "run3", "run4", "run5", "run6", "run7", "run8"]
        self.run_images_left = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]
        self.jump_image_right = "jump"
        self.jump_image_left = "rjump"
        self.is_jumping = False
        self.current_frame = 0
        self.ground = y
        self.gravity = 2
        self.vertical_velocity = 0
        self.jump_power = -35
        self.direction = "right"

    def draw(self):
        self.asset.draw()

    def fall(self):
        if self.is_jumping:
            self.vertical_velocity += self.gravity
            self.asset.y += self.vertical_velocity
            if self.asset.y >= self.ground:
                self.asset.y = self.ground
                self.is_jumping = False
                self.vertical_velocity = 0

                if self.direction == "left":
                    self.asset.image = "rstand"
                else:
                    self.asset.image = "stand"

    def update(self, keys):
        if keys.right and self.asset.x < WIDTH - 20:
            self.asset.x += 7
            self.direction = "right"
            if not self.is_jumping:
                self.animate()
        elif keys.left and self.asset.x > 20:
            self.asset.x -= 7
            self.direction = "left"
            if not self.is_jumping:
                self.animate()
        else:
            if not self.is_jumping:

                if self.direction == "left":
                    self.asset.image = "rstand"
                else:
                    self.asset.image = "stand"

        if keys.space and not self.is_jumping:
            self.is_jumping = True
            self.vertical_velocity = self.jump_power
            if self.direction == "left":
                self.asset.image = self.jump_image_left
            else:
                self.asset.image = self.jump_image_right

        if self.is_jumping:
            if self.direction == "left":
                self.asset.image = self.jump_image_left
            else:
                self.asset.image = self.jump_image_right

        self.fall()

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.run_images)
        if self.direction == "left":
            self.asset.image = self.run_images_left[self.current_frame]
        else:
            self.asset.image = self.run_images[self.current_frame]

class star:
    def __init__(self, image, pos):
        self.asset = Actor(image, pos)
        self.fps = 15
        self.asset.scale = 1.6

    def draw(self):
        self.asset.draw()

    def update(self):
        self.asset.x -= 3.5
        if self.asset.x < -30:
            self.asset.x = WIDTH + random.randint(10, 50)

# Objects
hero = Hero(30, 530)
enemy1 = ship("ship1", (WIDTH, 100))
enemy2 = spider("spider1", (WIDTH + 100, 550))
star1 = star("star", (WIDTH + 30, 500))

def draw():
    global score
    if menuView:
        draw_menu()
    else:
        if run:
            screen.clear()
            screen.blit("bg", (0, 0))
            enemy1.draw()
            enemy2.draw()
            hero.draw()
            star1.draw()
            show_Score(score)
        else:
            gameover()

def update():
    if not menuView and run:
        hero.update(keyboard)
        if enemy1 is not None:
            enemy1.update()
        if enemy2 is not None:
            enemy2.update()
        if star1 is not None:
            star1.update()
        checkColision()

def show_Score(score):
    screen.draw.text(f"Score = {score}", (400, 30), fontsize=50, color="purple")

def draw_menu():
    screen.clear()
    screen.blit("bg", (0, 0))
    screen.draw.filled_rect(exit_rect, "red")
    screen.draw.filled_rect(play_rect, "green")
    screen.draw.text("Runner Game", (300, 100), fontsize=90, color="white")
    screen.draw.text("PLAY", center=play_rect.center, fontsize=50)
    screen.draw.text("EXIT", center=exit_rect.center, fontsize=50)
    if soundMode:
        sound_on.draw()
        sounds.bgsong.play(-1)
    else:
        sound_off.draw()
        sounds.bgsong.stop()

def gameover():
    global score
    screen.clear()
    screen.blit("bg", (0, 0))
    screen.draw.text("GOOD GAME", (400, 30), fontsize=50, color="white")
    asset = Actor("dead", (500, 200))
    asset.scale = 2.0
    asset.draw()
    screen.draw.text(f"Your Score is = {score}", (370, 300), fontsize=50, color="black")
    screen.draw.text("Click to return menu", center=click.center, fontsize=50, color="green")
    sounds.bgsong.stop()

def on_mouse_down(pos):
    global menuView, soundMode, score, run, enemy1, enemy2, star1, hero
    if sound_on.collidepoint(pos) or sound_off.collidepoint(pos):
        soundMode = not soundMode
    if exit_rect.collidepoint(pos):
        sys.exit()
    if play_rect.collidepoint(pos):
        menuView = False
        run = True
        enemy1 = ship("ship1", (WIDTH, 100))
        enemy2 = spider("spider1", (WIDTH + 100, 550))
        star1 = star("star", (WIDTH + 30, 500))
        hero = Hero(30, 530)
        score = 0
    if click.collidepoint(pos):
        run = False
        menuView = True

def animate_Enemy():
    if not menuView:
        if enemy1 is not None:
            enemy1.animate()
        if enemy2 is not None:
            enemy2.animate()

clock.schedule_interval(animate_Enemy, 0.2)

def checkColision():
    global score, star1, enemy1, enemy2, run, hero
    if hero is not None and hero.asset.colliderect(star1.asset):
        sounds.bgsong.stop()
        sounds.collect.play()
        if soundMode:
            sounds.bgsong.play()
        score += 1
        star1 = None
        star1 = star("star", (WIDTH + random.randint(130, 200), 500))
    if hero is not None and hero.asset.colliderect(enemy2.asset):
        run = False
        star1 = None
        enemy1 = None
        enemy2 = None
        hero = None
    if enemy1 is not None:
        for laser in enemy1.laser_list:
            if hero is not None and hero.asset.colliderect(laser.actor):
                run = False
                star1 = None
                enemy1 = None
                enemy2 = None
                hero = None

pgzrun.go()


