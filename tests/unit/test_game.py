"""
Tests for the game class
"""

import unittest
import nash
import numpy as np


class TestGame(unittest.TestCase):
    """
    Tests for the game class
    """
    def test_bi_matrix_init(self):
        """Test that can create a bi matrix game"""
        A = np.array([[1, 2], [2, 1]])
        B = np.array([[2, 1], [1, 2]])
        g = nash.Game(A, B)
        self.assertEqual(g.payoff_matrices, (A, B))
        self.assertFalse(g.zero_sum)

        # Can also init with lists
        A = [[1, 2], [2, 1]]
        B = [[2, 1], [1, 2]]
        g = nash.Game(A, B)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], np.asarray(A)))
        self.assertTrue(np.array_equal(g.payoff_matrices[1], np.asarray(B)))
        self.assertFalse(g.zero_sum)

    def test_bi_matrix_repr(self):
        """Test that can create a bi matrix game"""
        A = np.array([[1, 2], [2, 1]])
        B = np.array([[2, 1], [1, 2]])
        g = nash.Game(A, B)
        string_repr = """Bi matrix game with payoff matrices:

Row player:
[[1 2]
 [2 1]]

Column player:
[[2 1]
 [1 2]]"""
        self.assertEqual(g.__repr__(), string_repr)

    def test_zero_sum_game_init(self):
        """Test that can create a zero sum game"""
        A = np.array([[1, 2], [2, 1]])
        g = nash.Game(A)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], A))
        self.assertTrue(np.array_equal(g.payoff_matrices[0],
                                       -g.payoff_matrices[1]))
        self.assertTrue(g.zero_sum)

        # Can also init with lists
        A = [[1, 2], [2, 1]]
        g = nash.Game(A)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], np.asarray(A)))
        self.assertTrue(np.array_equal(g.payoff_matrices[0],
                                       -g.payoff_matrices[1]))
        self.assertTrue(g.zero_sum)

    def test_zero_sum_repr(self):
        """Test that can create a bi matrix game"""
        A = np.array([[1, -1], [-1, 1]])
        g = nash.Game(A)
        string_repr = """Zero sum game with payoff matrices:

Row player:
[[ 1 -1]
 [-1  1]]

Column player:
[[-1  1]
 [ 1 -1]]"""
        self.assertEqual(g.__repr__(), string_repr)

    def test_zero_sum_property_from_bi_matrix(self):
        """Test that can create a zero sum game"""
        A = np.array([[1, 2], [2, 1]])
        B = -A
        g = nash.Game(A, B)
        self.assertTrue(g.zero_sum)

    def test_equilibria_for_bi_matrix(self):
        """Test for the equilibria calculation"""
        A = np.array([[160, 205, 44],
                      [175, 180, 45],
                      [201, 204, 50],
                      [120, 207, 49]])
        B = np.array([[2, 2, 2],
                      [1, 0, 0],
                      [3, 4, 1],
                      [4, 1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([0, 0, 3/4, 1/4]),
                                np.array([1/28, 27/28, 0]))]
        for obtained, expected in zip(g.equilibria(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(np.array_equal(s1, s2),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([1, 0]), np.array([1, 0])),
                               (np.array([0, 1]), np.array([0, 1])),
                               (np.array([1/2, 1/2]), np.array([1/2, 1/2]))]
        for obtained, expected in zip(g.equilibria(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(np.array_equal(s1, s2),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([1, 0]), np.array([1, 0])),
                               (np.array([0, 1]), np.array([0, 1])),
                               (np.array([1/3, 2/3]), np.array([1/3, 2/3]))]
        for obtained, expected in zip(g.equilibria(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(np.array_equal(s1, s2),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

    def test_potential_supports(self):
        """Test for the enumeration of potential supports"""
        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        g = nash.Game(A, B)
        self.assertEqual(list(g.potential_support_pairs()), [((0,), (0,)),
                                                             ((0,), (1,)),
                                                             ((1,), (0,)),
                                                             ((1,), (1,)),
                                                             ((0, 1), (0, 1))])

        A = np.array([[1, 0, 2], [-2, 3, 9]])
        B = np.array([[3, 2, 1], [-1, 0, 2]])
        g = nash.Game(A, B)
        self.assertEqual(list(g.potential_support_pairs()), [((0,), (0,)),
                                                             ((0,), (1,)),
                                                             ((0,), (2,)),
                                                             ((1,), (0,)),
                                                             ((1,), (1,)),
                                                             ((1,), (2,)),
                                                             ((0, 1), (0, 1)),
                                                             ((0, 1), (0, 2)),
                                                             ((0, 1), (1, 2))])

        A = np.array([[1, 0], [-2, 3], [2, 1]])
        B = np.array([[3, 2], [-1, 0], [5, 2]])
        g = nash.Game(B, A)
        self.assertEqual(list(g.potential_support_pairs()), [((0,), (0,)),
                                                             ((0,), (1,)),
                                                             ((1,), (0,)),
                                                             ((1,), (1,)),
                                                             ((2,), (0,)),
                                                             ((2,), (1,)),
                                                             ((0, 1), (0, 1)),
                                                             ((0, 2), (0, 1)),
                                                             ((1, 2), (0, 1))])

    def test_indifference_strategies(self):
        """Test for the enumeration of potential supports"""
        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)
        expected_indifference = [(np.array([1, 0]), np.array([1, 0])),
                                 (np.array([1, 0]), np.array([0, 1])),
                                 (np.array([0, 1]), np.array([1, 0])),
                                 (np.array([0, 1]), np.array([0, 1])),
                                 (np.array([1/3, 2/3]), np.array([1/3, 2/3]))]
        obtained_indifference = [out[:2] for out in g.indifference_strategies()]
        self.assertEqual(len(obtained_indifference), len(expected_indifference))
        for obtained, expected in zip(obtained_indifference,
                                      expected_indifference):
            self.assertTrue(np.array_equal(obtained, expected),
                            msg="obtained: {} !=expected: {}".format(obtained,
                                                                     expected))

    def test_obey_support(self):
        """Test for obey support"""
        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)
        self.assertFalse(g.obey_support(False, np.array([0, 1])))
        self.assertFalse(g.obey_support(np.array([1, 0]), np.array([0, 1])))
        self.assertFalse(g.obey_support(np.array([0, .5]), np.array([0])))
        self.assertFalse(g.obey_support(np.array([.5, 0]), np.array([1])))

        self.assertTrue(g.obey_support(np.array([1, 0]), np.array([0])))
        self.assertTrue(g.obey_support(np.array([0, .5]), np.array([1])))
        self.assertTrue(g.obey_support(np.array([.5, 0]), np.array([0])))
        self.assertTrue(g.obey_support(np.array([.5, .5]), np.array([0, 1])))

    def test_is_ne(self):
        """Test if is ne"""
        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)

        strategy_pair = np.array([1, 0]), np.array([1, 0])
        support_pair = [0], [0]
        self.assertTrue(g.is_ne(strategy_pair, support_pair))

        strategy_pair = np.array([1/3, 2/3]), np.array([1/3, 2/3])
        support_pair = [0, 1], [0, 1]
        self.assertTrue(g.is_ne(strategy_pair, support_pair))

        strategy_pair = np.array([0, 1]), np.array([1, 0])
        support_pair = [1], [0]
        self.assertFalse(g.is_ne(strategy_pair, support_pair))

        strategy_pair = np.array([1, 0]), np.array([0, 1])
        support_pair = [0], [1]
        self.assertFalse(g.is_ne(strategy_pair, support_pair))

        A = np.array([[1, -1], [-1, 1]])
        g = nash.Game(A)
        strategy_pair = np.array([1 / 2, 1 / 2]), np.array([1 / 2, 1 / 2])
        support_pair = [0, 1], [0, 1]
        self.assertTrue(g.is_ne(strategy_pair, support_pair))

        A = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
        g = nash.Game(A)
        strategy_pair = (np.array([1 / 3, 1 / 3, 1 / 3]),
                         np.array([1 / 3, 1 / 3, 1 / 3]))
        support_pair = [0, 1, 2], [0, 1, 2]
        self.assertTrue(g.is_ne(strategy_pair, support_pair))

        strategy_pair = (np.array([1, 0, 0]),
                         np.array([1, 0, 0]))
        support_pair = [0], [0]
        self.assertFalse(g.is_ne(strategy_pair, support_pair))

        A = np.array([[160, 205, 44],
                      [175, 180, 45],
                      [201, 204, 50],
                      [120, 207, 49]])
        B = np.array([[2, 2, 2],
                      [1, 0, 0],
                      [3, 4, 1],
                      [4, 1, 2]])
        g = nash.Game(A, B)
        self.assertTrue(g.is_ne((np.array((0, 0, 3/4, 1/4)),
                                 np.array((1/28, 27/28, 0))),
                                (np.array([2, 3]), np.array([0, 1]))))

    def test_solve_indifference(self):
        """Test solve indifference"""
        A = np.array([[0, 1, -1], [1, 0, 1], [-1, 1, 0]])
        g = nash.Game(A)

        rows = [0, 1]
        columns = [0, 1]
        self.assertTrue(np.array_equal(g.solve_indifference(A, rows, columns),
                                       np.array([0.5,  0.5,  0.])))

        rows = [1, 2]
        columns = [0, 1]
        self.assertTrue(all(np.isclose(g.solve_indifference(A, rows, columns),
                                       np.array([1/3,  2/3,  0.])
                                       )))

        rows = [0, 2]
        columns = [0, 1]
        self.assertTrue(np.array_equal(g.solve_indifference(A, rows, columns),
                                       np.array([0.,  1.0,  0.])))

        rows = [0, 1, 2]
        columns = [0, 1, 2]
        self.assertTrue(all(np.isclose(g.solve_indifference(A, rows, columns),
                                       np.array([0.2,  0.6,  0.2])
                                       )))


class TestUtils(unittest.TestCase):
    def test_powerset(self):
        n = 2
        powerset = list(nash.powerset(n))
        self.assertEqual(powerset, [(), (0,), (1,), (0, 1)])

        n = 3
        powerset = list(nash.powerset(n))
        self.assertEqual(powerset, [(), (0,), (1,), (2,),
                                    (0, 1), (0, 2), (1, 2),
                                    (0, 1, 2)])
