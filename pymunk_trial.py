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
    
    if __debug__:
        pygame.init()
    screen_width = 900
    screen_height = 600
    if __debug__:
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    if __debug__:
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        #disable the build in debug draw of collision point since we use our own code.
        draw_options.flags = (
            draw_options.flags ^ pymunk.pygame_util.DrawOptions.DRAW_COLLISION_POINTS
        )

    ### control platform
    platform_length = 400
    control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    control_body.position = screen_width/2, screen_height/2
    control_shape = pymunk.Segment(control_body, \
            (-platform_length/2, 0), \
            (+platform_length/2, 0), 0.0)
    
    space.add(control_body, control_shape)
    
    if __debug__:
        ch = space.add_collision_handler(0, 0)
        ch.data["surface"] = screen
        ch.post_solve = draw_collision

    mass = 1
    radius = 25
    position_x = random.randint(screen_width/2 - 200, screen_width/2 + 200)
    position_y = screen_height/2 + radius + 1
    position = position_x, position_y # Tuple of x, y | x is a random number ranging between values to randomize its initial spawn location
    friction = 0.5
    
    ball_body, ball_shape = spawn_ball(mass, radius, position, friction)
    
    
    space.add(ball_body, ball_shape)
    
    
    turn_rate = 0.01
    
    
    while running:
        if __debug__:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pygame.image.save(screen, "contact_with_friction.png")
               
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                control_body.angle += turn_rate
            if keys[pygame.K_RIGHT]:
                control_body.angle -= turn_rate
                
            ## Clear screen
            screen.fill(pygame.Color("white"))

            ## Draw stuff
            space.debug_draw(draw_options)
        
        if ball_body.position.y < 0:
            running = False

        ### Update physics
        dt = 1.0 / 60.0
        for x in range(1):
            space.step(dt)

        if __debug__:
            ### Flip screen
            pygame.display.flip()
            clock.tick(50)
            pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    sys.exit(main())
