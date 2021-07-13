"""This example spawns (bouncing) balls randomly on a L-shape constructed of 
two segment shapes. Displays collsion strength and rotating balls thanks to 
friction. Not interactive.
"""

import random
import sys

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

pymunk.pygame_util.positive_y_is_up = True


def draw_collision(arbiter, space, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
        pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)


def spawn_ball(mass, radius, position, friction):
    """
    Return the body and shape objects of a ball obtained given inputs mass, radius, position and friction
    """
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.friction = friction
    
    return body, shape
    
def main():

    pygame.init()
    screen_width = 900
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # disable the build in debug draw of collision point since we use our own code.
    draw_options.flags = (
        draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_COLLISION_POINTS
    )
    ## Balls
    balls = []

    ### control platform
    control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    control_body.position = screen_width/2, screen_height/2
    
    # print(control_body.position)
    
    control_shape = pymunk.Segment(control_body, \
            (-200, 0), \
            (200, 0), 0.0)
    
    space.add(control_body, control_shape)
    

    ch = space.add_collision_handler(0, 0)
    ch.data["surface"] = screen
    ch.post_solve = draw_collision

    mass = 0.1
    radius = 25
    position_x = random.randint(screen_width/2 - 200, screen_width/2 + 200)
    position_y = screen_height/2 + radius + 1
    position = position_x, position_y # Tuple of x, y | x is a random number ranging between values to randomize its initial spawn location
    friction = 0.5
    
    body, shape = spawn_ball(mass, radius, position, friction)
    
    
    space.add(body, shape)
    balls.append(shape)
    
    
    
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "contact_with_friction.png")


        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        space.debug_draw(draw_options)
        
        # control_body.angle = control_body.angle + 0.01
        
        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 200:
                balls_to_remove.append(ball)
        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    sys.exit(main())
