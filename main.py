import os
import pygame
from random import randint, uniform
from math import sqrt
import colorsys
import inputs

# ----------------------------------------------------------------------------------------------------------------------
# CONSTANTS

FPS = 60

# ----------------------------------------------------------------------------------------------------------------------
# PYGAME'S INITIATION

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
infoObject = pygame.display.Info()

full_screen = inputs.full_screen_input
if full_screen:
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
else:
    WIDTH, HEIGHT = inputs.WIDTH_input, inputs.HEIGHT_input
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ----------------------------------------------------------------------------------------------------------------------
# INPUTS
# ----------------------------------------------------------------------------------------------------------------------
# Velocity of moving particles

velocity = inputs.velocity_input

# ----------------------------------------------------------------------------------------------------------------------
# Max distance when connection between particles disappear

max_distance = inputs.max_distance_input

# ----------------------------------------------------------------------------------------------------------------------
# SURFACE DISPLAY

display_surface = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# ----------------------------------------------------------------------------------------------------------------------
# PLEXUS EFFECT CREATION

class Circle:
    def __init__(self, quantity):
        self.quantity = quantity
        self.circles = []
        self.velocity = [velocity, velocity]
        self.create_circles()

    def create_circles(self):
        for _ in range(self.quantity):
            self.x = randint(0, WIDTH)
            self.y = randint(0, HEIGHT)
            self.velocity_x = uniform(-self.velocity[0], self.velocity[0])
            self.velocity_y = uniform(-self.velocity[1], self.velocity[1])
            self.position = (self.x, self.y, self.velocity_x, self.velocity_y)
            self.circles.append(self.position)

    def update(self):
        self.circles_moved = []

        for i in self.circles:
            self.x = i[0]
            self.y = i[1]

            self.velocity_x = i[2]
            self.velocity_y = i[3]

            self.x += self.velocity_x
            self.y += self.velocity_y

            if self.x >= WIDTH or self.x <= 0:
                self.velocity_x *= -1

            if self.y >= HEIGHT or self.y <= 0:
                self.velocity_y *= -1

            self.position = (self.x, self.y, self.velocity_x, self.velocity_y)
            self.circles_moved.append(self.position)
            self.circles = self.circles_moved

    def connect_circles(self):
        self.lines = []
        for p0 in range(self.quantity - 1):
            for p1 in range(p0 + 1, self.quantity):
                self.lines.append([self.circles[p0][:2], self.circles[p1][:2]])

        return self.lines


# COLORS
# ----------------------------------------------------------------------------------------------------------------------
# Changing with distance

def color(distance, max_distance, h, s, v):
    h_max, s_max, v_max = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))
    r = int((max_distance - distance) * h_max / max_distance)
    g = int((max_distance - distance) * s_max / max_distance)
    b = int((max_distance - distance) * v_max / max_distance)
    return r, b, b


# ----------------------------------------------------------------------------------------------------------------------
# Using HSV color space

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


# ----------------------------------------------------------------------------------------------------------------------
# OBJECT INITIATION

circles = Circle(100)  # change number of particles


# ----------------------------------------------------------------------------------------------------------------------
# MAIN FUNCTION

def main():
    hue = 0

    paused = False
    running = True
    while running:
        clock.tick(FPS)
        pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))

        screen.fill((0, 0, 0))

        # Get the color in RGB
        r, g, b = hsv2rgb(hue, 1, 1)

        # Draw lines
        for i in circles.connect_circles():
            start_position = i[0]
            end_position = i[1]
            distance = sqrt((start_position[0] - end_position[0]) ** 2 + (start_position[1] - end_position[1]) ** 2)

            if distance < max_distance:
                r, g, b = color(distance, max_distance, hue, 1, 1)
                pygame.draw.line(screen, (r, g, b), start_pos=i[0], end_pos=i[1], width=2)

        # Draw circles
        for i in circles.circles:
            pygame.draw.circle(screen, (r, g, b), center=i[:2], radius=3)

        # Increase hue for different color
        hue += 0.001  # increase for faster color change
        if hue >= 1.0:
            hue = 0

        print(hue)

        circles.update()

        if not paused:
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused


if __name__ == "__main__":
    main()
