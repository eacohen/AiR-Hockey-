import pygame
import util
from vector import Vector
from math import pi
from collidables import *

# Source: https://math.stackexchange.com/questions/913350/how-to-find-the-intersection-point-of-two-moving-circles

# Pixels per millimeter
pix_per_mm = .3 
# Clock frequency in hertz
clock_freq = 60

class Arena:

    def __init__(self, width, length):
        # Both measured in mm
        self.width = width
        self.length = length

class Puck:

    color = (10, 100, 23)

    def __init__(self, location, velocity, radius):
        self.location = location
        self.velocity = velocity
        self.radius = radius

    # Update location by one clock cycle
    def move(self, collidables):

        # Time left in move 
        time_left = 1/clock_freq

        ii = 0 
        while time_left > 0:

            if ii >= 15:
                while True:
                    ii = ii - 1
                    
            ii = ii + 1

            coll_times = [obj.coll_time(self) for obj in collidables]
            min_pos = util.min_pos(coll_times)

            if min_pos is None or coll_times[min_pos] > time_left:

                # There are no more collisions this cycle 
                new_loc = self.location + (time_left * self.velocity)
                new_vel = self.velocity 
                time_left = 0

            else:
                # There is a collision
                coll_time = coll_times[min_pos]

                if coll_time < 0:
                    print("Error: computed collision in past")

                new_loc = self.location + (coll_time * self.velocity)
                new_vel = collidables[min_pos].collide_velocity(self)
                time_left = time_left - coll_time 

            self.location = new_loc
            self.velocity = new_vel



    # Draw on screen
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (mm_to_pix(self.location.x), 
                                                mm_to_pix(self.location.y)),
                                                mm_to_pix(self.radius))

class Game:

    def __init__(self):

        pygame.init()

        arena_width = 750 
        arena_length = 2000

        self.screen = pygame.display.set_mode((mm_to_pix(arena_width), 
                                               mm_to_pix(arena_length)))

        self.c_pos = Vector(500,430)
        self.c_rad = 100

        self.arena = Arena(arena_width, arena_length)
        self.puck = Puck(Vector(60, 60), Vector.polar(800, pi/6), 30)
        self.clock = pygame.time.Clock()
        self.collidables = [Wall_Vert_Left_Inf(arena_width),
                            Wall_Vert_Right_Inf(0),
                            Wall_Horz_Up_Inf(arena_length),
                            Wall_Horz_Down_Inf(0),
                            Circle(self.c_pos, self.c_rad)]

def mm_to_pix(mm):
    return int(mm * pix_per_mm)

def game_run():
    
    game = Game()

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        game.puck.move(game.collidables)

        game.screen.fill((0, 0, 0))
        game.puck.draw(game.screen)
        pygame.draw.circle(game.screen, (230, 44, 12), 
                (mm_to_pix(game.c_pos.x), mm_to_pix(game.c_pos.y)), mm_to_pix(game.c_rad))
        
        game.clock.tick(clock_freq)
        pygame.display.flip()

clock = pygame.time.Clock()
    

game_run()
