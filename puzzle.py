import random
from typing import List, Tuple

class PuzzleGenerator:
    def __init__(self):
        self.size = 9
        self.box_size = 3

    def generate_puzzle(self, difficulty_config: dict) -> Tuple[List[List[int]], List[List[int]]]:
        if 'custom_puzzle' in difficulty_config:
            return difficulty_config['custom_puzzle'], difficulty_config['custom_solution']

        solution = self._generate_complete_solution()
        puzzle = [row[:] for row in solution]
        self._remove_numbers(puzzle, difficulty_config['cells_removed'])
        return puzzle, solution

    def _generate_complete_solution(self) -> List[List[int]]:
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        for box in range(0, self.size, self.box_size):
            self._fill_diagonal_box(grid, box, box)
        
        self._solve_grid(grid)
        return grid

    def _fill_diagonal_box(self, grid: List[List[int]], row: int, col: int):
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)
        for i in range(self.box_size):
            for j in range(self.box_size):
                grid[row + i][col + j] = nums.pop()

    def _solve_grid(self, grid: List[List[int]]) -> bool:
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 0:
                    for num in random.sample(range(1, self.size + 1), self.size):
                        if self._is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self._solve_grid(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    def _is_valid(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        if num in grid[row]:
            return False

        if num in [grid[i][col] for i in range(self.size)]:
            return False

        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if grid[box_row + i][box_col + j] == num:
                    return False
        return True

    def _remove_numbers(self, grid: List[List[int]], cells_to_remove: int):
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        
        removed = 0
        for row, col in cells:
            if removed >= cells_to_remove:
                break
                
            backup = grid[row][col]
            grid[row][col] = 0
            
            temp_grid = [r[:] for r in grid]
            if not self._solve_grid(temp_grid):
                grid[row][col] = backup
            else:
                removed += 1