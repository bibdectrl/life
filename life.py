import sys
from random import random
import argparse
import pygame

DEAD = 0
ALIVE = 1

class LifeBoard:
    def __init__(self, x, y, alive_percent = .05):
        self.width = x
        self.height = y
        self.alive_percent = alive_percent
        self.cells = [[self.cell_contents() for i in range(y)] for j in range(x)]
        pygame.init()
        self.screen = pygame.display.set_mode((x * CELL_SIZE, y * CELL_SIZE))
        self.clock = pygame.time.Clock()
    def __str__(self):
        string = ""
        for line in self.cells:
            string +=  str(line) + "\n"
        return string

    def restart(self):
        self.cells = [[self.cell_contents() for i in range(self.height)] for j in range(self.width)]

    def cell_contents(self):
        num = random()
        if num <= self.alive_percent:
            return ALIVE
        else:
            return DEAD

    def next_step(self):
        new_cells = [[0 for i in range(self.height)] for j in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                neighbours = \
                self.cells[(x + 1) % self.width][y] \
                + self.cells[(x + 1) % self.width][(y + 1) % self.height] \
                + self.cells[x][(y + 1) % self.height] \
                + self.cells[(x - 1) % self.width][(y + 1) % self.height] \
                + self.cells[(x - 1) % self.width][y] \
                + self.cells[(x + 1) % self.width][(y - 1) % self.height] \
                + self.cells[(x - 1) % self.width][(y - 1) % self.height] \
                + self.cells[x][(y - 1) % self.height]
                if self.cells[x][y] == 0:
                    if neighbours == 3:
                        new_cells[x][y] = 1
                if self.cells[x][y] == 1:
                    if neighbours == 2 or neighbours == 3:
                        new_cells[x][y] = 1
        self.cells = new_cells
        
    def main(self):
        while True:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill((0, 0, 0))
            for x in range(self.width):
                for y in range(self.height):
                    if self.cells[x][y] == ALIVE:
                        pygame.draw.rect(self.screen, (255, 255, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            self.next_step()
 
parser = argparse.ArgumentParser()
parser.add_argument("--cellsize", "-c", type=int, default=5, help="the size of a cell")
parser.add_argument("--percent_living", "-p", type=float, default=0.05, help="the percentage of living starting cells")
parser.add_argument("--height", "-y", type=int, default=64, help="the height of the grid")
parser.add_argument("--width", "-x", type=int, default=48, help="the width of the grid")

args = parser.parse_args()

CELL_SIZE = args.cellsize

a = LifeBoard(args.height, args.width, args.percent_living)
a.main()     
