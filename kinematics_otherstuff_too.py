import math


def collisions(ball_groups, radius, restitution):
    balls = ball_groups.sprites()

    for i in range(len(balls)):
        for j in range((i + 1), len(balls)):    #   (i+1) becuase ball isnt going to collide with itself
            ball1 = balls[i]
            ball2 = balls[j]

            #   calculates differences in position
            dy = ball1.pos_y - ball2.pos_y
            dx = ball1.pos_x - ball2.pos_x

            # calculates distance between balls, and the minium distance the distance between them can be before they collide
            distance = math.sqrt((dy **2) + (dx **2))
            minimum_distance = (radius * 2) 

            if 0.1 < distance <= minimum_distance:
                ball1.x_velocity, ball1.y_velocity, ball2.x_velocity, ball2.y_velocity = \
                ball2.x_velocity, ball2.y_velocity, ball1.x_velocity, ball1.y_velocity

                relative_x_velocity = ball1.x_velocity - ball2.x_velocity
                relative_y_velocity = ball1.y_velocity - ball2.y_velocity

                #   calculates raw/total distance (a scale)
                #   represents direction
                nx = dx / distance
                ny = dy / distance

                velocity_along_normal_of_centers = (relative_x_velocity * nx) + (relative_y_velocity * ny)

                if velocity_along_normal_of_centers < 0:
                    impulse = ((1+ restitution) * velocity_along_normal_of_centers / (ball1.mass + ball2.mass))

                    #   multiplies impulse by balls mass then by nx (direction vector)
                    #   ensures balls are pushed back depending on sizes
                    ball1.x_velocity -= impulse * ball2.mass * nx
                    ball1.y_velocity -= impulse * ball2.mass * ny

                    ball2.x_velocity += impulse * ball1.mass * nx
                    ball2.y_velocity += impulse * ball1.mass * ny

                #   splits the difference of the overlap and reverses each ball by the difference
                #   done to push them apart preventing them from sticking together
                overlap = minimum_distance - distance

                ball1.pos_x += nx * overlap / 2
                ball1.pos_y += ny * overlap / 2

                ball2.pos_x -= nx * overlap / 2
                ball2.pos_y -= ny * overlap / 2

                #   refreshes visuals after unsticking the balls
                ball1.rect.centerx = int(ball1.pos_x)
                ball1.rect.centery = int(ball1.pos_y)
            
                ball2.rect.centerx = int(ball2.pos_x)
                ball2.rect.centery = int(ball2.pos_y)
            
            elif distance <= 0.1:
                ball1.pos_x +=1
                ball1.rect.centerx = int(ball1.pos_x)



def air_resistance(ball_groups, radius, density, drag_coefficient): #    fluid_velocity_air
    balls = ball_groups.sprites()
    cross_sectional_area = math.pi * (radius **2)
    #relative_x_velocity = ball.x_velocity - fluid_velocity_air  implement relative velocities when possible
    #relative_x_velocity = ball.x_velocity - fluid_velocity_air

    for ball in balls:

        #   calculates resultant velocity
        speed = math.sqrt((ball.x_velocity **2) + (ball.y_velocity **2))

        if speed > 0.01:

            #   air_resistance = 0.5 * p * v^2 * Cd * A
            air_resistance = 0.5 * density * (speed **2) * drag_coefficient * cross_sectional_area

            acceleration = air_resistance / ball.mass

            #   prevents balls from snapping back into the opposite direction
            if acceleration > speed:
                acceleration = speed

            #   calculate new velocities 
            #   dividing velocities by speed gives direction, this then increases acceleration in said direction
            ball.x_velocity -= (ball.x_velocity / speed) * acceleration
            ball.y_velocity -= (ball.y_velocity / speed) * acceleration


def friction(ball_groups, mass, gravity, coeff_friction, screen_height):
    balls = ball_groups.sprites()
    
    for ball in balls:
        if ball.rect.bottom >= screen_height and abs(ball.y_velocity) < 0.5:
            weight = mass * gravity
            
            # coefficient of friction determines the friction, the lower the more slippery
            force = coeff_friction * weight

            #   calculates the force the friction acts against
            opposing_acceleration = force / mass

            #   determines whether velocity is more than friction otherwise stop ball.x_velocity
            if abs(ball.x_velocity) > opposing_acceleration:

                #   determines whether opposing friction force should be + or - depending on the direction of velocity
                if ball.x_velocity > 0:
                    fric_direction = 1
                else:
                    fric_direction = -1

                #   calculates new position
                ball.x_velocity -= opposing_acceleration * fric_direction
            
            else:
                ball.x_velocity = 0

    

