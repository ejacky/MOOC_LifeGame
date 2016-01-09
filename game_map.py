# -*- coding: utf-8 -*-
#
# @author jackyzhang

import random
import sys


class GameMap(object):
    """
    The game map, contains a lot of cells.

    Each cell has a value, 0 means it is a dead/empty cell, 1 means it is a live cell,
    and -1 means it is a wall cell.

    Attributes:
        size: a tuple shows the map's rows and columns
        cells: a grid contains all the cells
    """
    
    MAX_MAP_SIZE = 100
    CELL_ALIVE = 1
    MAX_CELL_VALUE = 1
    MIN_CELL_VALUE = 0

    def __init__(self, rows, cols):
        """Inits GameMap with row and column count."""
        assert isinstance(rows, int)
        assert isinstance(cols, int)
        assert 0 < rows <= self.MAX_MAP_SIZE
        assert 0 < cols <= self.MAX_MAP_SIZE
        self.size = (rows, cols, )
        self.cells = [[0 for col in range(cols)] for row in range(rows)]

    @property
    def rows(self):
        return self.size[1]

    @property
    def cols(self):
        return self.size[0]

    def reset(self, possibility_live=0.5, possibility_wall=0.1):
        """Reset the map with random data.

        Args:
            possibility_live: possibility of live cell
            possibility_wall: to be added, means possibility of wall cell, represented with number -1
        """
        for row in self.cells:
            for col_num in range(self.cols):
                row[col_num] = 1 if random.random() < possibility_live else 0

    def set(self, row, col, val):
        """Set specific cell in the map."""
        assert self.MIN_CELL_VALUE <= val <= self.MAX_CELL_VALUE
        self.cells[col][row] = val
        return self

    def get_neighbor_count(self, row, col):
        """Get count of neighbors in specific cell.

        Args:
            row: row number
            col: column number

        Returns:
            Count of live neighbor cells
        """
        DIRECTION = {
            "up": (-1, 0),
            "up_up": (-2, 0),
            "down": (1, 0),
            "down_down": (2, 0),
            "left": (0, -1),
            "left_left": (0, -2),
            "right": (0, 1),
            "right_right": (0, 2),
        }
        counter = 0
        for dire in DIRECTION:
            trow = (row + DIRECTION[dire][0]) % self.rows
            tcol = (col + DIRECTION[dire][1]) % self.cols
            if self.cells[trow][tcol] == GameMap.CELL_ALIVE:
                counter += 1
        return counter

    def get_neighbor_count_map(self):
        """Get count of neighbors of every cell in the map.

        Returns:
            A grid contains every cell's neighbor count.
        """
        return [[self.get_neighbor_count(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def print_map(self, cell_maps=None, sep=' ', fd=sys.stdout):
        """Print the map to target file descriptor

        Args:
            cell_maps: mapping from cell value to a string that will be displayed.
            sep: separator between cells of the same row.
            fd: file descriptor, default standard output
        """
        if not cell_maps:
            cell_maps = {
                -1: 'X',
                0: '0',
                1: '1',
            }
        assert isinstance(cell_maps, list) or isinstance(cell_maps, dict)
        assert isinstance(sep, str)
        for row in self.cells:
            print(sep.join(map(lambda cell: cell_maps[cell], row)), file=fd)
