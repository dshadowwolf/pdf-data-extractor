#!/bin/env python

import numpy as np
import cv2
import os

class Deskew:
    def __init__(self, infile, outfile):
        tin = os.path.abspath( os.path.expanduser( os.path.expandvars( infile ) ) )
        tout = os.path.abspath( os.path.expanduser( os.path.expandvars( outfile ) ) )
        if not os.path.exists( tin ):
            print "Input file %s (%s) does not exist!" % (infile, tin)
        self.inputfile = tin
        self.outputfile = tout
        self.inputimage = cv2.imread(tin)

    def grayscaleAndEdges(self):
        self.gray = cv2.cvtColor(self.inputimage, cv2.COLOR_BGR2GRAY)
        self.edges = cv2.Canny( gr, 50, 150, apertureSize=3 )
    
    def run(self):
        self.grayscaleAndEdges()
        lines = cv2.HoughLinesP( image=self.edges, lines=np.array([]), rho=0.02, theta=np.pi/360, threshold=1, minLineLength=self.gray.shape[1]/4, maxLineGap=10 )
        angle = 0.0;
        if lines is None:
            print "Bad data? HoughLinesP returned data is empty!"
            return None
        numLines = lines.shape[0]
        for i in xrange(numLines):
            angle += math.atan2( lines[i][0][3] - lines[i][0][1],
                                 lines[i][0][2] - lines[i][0][0] )
        angle /= numLines
        sk_angle = (angle *180)/np.pi
        rows,cols,colors = self.inputimage.shape
        affineMatrix = cv2.getRotationMatrix2D( (cols/2, rows/2), sk_angle, 1 )
        rotated = cv2.warpAffine(self.inputimage, affineMatrix, (cols, rows))
        return rotated                

