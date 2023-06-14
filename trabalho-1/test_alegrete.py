import unittest
import alegrete
import numpy as np


class TestAlegrete(unittest.TestCase):

    def test_compute_mse(self):
        data = np.genfromtxt('data/alegrete.csv', delimiter=',')
        mse = alegrete.compute_mse(0, 0, data)
        self.assertAlmostEqual(66.78348986604624, mse, 8)  # comparacao de floats com 9 casas de precisao

    def test_step_gradient(self):
        # dataset ficticio
        data = np.array([
            [1, 3],
            [2, 4],
            [3, 4],
            [4, 2]
        ])

        new_b, new_w = alegrete.step_gradient(1, 1, data, alpha=0.1)
        # comparacao de floats com precisao de 11 casas
        self.assertAlmostEqual(0.95, new_b, 11)
        self.assertAlmostEqual(0.55, new_w, 11)


if __name__ == '__main__':
    unittest.main()
