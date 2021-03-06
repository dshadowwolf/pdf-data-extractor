#!/bin/env python

import numpy as np
import cv2
import os
import math
from . import ImageUtils

class Deskew:
    def __init__(self, infile):
        tin = os.path.abspath( os.path.expanduser( os.path.expandvars( infile ) ) )
        if not os.path.exists( tin ):
            print "Input file %s (%s) does not exist!" % (infile, tin)
        self.inputfile = tin
        self.inputImage = cv2.imread(tin)
        

    def getAngle(self):
        lines = ImageUtils.HoughLinesP( image=self.inputImage, minLineLength=self.inputImage.shape[0]/2 )
        angle = 0.0;
        if lines is None:
            print "Bad data? HoughLinesP returned data is empty!"
            return None
        numLines = lines.shape[0]
        for i in xrange(numLines):
            for x1,y1,x2,y2 in lines[i]:
                angle += math.atan2( y2 - y1,
                                     x2 - x1 )
        angle /= numLines
        return (angle *180)/np.pi
        
    def rotate(self):
        angle = self.getAngle()
        if angle is None:
            return None
        rows,cols,colors = self.inputImage.shape
        affineMatrix = cv2.getRotationMatrix2D( (cols/2, rows/2), angle, 1 )
        rotated = cv2.warpAffine(self.inputImage, affineMatrix, (cols, rows))
        return rotated                

