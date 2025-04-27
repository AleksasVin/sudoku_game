import unittest
import pygame
from grid import Cell, DrawableCell
from settings import GameSettings


class TestCell(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.settings = GameSettings()
        self.cell = Cell(5, 0, 0)
        self.drawable_cell = DrawableCell(5, 0, 0, 5)

    def test_cell_initialization(self):
        self.assertEqual(self.cell.value, 5)
        self.assertEqual(self.cell._row, 0)
        self.assertEqual(self.cell._col, 0)
        self.assertTrue(self.cell._is_initial)

    def test_cell_value_setter(self):
        empty_cell = Cell(0, 1, 1)
        empty_cell.value = 3
        self.assertEqual(empty_cell.value, 3)
        self.cell.value = 7
        self.assertEqual(self.cell.value, 5)

    def test_drawable_cell_validation(self):

        grid = [[DrawableCell(0, r, c, 0) for c in range(9)] for r in range(9)]


        test_cell = grid[0][0]
        self.assertTrue(test_cell.is_valid(1, grid))  # Should be valid


        grid[0][1].value = 1
        self.assertFalse(test_cell.is_valid(1, grid))


        grid[1][0].value = 2
        self.assertFalse(test_cell.is_valid(2, grid))


        grid[1][1].value = 3
        self.assertFalse(test_cell.is_valid(3, grid))

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()