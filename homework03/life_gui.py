import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = self.life.cols * cell_size, self.life.rows * cell_size
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols):
            pygame.draw.line(self.screen, pygame.Color("black"), (x * self.cell_size, 0),
                             (x * self.cell_size, self.life.rows * self.cell_size))
        for y in range(0, self.life.rows):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y * self.cell_size),
                             (self.life.cols * self.cell_size, y * self.cell_size))

    def draw_grid(self) -> None:
        y = 0
        for row in self.life.curr_generation:
            x = 0
            for el in row:
                if el:
                    color = 'green'
                else:
                    color = 'white'
                pygame.draw.rect(self.screen, pygame.Color(color),
                                 pygame.Rect(x, y, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size

    def colorize_cell(self, click_coords: (int, int)):
        j, i = click_coords[0] // self.cell_size, click_coords[1] // self.cell_size
        print(i,j)
        if self.life.curr_generation[i][j]:
            self.life.curr_generation[i][j] = 0
        else:
            self.life.curr_generation[i][j] = 1

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        playing= False
        self.draw_grid()
        self.draw_lines()
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not playing:
                    self.colorize_cell(pygame.mouse.get_pos())
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    playing = not playing
            if playing:
                self.life.step()
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()
life = GameOfLife((24, 80), max_generations=50)
ui = GUI(life)
ui.run()