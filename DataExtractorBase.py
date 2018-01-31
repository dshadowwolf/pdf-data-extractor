#!/bin/env python
import numpy as np
import cv2
import math
import glob
import os

class utils:
        def __init__(self):
                self.__windows = []

        def ensure_dir_exists(self, file_path):
                directory = os.path.dirname('%s/%s' % (os.getcwd(), file_path))
                if not os.path.exists(directory):
                        os.makedirs(directory)

        def grayscaleAndEdges(self, image):
                gr = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                ed = cv2.Canny( gr, 50, 150, apertureSize=3 )
                return gr, ed

        def doHoughLinesP(self, image, rho=0.125, theta=np.pi/180, maxLineGap=20, threshold=5, minLineLength=10):
                grayscale, edges = self.grayscaleAndEdges(image)
                return cv2.HoughLinesP(image=edges, rho=rho, theta=theta, threshold=threshold, 
                                        lines=np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)

        def doLineSegments(self, image):
                gr, edges = self.grayscaleAndEdges(image)
                lsd = cv2.createLineSegmentDetector(_refine = cv2.LSD_REFINE_ADV )
                return lsd.detect( edges )
                
        def max3( self, itemA, itemB, itemC ):
                return int( math.floor( max( max( itemA, itemB ), itemC ) ) )
        
        def min3( self, itemA, itemB, itemC ):
                return int( math.floor( min( min( itemA, itemB), itemC ) ) )

        def makeWindowAuto(self, windowName):
                if self.__windows.count(windowName) > 0:
                        return
                        
                cv2.namedWindow( windowName, cv2.WINDOW_AUTOSIZE )
                self.__windows.append( windowName )

        def makeWindowNormal( self, windowName ):
                if self.__windows.count(windowName) > 0:
                        return
                        
                cv2.namedWindow( windowName, cv2.WINDOW_NORMAL )

        def showImage( self, windowName, image ):
                if self.__windows.count(windowName) > 0:
                        return
                        
                self.makeWindowNormal(windowName)
                cv2.imshow(windowName, image)
                
        def evLoop(self):
                cv2.waitKey(0)
                cv2.destroyAllWindows()

class CropImage:
        def __init__(self, filename, outdir, utils_=None):
                self.inputFile = filename
                self.__image = None
                self.outputName = "%s/cropped_%s" % (outdir, os.path.basename(filename))
                if utils_ is None:
                        self.__utils = utils()
                else:
                        self.__utils = utils_

        def getBounds(self):
                img = cv2.imread(self.inputFile)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = np.float32(gray)
                dst = cv2.cornerHarris(gray,2,3,0.04)
                dst = cv2.dilate(dst,None)
                y,x = np.nonzero( dst > 0.01*dst.max() )
                corners = [ np.amin(x), np.amin(y), np.amax(x), np.amax(y) ]
                return corners, img.shape[1], img.shape[0]

        def cropImage(self):
                corners, maxX, maxY = self.getBounds()
                img = cv2.imread(self.inputFile)
                self.__image = img[corners[1]:corners[3], corners[0]:corners[2]]

        def process(self):
                self.cropImage()
                cv2.imwrite( self.outputName, self.__image )
        
        def getImage(self):
                return self.__image

class Deskew:
        def __init__(self, indir, outdir, fileglob, utils_=None):
                self.inputdir = indir
                self.outputdir = outdir
                self.glob = fileglob
                self.files = self.makeGlob()
                self.curImage = None
                self.curFile = None
                self.baseFilename = None
                self.__utils = utils_
                if self.__utils is None:
                        self.__utils = utils()

        def loadImage(self, filename):
                print "Loading ", filename
                self.curImage = cv2.imread(filename)
                self.curFile = filename
                self.baseFilename = os.path.basename(filename)

        def deskew(self):
                if self.curImage is None:
                        if self.curFile is not None:
                                self.loadImage(self.curFile)
                        else:
                                print "Image not found or loaded !"
                                return None
                                
                gray = cv2.cvtColor(self.curImage, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny( gray, 50, 150, apertureSize=3)
                lines = cv2.HoughLinesP( image=edges, lines=np.array([]), rho=0.02, theta=np.pi/360, threshold=1, minLineLength=gray.shape[1]/4, maxLineGap=10 )
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
                rows,cols,colors = self.curImage.shape
                affineMatrix = cv2.getRotationMatrix2D( (cols/2, rows/2), sk_angle, 1 )
                rotated = cv2.warpAffine(self.curImage, affineMatrix, (cols, rows))
                return rotated                
        
        def doSingle(self, filename):
                self.loadImage(filename)
                return self.deskew()

        def makeGlob(self):
                return glob.glob( "%s/%s" % (self.inputdir, self.glob) )

        def writeOutput(self, image):
                outname = "%s/deskewed_%s" % (self.outputdir, self.baseFilename)
                self.__utils.ensure_dir_exists(outname)
                cv2.imwrite(outname, image) 
                
        def run(self):
                self.files = self.makeGlob()
                for file_ in files:
                        im = self.doSingle(file_)
                        self.writeOutput(im)

if __name__ == "__main__":
        print "I do nothing right now standalone"

