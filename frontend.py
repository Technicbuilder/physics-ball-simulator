#   This is a simple physics 2d collision simulator
#   -------------------------------------------------------------------------------------------------------------------------------------------
#   I designed it so that I can apply and visualise what I learnt in both an visual and entertaining way
#   As of right now it is unfinished any upcoming features will be present in the read me
#   -------------------------------------------------------------------------------------------------------------------------------------------
#   I do use AI however I do not let it mindlessly generate for me I use it to help cover things I do not understand
#   such as  pygame aspects (Ive never really used pygame before this project) and to help smoothen bugs caused by computational limitations,
#   apart from these uses I have not heavily used AI - I believe using AI is a good thing and a good way to learn things because in the near
#   future it is going to become heavily integrated in assisting with coding and developing solutions. You should know and learn from what the
#   AI created before implementing it into code otherwise you do not know what you are coding
#   -------------------------------------------------------------------------------------------------------------------------------------------


import pygame
import random
import json
import time
from kinematics_otherstuff_too import *


with open('physics-ball-simulator-main/configurations.json', 'r') as f:
    config = json.load(f)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity, radius, color, mass):
        super().__init__()

        #   Creates visuals
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        #   Creates the rectangle where balls are going to collide etc
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

        #   Positions, velocities + other values are stored
        self.pos_x = float(x_pos)
        self.pos_y = float(y_pos)
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.mass = mass
        self.gravity = config['physics']['gravity']
        self.restitution = config['ball']['restitution']

    def update(self, screen_width, screen_height):
        self.y_velocity += self.gravity     #   constant velocity

        self.pos_y += self.y_velocity                       #   turns constant velocity into acceleration
        self.pos_x += self.x_velocity


        #   Matches pixels with integers (e.g you cant move a circle 10.5 pixels away from a collision)
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)

        #   collisions with the box edges
        #   self.rect.right is the boundary of the balls
        #   screen width is screen width
        
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
            self.pos_x = float(self.rect.centerx)
            self.x_velocity *= (-1 * self.restitution)

        elif self.rect.left <= 0:
            self.rect.left = 0
            self.pos_x = float(self.rect.centerx)
            self.x_velocity *= (-1 * self.restitution)

        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.pos_y = float(self.rect.centery)
            self.y_velocity *= (-1 * self.restitution)         
            if abs(self.y_velocity) < 1:
                self.y_velocity = 0

        elif self.rect.top <= 0:
            self.rect.top = 1
            self.pos_y = float(self.rect.centery)
            self.y_velocity *= (-1 * self.restitution)



#   INTERFACE
pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Physics collision thingy")
clock = pygame.time.Clock()

all_ball = pygame.sprite.Group()

for random_balls in range(config['ball']['number of balls']):   #   Balls are given random sizes, speeds, colours and starting positions
    random_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    new_ball = Ball(
        random.randint(1, 1000),    # x starting position
        random.randint(1, 600),    # y tarting position
        random.choice((config['ball']['min initial x velocity'], config['ball']['max initial x velocity'])),     # x starting velocity
        random.choice((config['ball']['min initial y velocity'], config['ball']['max initial y velocity'])),     # y starting velocity
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

    #   handles friction against surfaces
    friction(all_ball, config['ball']['mass'], config['physics']['gravity'], config['ball']['coeff of friction'], screen_height=600)

    #   handles air resistance
    air_resistance(all_ball, config['ball']['radius'], config['physics']['air density'], config['ball']['drag coefficient'])

    #   handles physics update
    all_ball.update(WIDTH, HEIGHT)

    #   handles collision
    collisions(all_ball, config['ball']['radius'], config['ball']['restitution'])

    screen.fill((20, 20, 30))
    all_ball.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)  #   60fps

pygame.quit()
