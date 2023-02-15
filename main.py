import pygame
from threading import Thread
import random
import time


width = 700
height = 500
bcg_color = "black"
target_fps = 60

particles = []
active = True

attraction_table = {
    "red": {
        "red": 0,
        "orange": 0,
        "yellow": 0,
        "green": 0
    },
    "orange": {
        "red": 0,
        "orange": 0,
        "yellow": 0,
        "green": 0
    },
    "yellow": {
        "red": 0,
        "orange": 0,
        "yellow": 0,
        "green": 0
    },
    "green": {
        "red": 0,
        "orange": 0,
        "yellow": 0,
        "green": 0
    },
}


class Particle:
    def __init__(self, x, y, m, vx, vy, r, color):
        self.x = x
        self.y = y
        self.m = m
        self.vx = 10
        self.vy = vy
        self.r = r
        self.color = color


class Engine(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.active = True
        self.time = time.time()

    def run(self) -> None:
        print("engine running")
        while self.active:
            for particle in particles:
                particle.x += particle.vx * (time.time() - self.time)
                particle.y += particle.vy * (time.time() - self.time)

            self.time = time.time()

    def stop(self):
        self.active = False


class Renderer(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.active = True
        self.target_fps = target_fps
        self.clock = pygame.time.Clock()
        self.background_color = bcg_color
        pygame.display.set_caption("Particle sim")
        self.screen = pygame.display.set_mode((width, height))

    def run(self) -> None:
        print("renderer running")
        while self.active:
            self.screen.fill(self.background_color)

            for particle in particles:
                pygame.draw.circle(self.screen, particle.color, (particle.x, particle.y), particle.r, 0)

            pygame.display.flip()
            self.clock.tick(self.target_fps)

    def stop(self):
        print("renderer stopping")
        self.active = False


def create_particle(color):
    particles.append(Particle(random.randint(0, width - 5), random.randint(0, height - 5), 1, 0, 0, 5, color))


def setup():
    for color in attraction_table.keys():
        create_particle(color)


def stop():
    global active

    active = False
    renderer.stop()
    engine.stop()


if __name__ == '__main__':
    renderer = Renderer()
    engine = Engine()

    renderer.start()
    engine.start()

    setup()
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
