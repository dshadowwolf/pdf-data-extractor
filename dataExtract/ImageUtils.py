#!/bin/env python
import numpy as np
import cv2
import math

def max3( itemA, itemB, itemC ):
    return int( math.floor( max( max( itemA, itemB ), itemC ) ) )
        
def min3( itemA, itemB, itemC ):
    return int( math.floor( min( min( itemA, itemB), itemC ) ) )

def getImageBoundsPoints(image):
    if len( image.shape ) > 2:
        # has a color depth
        gray = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    else:
        gray = image
    dst = cv2.dilate( cv2.cornerHarris(gray,2,3,0.04), None )
    y,x = np.nonzero( dst > 0.01*dst.max() )
    corners = [ np.amin(x), np.amin(y), np.amax(x), np.amax(y) ]
    return corners, image.shape[1], image.shape[0]

def getImageBoundsLines(image):
    MIN_X = 0
    MIN_Y = 1
    MAX_X = 2
    MAX_Y = 3
    if len( image.shape ) > 2:
        # has a color depth
        gray = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    else:
        gray = image
    edges = cv2.Canny( gray, 50, 150, apertureSize=3 )
    lines, width, prec, nfa = cv2.createLineSegmentDetector(_refine = cv2.LSD_REFINE_ADV ).detect( edges )
    corners = [ image.shape[1], image.shape[0], 0, 0 ]
    a, b, c = lines.shape
    for i in xrange(a):
        for line in lines[i]:
            corners[MIN_X] = min3( corners[MIN_X], line[MIN_X], line[MAX_X] )
            corners[MIN_Y] = min3( corners[MIN_Y], line[MIN_Y], line[MAX_Y] )
            corners[MAX_X] = max3( corners[MAX_X], line[MIN_X], line[MAX_X] )
            corners[MAX_Y] = max3( corners[MAX_Y], line[MIN_Y], line[MAX_Y] )
    return corners, image.shape[1], image.shape[0]

def cropImage(image, corners):
    return image[corners[1]:corners[3], corners[0]:corners[2]]


def HoughLinesP(image, lines=np.array([]), rho=0.02, theta=np.pi/360, threshold=1, minLineLength=100, maxLineGap=10):
    if len( image.shape ) < 3:
        edges = image
    else:
        edges = cv2.Canny( cv2.cvtColor( image, cv2.COLOR_BGR2GRAY ), 50, 150, apertureSize=3 )
    return cv2.HoughLinesP( image=edges, rho=rho, theta=theta, threshold=threshold, lines=lines,
                            minLineLength=minLineLength, maxLineGap=maxLineGap )
