import pygame
import math
import time
import copy
import random

pygame.init()

# ---------------- Setting up the screen, assigning some global variables, and loading text fonts
screen = pygame.display.set_mode((1400, 700))
clock = pygame.time.Clock()
fps = 60
screen_width = screen.get_width()
screen_height = screen.get_height()
screen2 = pygame.Surface((screen_width, screen_height)).convert_alpha()
screenT = pygame.Surface((screen_width, screen_height)).convert_alpha()
screenT.set_alpha(100)
screenUI = pygame.Surface((screen_width, screen_height)).convert_alpha()
timer = 0
shake = [0, 0]
shake_strength = 3
scroll_counter = 0
pygame.font.get_fonts()
font15 = pygame.font.Font("freesansbold.ttf", 15)
font20 = pygame.font.Font("freesansbold.ttf", 20)
font30 = pygame.font.Font("freesansbold.ttf", 30)
font40 = pygame.font.Font("freesansbold.ttf", 40)
better_font40 = pygame.font.SysFont("keyboard.ttf", 40)
font50 = pygame.font.Font("freesansbold.ttf", 50)
font100 = pygame.font.Font("freesansbold.ttf", 100)
number_of_crests = 4


class Endesga:
    maroon_red = (87, 28, 39)
    lighter_maroon_red = (127, 36, 51)
    dark_green = (9, 26, 23)
    light_brown = (191, 111, 74)
    black = (19, 19, 19)
    grey_blue = (66, 76, 110)
    cream = (237, 171, 80)
    white = (255, 255, 255)
    greyL = (200, 200, 200)
    grey = (150, 150, 150)
    greyD = (100, 100, 100)
    greyVD = (50, 50, 50)
    very_light_blue = (199, 207, 221)
    my_blue = [7, 15, 21]


class slider:
    def __init__(self, x, y, width, height, orientation):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.click = False
        self.o = orientation
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.bar = 200

    def detect(self, clik, x, y):
        if clik:
            if self.rect.collidepoint((x, y)):
                if self.o == "ver":
                    self.bar = y - self.y
                    return math.fabs(self.bar / self.h)
                if self.o == "hor":
                    self.bar = x - self.x
                    return math.fabs(self.bar / self.w)
        return math.fabs(self.bar / self.w + 0.01)

    def draw(self, display_screen, color, bar_color):
        if self.o == "ver":
            pygame.draw.rect(display_screen, bar_color, pygame.rect.Rect(self.x, self.y, self.w, self.bar), 0, math.floor(self.w / 4))
            pygame.draw.rect(display_screen, color, self.rect, int(self.w / 10), math.floor(self.w / 4))
        if self.o == "hor":
            pygame.draw.rect(display_screen, bar_color, pygame.rect.Rect(self.x, self.y, self.bar, self.h), 0, math.floor(self.h / 4))
            pygame.draw.rect(display_screen, color, self.rect, int(self.h / 10), math.floor(self.h / 4))


def f(x, crests):
    return math.cos(2 * math.pi * crests * 2 * x / screen_width) * 50 + math.cos(5 * math.pi * crests * 2 * x / screen_width / 2) * 50


def path(length, res, shift, c):
    cords = []
    n = math.ceil(length / res)
    for p in range(res + 1):
        cords.append([p * n, f(p * n, c) + shift])
    return cords


