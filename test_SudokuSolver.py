import unittest
import json
from SudokuSolver import SudokuSolver

class TestSudokuSolver(unittest.TestCase):
    def setUp(self):
        with open('testingSudoku.json') as f:
            req = json.load(f)
        baseBoard = req['newboard']['grids'][0]['value']
        self.ss = SudokuSolver(baseBoard)
    
    def test_searchRow(self):
        self.assertEqual(self.ss.searchRow(3,[1]), [0,2,5,6,8])
        self.assertEqual(self.ss.searchRow(5,[4]), [1,3,4,6,8])
        self.assertEqual(self.ss.searchRow(8,[2]), [1,2,6,7,8])
        self.assertEqual(self.ss.searchRow(1,[1,4]), [0,1,2,3,6,8])
        self.assertRaises(ValueError, self.ss.searchRow, 10, [4])
        self.assertRaises(ValueError, self.ss.searchRow, 4, [0])
    
    def test_searchCol(self):
        self.assertEqual(self.ss.searchCol(3,[1]), [0,1,2,6,7])
        self.assertEqual(self.ss.searchCol(5,[4]), [0,3,4,6,8])
        self.assertEqual(self.ss.searchCol(8,[2]), [0,1,2,3,4,5,6,7,8])
        self.assertEqual(self.ss.searchCol(1,[2,5]), [0,1,2,5,7,8])
        self.assertRaises(ValueError, self.ss.searchCol, 10, [4])
        self.assertRaises(ValueError, self.ss.searchCol, 4, [0])
    
    def test_searchGrid(self):
        self.assertEqual(self.ss.searchGrid(4,1,[2]), [[3,2],[4,1],[5,1]])
        self.assertEqual(self.ss.searchGrid(5,4,[6]), [[3,5],[4,4],[4,5],[5,4]])
        self.assertEqual(self.ss.searchGrid(2,8,[1]), [[0,6],[0,8],[1,6],[1,7],[1,8],[2,8]])
        self.assertEqual(self.ss.searchGrid(4,1,[2,7]), [[3,2],[5,1]])
        self.assertRaises(ValueError, self.ss.searchGrid, 4, 10, [4])
        self.assertRaises(ValueError, self.ss.searchGrid, 10, 4, [4])
        self.assertRaises(ValueError, self.ss.searchGrid, 4, 4, [10])
    
    def test_singlesTest(self):
        pass
    
    def test_lineTest(self):
        pass

    def test_hiddenPairTest(self):
        pass

    def test_pairTest(self):
        pass

    def test_str(self):
        pass
    

if __name__ == "__main__":
    unittest.main()
