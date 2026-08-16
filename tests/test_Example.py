import unittest
from mlips.Example import *

class exampleClassTest(unittest.TestCase):
    def test_construct(self):
        L = 8
        base = 2
        error = 0.1
        q = 2
        r = 3
        try:
            E = Example(L, base, error, q, r)
            E2 = Example(L, base + 1, error, q - 1, 2 * r)
        except Exception as e:
            self.fail("Correct construction of Example raised exception!")

    def test_wrong_construct(self):
        L = 8
        base = 2
        error = 0.1
        q = 2
        r = 3
        self.assertRaises(ValueError, Example, -1, base, error, q, r)
        self.assertRaises(ValueError, Example, L, base, error, -1, r)
        self.assertRaises(ValueError, Example, L, base, error, q, -3)
        self.assertRaises(ValueError, Example, L, 0.1, error, q, -3)

    def test_solve_format(self):
        L = 8
        base = 2
        error = 0.1
        q = 2
        r = 3
        E = Example(L, base, error, q, r)

        solve = E.solveParam([0., 0.], 1);
        self.assertTrue("QoI" in solve)
        self.assertTrue("Cost" in solve)
        
        solve = E.solveParam([-1., 0.5], 1);
        self.assertTrue("QoI" in solve)
        self.assertTrue("Cost" in solve)

    def test_solve_base_val(self):
        L = 8
        base = 2
        error = 0.1
        q = 2
        r = 3
        E = Example(L, base, error, q, r)

        solve = E.solveParam([0., 0.], -1);
        self.assertEqual(solve["QoI"], 0.0)
        self.assertEqual(solve["Cost"], 0.0)

        solve = E.solveParam([1., 0.5], -1);
        self.assertEqual(solve["QoI"], 0.0)
        self.assertEqual(solve["Cost"], 0.0)
        
    def test_solve_cost(self):
        L = 8
        base = 2
        error = 0.1
        q = 2
        r = 3
        E = Example(L, base, error, q, r)

        solve = E.solveParam([0., 0.], 0);
        cost0 = solve["Cost"]
        
        solve = E.solveParam([0., 0.], 1);
        cost1 = solve["Cost"]

        solve = E.solveParam([0., 0.], 2);
        cost2 = solve["Cost"]

        self.assertEqual(cost0, base**(r*0))
        self.assertEqual(cost1, base**(r*1))
        self.assertEqual(cost2, base**(r*2))

    def test_solve_zero_error(self):
        L = 8
        base = 2
        error = 0.
        q = 2
        r = 3
        E = Example(L, base, error, q, r)

        solve = E.solveParam([0., 0.], 0);
        qoi0 = solve["QoI"]
        
        solve = E.solveParam([0., 0.], 1);
        qoi1 = solve["QoI"]

        solve = E.solveParam([0., 0.], 2);
        qoi2 = solve["QoI"]

        self.assertEqual(qoi0, qoi1)
        self.assertEqual(qoi0, qoi2)


if __name__=='__main__':
    unittest.main()
