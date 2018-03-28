import pygame

# Source: https://math.stackexchange.com/questions/913350/how-to-find-the-intersection-point-of-two-moving-circles

# Pixels per millimeter
pix_per_mm = .3 

class Vector:                                                                                    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, vx):
        return Vector(self.x + vx.x, self.y + vx.y)

    def scale(self, scaler):
        return Vector(self.x * scaler, self.y * scaler)

    def flip_horz(self):
        return Vector(-self.x, self.y)

    def flip_vert(self):
        return Vector(self.x, -self.y)

    @staticmethod
    def sum(v1, v2):
        return Vector(v1.x + v2.x, v1.y + v2.y)

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
    def move(self, arena):

        # The current location in the move
        temp_loc = self.location
        # The current velocity in the move
        temp_vel = self.velocity

        # Fraction of the move left to do 
        move_left = 1

        while move_left > 0:
            # Possible new location
            pos_loc = temp_loc.add(temp_vel.scale(move_left))

            col_fr = ((arena.width - self.radius) - temp_loc.x) / (pos_loc.x - temp_loc.x)

            if col_fr < 1 and temp_vel.x > 0: 
                temp_loc = temp_loc.add(temp_vel.scale(move_left).scale(col_fr))
                temp_vel = temp_vel.flip_horz()
                move_left = move_left * (1 - col_fr)

            else:
                temp_loc = pos_loc
                move_left = 0

        self.location = temp_loc
        self.velocity = temp_vel

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

        self.arena = Arena(arena_width, arena_length)
        self.puck = Puck(Vector(50, 50), Vector(3, 3), 30)
        self.clock = pygame.time.Clock()

def mm_to_pix(mm):
    return int(mm * pix_per_mm)

def game_run():
    
    game = Game()

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        game.puck.move(game.arena)

        game.screen.fill((0, 0, 0))
        game.puck.draw(game.screen)
        
        game.clock.tick(60)
        pygame.display.flip()

clock = pygame.time.Clock()
    

game_run()
