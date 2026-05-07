import unittest
from MLPoints import *

class mlmcSamplesTest(unittest.TestCase):
    def test_get_samples(self):
        try:
            S = mlmcSamples(2, 1.3, 0.1, 5)
            S2= mlmcSamples(2.5, 2, 0.8, 9)
        except Exception as e:
            self.fail("Correct usage of mlmcSamples raised exception!")

    def test_check_levels(self):
        S = mlmcSamples(2, 1.3, 0.1, 5)
        self.assertEqual(len(S),6)
        S2= mlmcSamples(2.5, 2, 0.8, 9)
        self.assertEqual(len(S2),10)

    def test_check_samples_decrease(self):
        S = mlmcSamples(2, 1.3, 0.1, 5)
        for s in range(len(S)-1):
            self.assertTrue(S[s]>S[s+1])

        S2 = mlmcSamples(4, .3, 0.8, 5)
        for s in range(len(S2)-1):
            self.assertTrue(S2[s]>S2[s+1])

    def test_samples_negative_input(self):
        self.assertRaises(ValueError, mlmcSamples, -1, 2.3, 0.5, 2)
        self.assertRaises(ValueError, mlmcSamples, 1., -2.3, 0.5, 2)
        self.assertRaises(ValueError, mlmcSamples, 1., 2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcSamples, 1., 2.3, 1.5, -2)
        self.assertRaises(ValueError, mlmcSamples, 1., -2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcSamples, -1., 2.3, 1.5, -2)
        self.assertRaises(ValueError, mlmcSamples, -1., 2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcSamples, 1., -2.3, 1.5, -2)

    def test_samples_gamma_larger_one(self):
        self.assertRaises(ValueError, mlmcSamples, 1, 2.3, 2, 2)
        self.assertRaises(ValueError, mlmcSamples, 1., 2.3, 1.5, 2)

    def test_samples_float_level(self):
        self.assertRaises(TypeError, mlmcSamples, 1, 2.3, 0.9, 2.1)
        self.assertRaises(TypeError, mlmcSamples, 1., 2.3, .5, 2.01)


class mlmcAdSamplesTest(unittest.TestCase):
    def test_get_samples(self):
        try:
            S = mlmcAdSamples(2, 1.3, 0.1, 5)
            S2= mlmcAdSamples(2.5, 2, 0.8, 9)
        except Exception as e:
            self.fail("Correct usage of mlmcAdSamples raised exception!")

    def test_check_levels(self):
        S = mlmcAdSamples(2, 1.3, 0.1, 5)
        self.assertEqual(len(S),6)
        S2= mlmcAdSamples(2.5, 2, 0.8, 9)
        self.assertEqual(len(S2),10)

    def test_check_samples_decrease(self):
        S = mlmcAdSamples(2, 1.3, 0.1, 5)
        for s in range(len(S)-1):
            self.assertTrue(S[s]>S[s+1])

        S2 = mlmcAdSamples(4, .3, 0.8, 5)
        for s in range(len(S2)-1):
            self.assertTrue(S2[s]>S2[s+1])

    def test_samples_negative_input(self):
        self.assertRaises(ValueError, mlmcAdSamples, -1, 2.3, 0.5, 2)
        self.assertRaises(ValueError, mlmcAdSamples, 1., -2.3, 0.5, 2)
        self.assertRaises(ValueError, mlmcAdSamples, 1., 2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcAdSamples, 1., 2.3, 1.5, -2)
        self.assertRaises(ValueError, mlmcAdSamples, 1., -2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcAdSamples, -1., 2.3, 1.5, -2)
        self.assertRaises(ValueError, mlmcAdSamples, -1., 2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcAdSamples, 1., -2.3, 1.5, -2)

    def test_samples_gamma_larger_one(self):
        self.assertRaises(ValueError, mlmcAdSamples, 1, 2.3, 2, 2)
        self.assertRaises(ValueError, mlmcAdSamples, 1., 2.3, 1.5, 2)

    def test_samples_float_level(self):
        self.assertRaises(TypeError, mlmcAdSamples, 1, 2.3, 0.9, 2.1)
        self.assertRaises(TypeError, mlmcAdSamples, 1., 2.3, .5, 2.01)

class mlmcIpsSamplesTest(unittest.TestCase):
    def test_get_samples(self):
        try:
            S = mlmcIpsSamples(2, 1.3, 0.1, 5)
            S2= mlmcIpsSamples(2.5, 2, 0.8, 9)
        except Exception as e:
            self.fail("Correct usage of mlmcIpsSamples raised exception!")

    def test_check_levels(self):
        S = mlmcIpsSamples(2, 1.3, 0.1, 5)
        self.assertEqual(len(S),6)
        S2= mlmcIpsSamples(2.5, 2, 0.8, 9)
        self.assertEqual(len(S2),10)

    def test_check_samples_decrease(self):
        
        S = mlmcIpsSamples(2, 3.3, 0.2, 5)
        for s in range(len(S)-1):
            self.assertTrue(1.5*S[s]>S[s+1])
        S2 = mlmcIpsSamples(4, .3, 0.8, 5)
        for s in range(len(S2)-1):
            self.assertTrue(1.5*S2[s]>S2[s+1])

    def test_samples_negative_input(self):
        self.assertRaises(ValueError, mlmcIpsSamples, -1, 2.3, 0.5, 2)
        self.assertRaises(ValueError, mlmcIpsSamples, 1., -2.3, 0.5, 2)
        self.assertRaises(ValueError, mlmcIpsSamples, 1., 2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcIpsSamples, 1., 2.3, 1.5, -2)
        self.assertRaises(ValueError, mlmcIpsSamples, 1., -2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcIpsSamples, -1., 2.3, 1.5, -2)
        self.assertRaises(ValueError, mlmcIpsSamples, -1., 2.3, -1.5, 2)
        self.assertRaises(ValueError, mlmcIpsSamples, 1., -2.3, 1.5, -2)

    def test_samples_gamma_larger_one(self):
        self.assertRaises(ValueError, mlmcIpsSamples, 1, 2.3, 2, 2)
        self.assertRaises(ValueError, mlmcIpsSamples, 1., 2.3, 1.5, 2)

    def test_samples_float_level(self):
        self.assertRaises(TypeError, mlmcIpsSamples, 1, 2.3, 0.9, 2.1)
        self.assertRaises(TypeError, mlmcIpsSamples, 1., 2.3, .5, 2.01)

if __name__=='__main__':
    unittest.main()
