#!/bin/env python
import numpy as np
import cv2
from PIL import Image
import math

# load the original deskewed image, convert to greyscale
# and run the edge detection
im1 = cv2.imread('out/pdfimage_0000.jpg')
img1gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
edges1 = cv2.Canny(img1gray,50,150,apertureSize = 3)

# this is enough to get the 'outermost crop'
minLineLength=im1.shape[1]-600
lines = cv2.HoughLinesP(image=edges1, rho=0.125, theta=np.pi/180, threshold=5, lines=np.array([]), minLineLength=minLineLength, maxLineGap=20)

# find the minima and maxima of the outermost lines, which represent the
# black areas added during the deskew
points = [im1.shape[1], im1.shape[0], 0, 0]
for _line in lines:
        for segment in _line:
                dir_x = segment[2] - segment[0]
                dir_y = segment[3] - segment[1]
                if dir_x < dir_y:
                        if dir_x < 0:
                                dir_x = segment[0] - segment[2]
                else:
                        if dir_y < 0:
                                dir_y = segment[1] - segment[3]
                                
                points[0] = min( points[0], im1.shape[1] - dir_x )
                points[1] = min( points[1], dir_y )
                points[2] = max( points[2], dir_x )
                points[3] = max( points[3], im1.shape[0] - dir_y )

# the hough permutation we did can miss some pixels, so pull the minima and maxima in
# decreasing the final image by 4 pixels
points[0] += 2
points[1] += 2
points[2] -= 2
points[3] -= 2

# actually do the crop
im3 = Image.open("out/pdfimage_0000.jpg")
im4 = im3.crop( (points[0], points[1], points[2], points[3]) )
im4.save("out/pdfimage_0000_autocropped.jpg")

# read the cropped image, convert to grayscale and edge-detect
im2 = cv2.imread('out/pdfimage_0000_autocropped.jpg')
img2gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
edges2 = cv2.Canny(img2gray,50,150,apertureSize = 3)

# line segment detector - don't need more than just the "LSD_REFINE_ADV"
lsd = cv2.createLineSegmentDetector(_refine = cv2.LSD_REFINE_ADV )
lines,width,prec,nfa = lsd.detect( edges2 )

# prep for finding the forms outermost corners
a,b,c = lines.shape
points2 = [ im5.shape[1], im5.shape[0], 0, 0 ]

for i in xrange(a):
        for line_ in lines[i]:
                # yes, its messy but its needed. Should probably offload the min/max bits to a helper in
                # later versions
                points2[0] = min( min( points2[0], int(math.floor(line_[0])) ), int(math.floor(line_[2])) )
                points2[1] = min( min( points2[1], int(math.floor(line_[1])) ), int(math.floor(line_[3])) )
                points2[2] = max( max( points2[2], int(math.floor(line_[0])) ), int(math.floor(line_[2])) )
                points2[3] = max( max( points2[3], int(math.floor(line_[1])) ), int(math.floor(line_[3])) )

# give a bit of extra room
# expand out by 2 pixels top and bottom to give some extra room for stuff that might be on the edge of the document
points2[0] -= 2
points2[1] -= 2
points2[2] += 2
points2[3] += 2

# draw in the box that we're going to do a final crop and/or use as the minima/maxima for the extraction
im5 = im2.copy()
cv2.line( im5, (points2[0], points2[1]), (points2[0], points2[3]), (0,0,255), 1, cv2.LINE_AA )
cv2.line( im5, (points2[0], points2[3]), (points2[2], points2[3]), (0,0,255), 1, cv2.LINE_AA )
cv2.line( im5, (points2[2], points2[3]), (points2[2], points2[1]), (0,0,255), 1, cv2.LINE_AA )
cv2.line( im5, (points2[2], points2[1]), (points2[0], points2[1]), (0,0,255), 1, cv2.LINE_AA )
                
cv2.imwrite("out/pdfimage_0000_boxed.jpg", im5)
