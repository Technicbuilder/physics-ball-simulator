import pygame
import random
import json
import time
from kinematics_otherstuff_too import *


with open('configurations.json', 'r') as f:
    config = json.load(f)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, xv, yv, radius, color, mass):
        super().__init__()

        #   Creates visuals
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        #   Creates the rectangle where balls are going to collide etc
        self.rect = self.image.get_rect(center = (x, y))

        #   Positions and velocities are stored
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.x_velocity = xv
        self.y_velocity = yv
        self.mass = mass
        self.gravity = 0.16
        

    def update(self, screen_width, screen_height):
        self.y_velocity += config['physics']['gravity']     #   constant velocity

        self.pos_y += self.y_velocity                       #   turns constant velocity into acceleration
        self.pos_x += self.x_velocity


        #   Matches pixels with integers (e.g you cant move a circle 10.5 pixels away from a collision)
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)

        #   collisions with the box edges
        #   self.rect.right is the boundary rectangle
        #   screen width is screen width
        
        if self.rect.right >= screen_width and self.x_velocity < 0:
            self.rect.right = screen_width
            self.pos_x = float(self.rect.centerx)
            self.x_velocity *= -1

        elif self.rect.left <= 0 and self.x_velocity < 0:
            self.rect.left = 0
            self.pos_x = float(self.rect.centerx)
            self.x_velocity *= -1

        if self.rect.bottom >= screen_height and self.y_velocity < 0:
            self.rect.bottom = screen_height
            self.pos_y = float(self.rect.centery)
            self.y_velocity *= -1         
            if abs(self.y_velocity) < 1:
                self.y_velocity = 0

        elif self.rect.top <= 0 and self.y_velocity < 0:
            self.rect.top = 0
            self.pos_y = float(self.rect.centery)
            self.y_velocity *= -1


#   INTERFACE
pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Physics collision thingy")
clock = pygame.time.Clock()

all_ball = pygame.sprite.Group()

for random_balls in range(20):   #   Balls are given random sizes, speeds, colours and starting positions
    random_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    new_ball = Ball(
        random.randint(50, 750),    # x starting position
        random.randint(50, 550),    # y tarting position
        10,     # x starting velocity
        10,     # y starting velocity
        config['ball']['radius'],   # ball radius
        random_color,               # ball colour
        config['ball']['mass']      # ball mass
    )

    all_ball.add(new_ball)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #   handles air resistance
    air_resistance(all_ball, config['ball']['radius'], config['physics']['air density'], config['ball']['drag coefficient'])

    #   handles physics update
    all_ball.update(WIDTH, HEIGHT)

    #   handles collision
    collisions(all_ball, config['ball']['radius'])

    screen.fill((20, 20, 30))
    all_ball.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)  #   60fps

pygame.quit()
