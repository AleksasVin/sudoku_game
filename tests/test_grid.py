import unittest
import pygame
import numpy as np
from grid import Grid
from settings import GameSettings


class TestGrid(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.settings = GameSettings()
        self.solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.puzzle = [row.copy() for row in self.solution]
        # Remove some numbers
        self.puzzle[0][1] = 0
        self.puzzle[3][8] = 0
        self.grid = Grid(self.puzzle, self.solution)

    def test_grid_initialization(self):
        self.assertEqual(len(self.grid._cells), 9)
        self.assertEqual(len(self.grid._cells[0]), 9)
        self.assertFalse(self.grid._victory)

    def test_cell_selection(self):
        self.grid.select_cell(2, 3)
        self.assertTrue(self.grid._cells[2][3].is_selected)
        self.assertFalse(self.grid._cells[0][0].is_selected)

    def test_value_setting(self):
        self.grid.select_cell(0, 1)  # Empty cell at (0,1)
        self.assertEqual(self.grid._cells[0][1].value, 0)

        self.grid.set_value(3)
        self.assertEqual(self.grid._cells[0][1].value, 3)
        self.assertTrue(self.grid._cells[0][1]._is_correct)

        # Set incorrect value
        self.grid.set_value(9)
        self.assertEqual(self.grid._cells[0][1].value, 9)
        self.assertFalse(self.grid._cells[0][1]._is_correct)

    def test_victory_condition(self):
        # Fill all empty cells with correct values
        self.grid.select_cell(0, 1)
        self.grid.set_value(3)  # Correct
        self.grid.select_cell(3, 8)
        self.grid.set_value(3)  # Correct

        self.assertTrue(self.grid.victory)

    def test_invalid_move(self):
        self.grid.select_cell(0, 1)
        self.grid.set_value(9)  # Invalid (9 already in row)
        self.assertFalse(self.grid._cells[0][1]._is_correct)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()