import pygame
import os
import util
import threading
from vector import Vector
from math import pi
from collidables import *

# Source: https://math.stackexchange.com/questions/913350/how-to-find-the-intersection-point-of-two-moving-circles

FIFO = 'fifo'

# Pixels per millimeter
pix_per_mm = .3 
# Clock frequency in hertz
clock_freq = 120

class Puck(Circle):

    color = (255, 4, 4)

    def __init__(self, location, velocity, radius):
        self.base_location = location
        self.base_velocity = velocity
        self.location = self.base_location
        self.velocity = self.base_velocity
        self.radius = radius
        self.ghost = False
        self.max_velocity = 10000

    # Update location by one clock cycle
    def move(self, collidables):

        # Time left in move 
        time_left = 1/clock_freq

        while time_left > 0:

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
                    # Weird paddle movement happened
                    # Pretend that the paddle doesn't exist
                    collidables[min_pos].ghost = True
                    continue

                else:
                    new_loc = self.location + (coll_time * self.velocity)
                    new_vel = collidables[min_pos].collide_velocity(self, new_loc)
                    time_left = time_left - coll_time 

            self.location = new_loc
            self.velocity = new_vel

    # Has a goal just been scored?
    # Returns false if no goal, -1 if left goal, 1  if right goal
    def goal(self, arena):

        if self.location.x > arena.x_len + arena.border_width:
            # Left scores
            return -1 
        if self.location.x < -arena.border_width:
            # Right scores
            return 1 
        return False

    # Reset position 
    def reset(self):
        self.location = self.base_location
        self.velocity = self.base_velocity

    # Draw on screen
    def draw(self, arena):
        pygame.draw.circle(arena.screen, self.color, 
                           (mm_to_pix(self.location.x + arena.border_width), 
                            mm_to_pix(self.location.y + arena.border_width)),
                           mm_to_pix(self.radius))

class Paddle(Circle):

    def __init__(self, location, radius, color, left):
        self.location = location 
        self.new_location = Vector(0, 0)
        self.radius = radius
        self.color = color
        self.ghost = False
        self.velocity = Vector(0, 0)
        self.coll_const = .8 
        # Is left paddle
        self.left = left
    
    # Update the location from a mouse position
    def start_move(self, new_pos, arena, puck):
        (m_x, m_y) = new_pos
        self.new_location = Vector(pix_to_mm(m_x), pix_to_mm(m_y)) \
                            - Vector(arena.border_width, arena.border_width)
        self.velocity = clock_freq * (self.new_location - self.location) 

        if not self.ghost:
            # The paddle can't collide with the puck while its ghost, in order
            # to let the puck move away

            # See if the paddle crashes into the puck
            puck_coll_time = puck.coll_time(self)

            if puck_coll_time != None and puck_coll_time < 1/clock_freq:

                # The paddle will collide with the puck
                self.location = self.location + puck_coll_time * self.velocity

                if self.invalid_loc(arena):
                    self.ghost = True
                else:
                    puck.velocity = self.collide_velocity(puck, puck.location)

            else:
                self.location = self.new_location
        else:
            self.location = self.new_location

        if self.invalid_loc(arena):
            self.ghost = True

    def end_move(self, arena, puck):
        self.location = self.new_location
        self.ghost = self.intersecting(puck) or self.invalid_loc(arena)

    # Paddle in a position where it shouldn't hit the puck 
    def invalid_loc(self, arena):

        # Is the paddle over the center line
        if self.left:
            if (self.location.x + self.radius) > (arena.x_len + arena.mid_line_width)/2:
                return True 
        else:
            if (self.location.x - self.radius) < (arena.x_len - arena.mid_line_width)/2:
                return True

        # Paddle over borders
        if self.location.x < self.radius:
            return True
        if self.location.x > arena.x_len - self.radius:
            return True
        if self.location.y < self.radius:
            return True
        if self.location.y > arena.y_len - self.radius:
            return True

        return False

    def draw(self, arena):
        pygame.draw.circle(arena.screen, self.color, 
                           (mm_to_pix(self.location.x + arena.border_width), 
                            mm_to_pix(self.location.y + arena.border_width)),
                           mm_to_pix(self.radius))

# Represents the surface that the game is played on
class Arena:

    border_width = 100 
    border_color = (10, 15, 176)
    space_color = (255,255,255)

    x_len = 3000
    y_len = 1000

    goal_width = 300
    goal_y_low = (y_len - goal_width) / 2
    goal_y_high = (y_len + goal_width) / 2

    screen_x = x_len + 2 * border_width
    screen_y = y_len + 2 * border_width

    mid_line_width = 50


    def __init__(self):

        self.screen = pygame.display.set_mode((mm_to_pix(self.screen_x), 
                                               mm_to_pix(self.screen_y)))

    def draw(self):
        borders = pygame.Rect(0, 0, mm_to_pix(self.screen_x), mm_to_pix(self.screen_y))
        pygame.draw.rect(self.screen, self.border_color, borders)

        cent_arena = pygame.Rect(mm_to_pix(self.border_width), 
                                 mm_to_pix(self.border_width),
                                 mm_to_pix(self.x_len), 
                                 mm_to_pix(self.y_len))
        pygame.draw.rect(self.screen, self.space_color, cent_arena)
        
        goal_right = pygame.Rect(mm_to_pix(self.border_width + self.x_len), 
                                 mm_to_pix(self.border_width + self.goal_y_low),
                                 mm_to_pix(self.border_width), 
                                 mm_to_pix(self.goal_width))
        pygame.draw.rect(self.screen, self.space_color, goal_right)

        goal_left = pygame.Rect(mm_to_pix(0), 
                                 mm_to_pix(self.border_width + self.goal_y_low),
                                 mm_to_pix(self.border_width), 
                                 mm_to_pix(self.goal_width))
        pygame.draw.rect(self.screen, self.space_color, goal_left)

        # Draw middle line
        mid_line = pygame.Rect(mm_to_pix(self.border_width \
                               + (self.x_len - self.mid_line_width)/2),
                               mm_to_pix(self.border_width),
                               mm_to_pix(self.mid_line_width),
                               mm_to_pix(self.y_len))
        pygame.draw.rect(self.screen, (0,0,0), mid_line)


