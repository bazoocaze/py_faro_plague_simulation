import pygame


class Surface:
    def __init__(self, width, height, target_surface):
        self.target_surface = target_surface
        self.draw_surface = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self._pixels = [[0 for x in range(width)] for y in range(height)]

    def process(self, context):
        pass

    def draw(self, context):
        pixel_array = pygame.PixelArray(self.draw_surface)
        for y in range(self.height):
            for x in range(self.width):
                pixel_array[x, y] = self._pixels[y][x]
        pixel_array.close()

        # target = self.target_surface.subsurface(pygame.Rect(0, 0, self.width * 4, self.height * 4))
        # pygame.transform.scale(self.draw_surface, (self.width * 4, self.height * 4), target)

        pygame.transform.scale(self.draw_surface, (self.target_surface.get_width(), self.target_surface.get_height()),
                               self.target_surface)

    def put(self, x, y, color):
        self._pixels[y][x] = color
