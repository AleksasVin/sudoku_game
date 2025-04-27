import unittest
from puzzle import PuzzleGenerator

class TestPuzzleGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PuzzleGenerator()

    def test_puzzle_generation(self):
        config = {'grid_size': 9, 'cells_removed': 40, 'box_height': 3, 'box_width': 3}
        puzzle, solution = self.generator.generate_puzzle(config)
        
        # Verify dimensions
        self.assertEqual(len(puzzle), 9)
        self.assertEqual(len(puzzle[0]), 9)
        

        for row in solution:
            self.assertNotIn(0, row)
        

        empty_count = sum(row.count(0) for row in puzzle)
        self.assertGreater(empty_count, 0)

    def test_custom_puzzle_loading(self):
        custom_config = {
            'grid_size': 9,
            'cells_removed': 4,
            'box_height': 3,
            'box_width': 3,
            'custom_puzzle': [
                [5,0,4,6,7,8,9,1,2],
                [6,7,2,1,9,5,3,4,8],
                [0,9,8,3,4,2,5,6,7],
                [8,5,9,7,6,1,4,2,3],
                [4,2,6,8,5,3,7,9,1],
                [7,1,3,9,2,4,8,5,6],
                [9,6,1,5,3,7,2,8,4],
                [2,8,7,4,1,9,6,3,5],
                [3,4,5,2,8,6,1,7,9]
            ],
            'custom_solution': [
                [5,3,4,6,7,8,9,1,2],
                [6,7,2,1,9,5,3,4,8],
                [1,9,8,3,4,2,5,6,7],
                [8,5,9,7,6,1,4,2,3],
                [4,2,6,8,5,3,7,9,1],
                [7,1,3,9,2,4,8,5,6],
                [9,6,1,5,3,7,2,8,4],
                [2,8,7,4,1,9,6,3,5],
                [3,4,5,2,8,6,1,7,9]
            ]
        }
        
        puzzle, solution = self.generator.generate_puzzle(custom_config)
        self.assertEqual(puzzle, custom_config['custom_puzzle'])
        self.assertEqual(solution, custom_config['custom_solution'])

    def test_solution_validity(self):
        config = {'grid_size': 9, 'cells_removed': 10, 'box_height': 3, 'box_width': 3}
        puzzle, solution = self.generator.generate_puzzle(config)
        
        # Verify rows in solution
        for row in solution:
            self.assertEqual(len(set(row)), 9)
            self.assertEqual(min(row), 1)
            self.assertEqual(max(row), 9)
        
        # Verify columns in solution
        for col in zip(*solution):
            self.assertEqual(len(set(col)), 9)

if __name__ == '__main__':
    unittest.main()