class Game:

    def __init__(self):

        pygame.init()

        self.win_score = 7
        self.arena = Arena()
        self.puck = Puck(Vector(self.arena.x_len/2, self.arena.y_len/2), 
                         Vector(0,0), 50)
        paddle_color = (196, 0, 0)
        self.paddle_1 = Paddle(Vector(300, 300), 70, paddle_color, False)
        self.paddle_2 = Paddle(Vector(200, self.arena.y_len / 2), 70, paddle_color, True)
        self.clock = pygame.time.Clock()
        
        # (left score, right score)
        self.score = (0,0)

        # Very small corner circle radius
        bcirc_r = 10

        # Objects that the puck can collide with
        self.collidables = [
                            # Upper right wall
                            Wall_Vert_Left(self.arena.x_len, 0,
                                self.arena.goal_y_low),
                            # Lower right wall
                            Wall_Vert_Left(self.arena.x_len, 
                                self.arena.goal_y_high,
                                self.arena.y_len),
                            # Right goal top wall
                            Wall_Horz_Down(self.arena.x_len, 
                                self.arena.x_len 
                                + 2*self.puck.radius + self.arena.border_width,
                                self.arena.goal_y_low),
                            # Right goal bottom wall
                            Wall_Horz_Up(self.arena.x_len, 
                                self.arena.x_len 
                                + 2*self.puck.radius + self.arena.border_width,
                                self.arena.goal_y_high),
                            # Right goal top corner
                            Circle(Vector(self.arena.x_len + bcirc_r,
                                          self.arena.goal_y_low - bcirc_r),
                                   bcirc_r),
                            # Right goal bottom corner
                            Circle(Vector(self.arena.x_len + bcirc_r,
                                          self.arena.goal_y_high + bcirc_r),
                                   bcirc_r),
                            # Upper left wall
                            Wall_Vert_Right(0, 0,
                                self.arena.goal_y_low),
                            # Lower left wall
                            Wall_Vert_Right(0,
                                self.arena.goal_y_high,
                                self.arena.y_len),
                            # Left goal top wall
                            Wall_Horz_Down(- 2*self.puck.radius - self.arena.border_width,
                                           0, self.arena.goal_y_low),
                            # Left goal bottom wall
                            Wall_Horz_Up(- 2*self.puck.radius - self.arena.border_width,
                                           0, self.arena.goal_y_high),
                            # Left goal top corner
                            Circle(Vector(-bcirc_r,
                                          self.arena.goal_y_low - bcirc_r),
                                   bcirc_r),
                            # Left goal bottom corner
                            Circle(Vector(-bcirc_r,
                                          self.arena.goal_y_high + bcirc_r),
                                   bcirc_r),
                            # Top wall
                            Wall_Horz_Down_Inf(0),
                            # Bottom wall
                            Wall_Horz_Up_Inf(self.arena.y_len),
                            self.paddle_1,
                            self.paddle_2] 
        # Objects that must be drawn every cycle 
        self.drawables = [self.puck, self.paddle_1, self.paddle_2]

    def draw(self):
        self.arena.screen.fill((0, 0, 0))
        self.arena.draw()

        for drawable in self.drawables:
            drawable.draw(self.arena)

    def update_score(self, goal):
        (left_score, right_score) = self.score
        if goal < 0:
            left_score = left_score + 1
        elif goal > 0:
            right_score = right_score + 1
        self.score = (left_score, right_score)

    def check_win(self):
        (left_score, right_score) = self.score
        if left_score >= self.win_score:
            return -1
        if right_score >= self.win_score:
            return 1
        return None

    def reset(self):
        self.puck.reset()
        self.score = (0,0) 

def mm_to_pix(mm):
    return int(mm * pix_per_mm)

def pix_to_mm(pix):
    return pix / pix_per_mm

# Run by separate thread to update to update location
def paddle_locator(paddle_lock):
    with open(FIFO, mode='rb') as fifo:
        data = fifo.read(4)
        print(data)
        print(type(data))
        num = int.from_bytes(data, byteorder="little")
        n = len(data);
        print("data length is " + str(n));
        print("Received: " + str(num));
        print(a)

def game_run():
    
    game = Game()

    game_running = True

    paddle_lock = threading.Lock()
    input_thread = threading.Thread(target=paddle_locator, args=(paddle_lock,))
    input_thread.daemon = True
    input_thread.start()

    while game_running:

        game.paddle_1.velocity = Vector(0,0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEMOTION:
                game.paddle_1.start_move(event.pos, game.arena, game.puck) 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_running = False
                if event.key == pygame.K_r:
                    # Reset game 
                    game.reset()

        game.puck.move(game.collidables)

        game.paddle_1.end_move(game.arena, game.puck)

        game.draw()

        game.clock.tick(clock_freq)
        pygame.display.flip()

        # Compute goals
        goal = game.puck.goal(game.arena)
        if goal:
            # Goal scored
            game.update_score(goal)
            print(game.score)

            winner = game.check_win()

            # Wait and reset puck
            for i in range(0, 30):
                game.clock.tick(clock_freq)

            if winner:
                if winner < 0:
                    print("Left wins!!!")
                elif winner > 0: 
                    print("Right wins!!!")
                game.reset()
            else:
                game.puck.reset()

clock = pygame.time.Clock()

game_run()
