import unittest
from dataExtract import *
import cv2

class TestImageMethods(unittest.TestCase):
    def test_load(self):
        img = cv2.imread("test/base_image.jpg")
        self.assertTrue(img.shape is not None)
        self.assertEqual(len(img.shape), 3)

    def test_getAngle(self):
        img = cv2.imread("test/base_image.jpg")
        d = Deskew.Deskew( "test/base_image.jpg" )
        angle = d.getAngle()
        self.assertEqual(angle, 0.4960549603952498 )

    def test_rotate(self):
        img = cv2.imread("test/deskewed_image.jpg")
        d = Deskew.Deskew( "test/base_image.jpg" )
        img2 = d.rotate()
        self.assertEqual(img.all(),img2.all())
        
    
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestImageMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
