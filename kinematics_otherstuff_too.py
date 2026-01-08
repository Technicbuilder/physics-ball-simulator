import math


def collisions(ball_groups, radius):
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

                #   prevents balls from sticking together
                overlap = minimum_distance - distance
                nx = dx / distance
                ny = dy / distance

                ball1.pos_x += nx * overlap / 2
                ball1.pos_y += ny * overlap / 2
                ball2.pos_x -= nx * overlap / 2
                ball2.pos_y -= ny * overlap / 2

                ball1.rect.centerx = int(ball1.pos_x)
                ball1.rect.centery = int(ball1.pos_y)
                ball2.rect.centerx = int(ball2.pos_x)
                ball2.rect.centery = int(ball2.pos_y)
            
            elif distance <= 0.1:
                ball1.pos_x +=1
                ball1.rect.centerx = int(ball1.pos_x)



def air_resistance(ball_groups, radius, density, drag_coefficient):
    balls = ball_groups.sprites()
    cross_sectional_area = math.pi * (radius **2)

    for ball in balls:

        #   calculates resultant velocity
        speed = math.sqrt((ball.x_velocity **2) + (ball.y_velocity **2))

        if speed > 0.01:

            #   air_resistance = 0.5 * p * v^2 * Cd * A
            air_resistance = 0.5 * density * (speed **2) * drag_coefficient * cross_sectional_area

            acceleration = air_resistance / ball.mass

            if acceleration > speed:
                acceleration = speed

            ball.x_velocity -= (ball.x_velocity / speed) * acceleration
            ball.y_velocity -= (ball.y_velocity / speed) * acceleration
        elif speed < 0.1:
            pass