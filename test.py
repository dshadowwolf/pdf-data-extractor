import unittest
from dataExtract import *
import cv2

class TestDeskewAngle(unittest.TestCase):
    def setUp(self):
        self.skew_angle = 0.4961
        
    def test_getAngle(self):
        d = Deskew.Deskew( "test/base_image.jpg" )
        angle = round( d.getAngle(), 4 )
        self.assertEqual(angle, self.skew_angle )

    def shortDescription(self):
        return "Make sure we can still detect the angle by which the image is skewed"

    
class TestDeskewRotate(unittest.TestCase):
    def setUp(self):
        self.base_image = cv2.imread("test/base_image.jpg")
        self.deskewed_image = cv2.imread("test/deskewed_image.jpg")
        
    def test_rotate(self):
        d = Deskew.Deskew( "test/base_image.jpg" )
        img2 = d.rotate()
        self.assertEqual(self.deskewed_image.all(),img2.all())

    def shortDescription(self):
        return "Make sure that the rotation of the image works properly"

class TestCropDown(unittest.TestCase):
    def setUp(self):
        self.base = cv2.imread("test/deskewed_image.jpg")
        self.cropped = cv2.imread("test/cropped_image.jpg")

    def test_ImageCrop(self):
        (corners, x, y) = ImageUtils.getImageBoundsPoints(self.base)
        sx = corners[0]
        sy = corners[1]
        w = corners[2] - (x - sx)
        h = corners[3] - (y - sy)
        cropped = ImageUtils.cropImage(self.base, corners)
        self.assertEqual( self.cropped.all(), cropped.all() )

    def shortDescription(self):
        return "Test cropping an image to size"
    
    # def test_imageSize(self):
    #     self.assertLessEqual( self.base_image.shape[0], self.deskewed_image.shape[0] )
    #     self.assertLessEqual( self.base_image.shape[1], self.deskewed_image.shape[1] )
    #     self.assertEqual( self.base_image.shape[2], self.deskewed_image.shape[2] )
        
    # def shortDescription(self):
    #     return "Test Image Manipulation Methods"


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestDeskewAngle('test_getAngle'))
    suite.addTest(TestDeskewRotate('test_rotate'))
    suite.addTest(TestCropDown('test_ImageCrop'))
    unittest.TextTestRunner(verbosity=2).run(suite)