class Car:
    def __init__(self, x, y, size, angle, speed):
        self.x = x
        self.y = y
        self.y_prev = y
        self.deriv = (self.y - self.y_prev) / fps
        self.deriv_prev = (self.y - self.y_prev) / fps
        self.accel = (self.deriv - self.deriv) / fps
        self.size = size
        self.a = angle
        self.speed = speed

    def move(self):
        self.y_prev = copy.deepcopy(self.y)
        self.x += self.speed * math.cos(self.a)
        self.y += self.speed * math.sin(self.a)
        self.deriv_prev = copy.deepcopy(self.deriv)
        self.deriv = (self.y - self.y_prev) / fps
        self.accel = (self.deriv - self.deriv_prev) / fps
        if self.x >= screen_width:
            self.x = 1
        if self.x < 0:
            self.x = screen_width

    def draw(self):
        cords = [[self.x + self.size * (math.cos(self.a - math.pi) - math.sin(self.a - math.pi)), self.y + self.size * (math.sin(self.a - math.pi) + math.cos(self.a - math.pi))],
                 [self.x + self.size * (math.cos(self.a - (math.pi / 2)) - math.sin(self.a - (math.pi / 2))), self.y + self.size * (math.sin(self.a - (math.pi / 2)) + math.cos(self.a - (math.pi / 2)))],
                 [self.x + self.size * (math.cos(self.a) - math.sin(self.a)), self.y + self.size * (math.sin(self.a) + math.cos(self.a))],
                 [self.x + self.size * (math.cos(self.a + (math.pi / 2)) - math.sin(self.a + (math.pi / 2))), self.y + self.size * (math.sin(self.a + (math.pi / 2)) + math.cos(self.a + (math.pi / 2)))]]
        pygame.draw.polygon(screen2, Endesga.white, cords)

    def drawUI(self, c):
        pygame.draw.line(screen2, Endesga.cream, (self.x, self.y), (self.x, (f(self.x, c) + screen_height / 2)), 5)
        pygame.draw.line(screen2, Endesga.cream, (self.x, self.y), (self.x + self.size * 5 * math.cos(self.a), self.y + self.size * 5 * math.sin(self.a)))

    def calc_dist(self, c):
        return self.y - (f(self.x, c) + screen_height / 2)

    def bang_bang_controller(self, d, proportionality_constant):
        self.a -= proportionality_constant * d

    def derivative_controller(self, d, proportionality_constant, proportionality_constant_der):
        self.a -= proportionality_constant * d + proportionality_constant_der * self.deriv

    def pd_controller(self, d, proportionality_constant_theta, proportionality_constant_der):
        self.a -= proportionality_constant_theta * self.a + proportionality_constant_der * d / self.speed


car = Car(0, screen_height / 2 + 80, 15, 0, 5)
# Defining some more variables to use in the game loop
click = False
oscillating_random_thing = 0
ShakeCounter = 0
scale_slider = slider(50, screen_height - 100, 200, 25, "hor")

# ---------------- Main Game Loop
last_time = time.time()
running = True
while running:

    # ---------------- Reset Variables and Clear screens
    oscillating_random_thing += math.pi/fps
    mx, my = pygame.mouse.get_pos()
    screen.fill(Endesga.my_blue)
    screen2.fill(Endesga.my_blue)
    screenT.fill((0, 0, 0, 0))
    screenUI.fill((0, 0, 0, 0))
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    timer -= 1 * dt
    shake = [0, 0]
    points = path(screen_width, int(number_of_crests + 1) * 50, screen_height / 2, number_of_crests)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            pass

    for i, point in enumerate(points):
        if i > 0:
            if i % 2 == 0:
                pygame.draw.line(screen2, Endesga.white, points[i], points[i - 1], 5)

    # ---------------- Car Calculations
    dist = better_font40.render("Error: " + str(int(100 * car.calc_dist(number_of_crests)) / 100), True, Endesga.white)
    screen2.blit(dist, (50, 50))
    deriv = better_font40.render("Derivative of Error: " + str(int(car.deriv * 1000) / 1000), True, Endesga.white)
    screen2.blit(deriv, (50, 100))

    # ---------------- Moving and displaying the car
    car.move()
    car.draw()
    car.drawUI(number_of_crests)
    # bang bang constant — 0.0001
    # car.bang_bang_controller(car.calc_dist(number_of_crests), 0.0001)

    # derivative controller — 0.0005, 0.5
    # car.derivative_controller(car.calc_dist(number_of_crests), 0.0005, 0.5)

    # pd controller —0.02, 0.002
    car.pd_controller(car.calc_dist(number_of_crests), 0.5, 0.14)

    number_of_crests = int(4 * scale_slider.detect(click, mx, my))
    scale_slider.draw(screen2, Endesga.white, Endesga.cream)

    # ---------------- Updating Screen
    pygame.mouse.set_visible(False)
    pygame.draw.circle(screenUI, Endesga.white, (mx, my), 5, 1)
    screen.blit(screen2, (shake[0], shake[1]))
    screen.blit(screenT, (0, 0))
    screen.blit(screenUI, (0, 0))
    pygame.display.update()
    clock.tick(fps)
