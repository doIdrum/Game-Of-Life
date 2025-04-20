import numpy as np
import pygame as pg

import sys

WINDOW_SIZE = (1920, 1080) 
RES = 1
ROWS, COLS = WINDOW_SIZE[0] // RES, WINDOW_SIZE[1] // RES

shifts = [(1, 0), (1, 1), (1, -1), (0, 1), 
          (0, -1), (-1, 1), (-1, -1), (-1, 0)]

def init():
    pg.init()

    win = pg.display.set_mode(WINDOW_SIZE)
    clock = pg.time.Clock()
    return win, clock

def gen_randomize_grid(size, prob_alive):
    return np.random.choice([0, 1], size=size, p=[1 - prob_alive, prob_alive]).astype(np.uint8)

def draw_cells(grid, surf):
    rgb_grid = np.stack([grid * 200] * 3, axis=-1)
    surface = pg.surfarray.make_surface(rgb_grid)
    surface = pg.transform.scale(surface, WINDOW_SIZE)

    surf.blit(surface, (0, 0))

def count_neighbours(grid):
    return sum(np.roll(np.roll(grid, dx, axis=0), dy, axis=1) 
               for dx, dy in shifts)

def apply_rules(grid, next_gen):
    neighbours = count_neighbours(grid)

    alive = (grid == 1) & ((neighbours < 2) | (neighbours > 3))
    dead = (grid == 0) & (neighbours == 3)
    survive = (grid == 1) & ((neighbours == 2) | (neighbours == 3))

    next_gen[alive] = 0
    next_gen[dead] = 1 
    next_gen[survive] = 1

    return next_gen

def draw():
    win, clock = init()

    interval = 50
    update_grid = pg.USEREVENT
    pg.time.set_timer(update_grid, interval)

    grid = gen_randomize_grid((ROWS, COLS), 0.1)
    next_gen = np.zeros(grid.shape, dtype=np.uint8) 

    while True:
        pg.display.set_caption(f'FPS: {round(clock.get_fps())} iNTERVAL: {interval}')

        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if e.type == update_grid:
                grid = apply_rules(grid, next_gen)
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    grid = gen_randomize_grid((ROWS, COLS), np.random.uniform(0.1, 0.5))

        draw_cells(grid, win)

        clock.tick()
        pg.display.flip()
        
if __name__ == '__main__':
    draw()
