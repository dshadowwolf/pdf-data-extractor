#!/bin/env python
import numpy as np
import cv2
from PIL import Image
import math
import glob
import os
import imutils
import os

class utils:
        def ensure_dir_exists(file_path):
                directory = path.dirname('%s/%s' % (os.getcwd(), file_path))
                if not os.path.exists(directory):
                        os.makedirs(directory)

        def grayscaleAndEdges(image):
                gr = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                ed = cv2.Canny( gr, 50, 150, apertureSize=3 )
                return gr, ed

        def doHoughLinesP(image, rho=0.125, theta=np.pi/180, maxLineGap=20, threshold=5, minLineLength):
                grayscale, edges = grayscaleAndEdges(image)
                return cv2.HoughLinesP(image=edges, rho=rho, theta=theta, threshold=threshold, 
                                        lines=np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)

        def doLineSegments(image):
                gr, edges = grayscaleAndEdges(image)
                lsd = cv2.createLineSegmentDetector(_refine = cv2.LSD_REFINE_ADV )
                return lsd.detect( edges )

class CropDeskewedImage:
        def __init__(self, filename, outdir):
                self.inputFile = filename
                self.__image = Image.open(filename)
                self.outputName = "%/cropped_%s" % (outdir, os.path.basename(filename))

        def getBounds(self):
                img = cv2.imread(self.inputFile)
                lines = utils.doHoughLinesP( image=img, minLineLength=img.shape[1]-600 )
                return lines, img.shape[1], img.shape[0]
                
        def findMaximaAndMinima(self, lines, imgXMax, imgYMax):
                points = [imgXMax, imgYMax, 0, 0]
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
                points[0] += 2
                points[1] += 2
                points[2] -= 2
                points[3] -= 2
                return points

        def cropImage(self):
                lines, maxX, maxY = self.getBounds()
                trueBounds = self.findMinimaAndMaxima(lines, maxX, maxY)
                self.__image.crop( (trueBounds[0], trueBounds[1], trueBounds[2], trueBounds[3]) )
                
        def process(self):
                self.cropImage()
                self.__image.save( self.outputName )

class GridBounds:
        def __init__(self, indir, outdir, fnpattern):
                self.indir = indir
                self.outdir = outdir
                self.pattern = fnpattern
                self.filelist = makeGlob(self.indir, self.pattern)

        def setInputDirectory(self, dirname):
                self.indir = dirname
                self.filelist = makeGlob(self, self.indir, self.pattern)
                
        def setOutputDirectory(self, dirname):
                self.outdir = outdir
        
        def makeGlob(self, dirname, glob_pattern):
                self.filelist = glob.glob( "%s/%s" % (dirname,glob_pattern) )

        def loadImageCV(self, filename):
                return cv2.imread(filename)
                
        def makeGrayscale(self, image):
                return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        def edgeDetect(self, image):
                return cv2.Canny(image, 50, 150, apertureSize=3)

        def prepCVImage(self, filename):
                img = loadImageCV(self,filename)
                gray = makeGrayscale(self,img)
                edges = edgeDetect(self,img)
                return img, gray, edges
                
        def max3( itemA, itemB, itemC ):
                return int( math.floor( max( max( itemA, itemB ), itemC ) ) )
        
        def min3( itemA, itemB, itemC ):
                return int( math.floor( min( min( itemA, itemB), itemC ) ) )

        def findCornerPoints(self, filename):
                lines, width, prec, nfa = utils.doLineSegments( cv2.imread( filename ) )
                
                # prep for finding the forms outermost corners
                a,b,c = lines.shape
                points = [ img.shape[1], img.shape[0], 0, 0 ]

                for i in xrange(a):
                        for line_ in lines[i]:
                                points[0] = min3( points2[0], line_[0], line_[2] )
                                points[1] = min3( points2[1], line_[1], line_[3] )
                                points[2] = max3( points2[2], line_[0], line_[2] )
                                points[3] = max3( points2[3], line_[1], line_[3] )

                # give a bit of extra room
                # expand out by 2 pixels top and bottom to give some extra room for stuff that might
                # be on the edge of the document
                points[0] -= 2
                points[1] -= 2
                points[2] += 2
                points[3] += 2
                return points

        def drawBorderLines(self, filename):
                points = findCornerPoints(self, filename)
                img = loadImageCV(self, filename)
                lines = [ [ (points[0], points[1]), (points[0], points[3]) ], 
                          [ (points[0], points[3]), (points[2], points[3]) ],
                          [ (points[2], points[3]), (points[2], points[1]) ],
                          [ (points[2], points[1]), (points[0], points[1]) ] ]
                for line in lines:
                        cv2.line( img, line[0], line[1], (0,0,255), cv2.LINE_AA )
                return img

        def run(self):
                for filename in self.filelist:
                        output = "%s/%s" % (self.outdir, os.path.basename(filename))
                        cv2.imwrite( output, self.drawBorderLines(filename) )

class Deskew:
        def __init__(self, indir, outdir, fileglob):
                self.inputdir = indir
                self.outputdir = outdir
                self.glob = fileglob
                self.files = self.makeGlob()
                self.curImage = None
                self.curFile = None
                self.baseFilename = None
                
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
                rotated = imutils.rotate(self.curImage, sk_angle)
                return rotated                
        
        def doSingle(self, filename):
                self.loadImage(filename)
                return self.deskew()

        def makeGlob(self):
                return glob.glob( "%s/%s" % (self.inputdir, self.glob) )

        def writeOutput(self, image):
                outname = "%s/deskewed_%s" % (self.outputdir, self.baseFilename)
                ensure_dir_exists(outname)
                cv2.imwrite(outname, image) 
                
        def run(self):
                self.files = self.makeGlob()
                for file_ in files:
                        im = self.doSingle(file_)
                        self.writeOutput(im)

if __name__ == "__MAIN__":
        print "I do nothing right now standalone"
