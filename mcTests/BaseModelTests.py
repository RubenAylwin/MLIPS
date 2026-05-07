import unittest
from BaseModel import BaseModel


class BaseModelTest(unittest.TestCase):
    def test_initialization_correct(self):
        try:
            B1 = BaseModel(10,2)
            B2 = BaseModel(10,2.)
        except Exception as e:
            self.fail("Correct initializtion in BaseModel raised exception!")

    def test_initialization_level_incorrect(self):
        self.assertRaises(ValueError, BaseModel, 10., 2)
        self.assertRaises(ValueError, BaseModel, -1, 2)
        self.assertRaises(ValueError, BaseModel, -1., 2)
        self.assertRaises(ValueError, BaseModel, 'a', 2)
        
    def test_initialization_base_incorrect(self):
        self.assertRaises(ValueError, BaseModel, 5, 0.5)
        self.assertRaises(ValueError, BaseModel, 5, -1)
        self.assertRaises(ValueError, BaseModel, 5, -0.5)
        self.assertRaises(ValueError, BaseModel, 5, 'a')

    def test_initialization_base_level_incorrect(self):
        self.assertRaises(ValueError, BaseModel, 10., 0.5)
        self.assertRaises(ValueError, BaseModel, -1., -1)
        self.assertRaises(ValueError, BaseModel, 'a', -0.5)
        self.assertRaises(ValueError, BaseModel, -1., 'a')

    def test_initialization_correct_values(self):
        B = BaseModel(2,1.2)
        self.assertEqual(B.getBase(), 1.2)
        self.assertEqual(B.getNumLevels(), 3)
        self.assertEqual(B.getMaxLevel(), 2)

        B = BaseModel(2,2)
        self.assertEqual(B.getBase(), 2)
        self.assertEqual(B.getNumLevels(), 3)
        self.assertEqual(B.getMaxLevel(), 2)
        
    def test_initialization_empty_fields(self):
        B = BaseModel(10, 2)
        self.assertRaises(AttributeError, B.getConvergenceRate)
        self.assertRaises(AttributeError, B.getWorkRate)
        self.assertRaises(AttributeError, B.getParamDim)
        self.assertRaises(AttributeError, B.getErrorConstant)
        self.assertRaises(AttributeError, B.getLimit, 1)
        self.assertRaises(AttributeError, B.costSamples, [1, 1])
        
if __name__=='__main__':
    unittest.main()

