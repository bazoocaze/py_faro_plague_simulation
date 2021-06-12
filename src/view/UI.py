import pygame

from src.view.Surface import Surface


class UI:
    def __init__(self, width=640, height=480):
        self._window = None
        self._finished = False
        self._width = width
        self._height = height
        self._initialize()

    def process(self, context):
        if self._finished:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                context.exit_simulation()
                self._finished = True

    def draw(self, context):
        if self._finished:
            return

        pygame.display.flip()

    def _initialize(self):
        pygame.init()
        self._window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Faro Plague Simulation: red=Plague, blue=EDF")

    def pygame_run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()

    def terminate(self):
        self._finished = True
        pygame.quit()

    def world_surface(self, virtual_width, virtual_height):
        return Surface(virtual_width, virtual_height, self._window)
