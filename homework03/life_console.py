import curses
import time
from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        curses.resize_term(self.life.rows + 2, self.life.cols + 2)
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        y = 1
        for line in self.life.curr_generation:
            newline = ""
            for e in line:
                if e:
                    newline += "*"
                else:
                    newline += " "
            screen.addstr(y, 1, newline)
            y += 1

    def run(self) -> None:
        while self.life.is_changing:
            screen = curses.initscr()
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
            time.sleep(0.5)
            #time.sleep(1)
            # PUT YOUR CODE HERE
        curses.endwin()
life = GameOfLife((24, 80), max_generations=50)
ui = Console(life)
ui.run()