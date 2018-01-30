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
                                
                                points[0] = min( points[0], imgXMax - dir_x )
                                points[1] = min( points[1], dir_y )
                                points[2] = max( points[2], dir_x )
                                points[3] = max( points[3], imgYMax - dir_y )
                points[0] += 2
                points[1] += 2
                points[2] -= 2
                points[3] -= 2
                return points
class CropDeskewedImage:
        def __init__(self, filename, outdir):
                self.inputFile = filename
                self.__image = Image.open(filename)
                self.outputName = "%s/cropped_%s" % (outdir, os.path.basename(filename))

        def getBounds(self):
                img = cv2.imread(self.inputFile)
                lines = utils().doHoughLinesP( image=img, minLineLength=img.shape[1]-600 )
                return lines, img.shape[1], img.shape[0]

        def cropImage(self):
                lines, maxX, maxY = self.getBounds()
                trueBounds = utils().findMaximaAndMinima(lines, maxX, maxY)
                print trueBounds
                self.__image.crop( (trueBounds[0], trueBounds[1], trueBounds[2], trueBounds[3]) )
                
        def process(self):
                self.cropImage()
                self.__image.save( self.outputName )

class GridBounds:
        def __init__(self, indir, outdir, fnpattern):
                self.indir = indir
                self.outdir = outdir
                self.pattern = fnpattern
                self.filelist = self.makeGlob(self.indir, self.pattern)

        def setInputDirectory(self, dirname):
                self.indir = dirname
                self.filelist = self.makeGlob( self.indir, self.pattern)
                
        def setOutputDirectory(self, dirname):
                self.outdir = outdir
        
        def makeGlob(self, dirname, glob_pattern):
                return glob.glob( "%s/%s" % (dirname,glob_pattern) )

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
                
        def findCornerPoints(self, filename):
                img = cv2.imread(filename)
                lines, width, prec, nfa = utils().doLineSegments( img )
                # prep for finding the forms outermost corners
                a,b,c = lines.shape
                points = [ img.shape[1], img.shape[0], 0, 0 ]
                
                for i in xrange(a):
                        for line_ in lines[i]:
                                util = utils()
                                points[0] = util.min3( points[0], line_[0], line_[2] )
                                points[1] = util.min3( points[1], line_[1], line_[3] )
                                points[2] = util.max3( points[2], line_[0], line_[2] )
                                points[3] = util.max3( points[3], line_[1], line_[3] )
                               
                # give a bit of extra room
                # expand out by 2 pixels top and bottom to give some extra room for stuff that might
                # be on the edge of the document
                points[0] -= 2
                points[1] -= 2
                points[2] += 2
                points[3] += 2
                if points[0] < 0:
                        points[0] = 0
                if points[1] < 0:
                        points[1] = 0

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

        def getBounds(self, fn):
                img = cv2.imread(fn)
                lines = utils().doHoughLinesP( image=img, minLineLength=img.shape[1]/2 )
                return lines, img.shape[1], img.shape[0]

        def tryCrop(self, filename):
                img = self.loadImageCV(filename)
                maxX = img.shape[1]
                maxY = img.shape[0]
                lines = utils().doHoughLinesP( image=img, minLineLength=maxX/4 )
                print lines
                print lines.shape
                points = utils().findMaximaAndMinima(lines, maxX, maxY)
                x_end = points[2]
                y_end = points[3]
                x_start = points[0]
                y_start = points[1]
                width = x_end - x_start
                height = y_end -y_start
                print (points, width, height)
                print x_start, y_start, x_end, y_end
                new_image = img[y_start:y_end, x_start:x_end].copy()
                print img.shape
                print new_image.shape
                return new_image

        def doSingle(self):
                fn = self.filelist[0]
                img = self.loadImageCV(fn)
                lines, maxX, maxY = self.getBounds(fn)
                points = utils().findMaximaAndMinima(lines, maxX, maxY)
                a,b,c = lines.shape
                for i in xrange(a):
                        cv2.line( img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]),
                                  (255,255,255), 2, cv2.LINE_AA )

                cv2.line( img, (points[0],points[1]), (points[0], points[3]), (0,0,255), 2, cv2.LINE_AA )
                cv2.line( img, (points[0],points[3]), (points[2], points[3]), (0,0,255), 2, cv2.LINE_AA )
                cv2.line( img, (points[2],points[3]), (points[2], points[1]), (0,0,255), 2, cv2.LINE_AA )
                cv2.line( img, (points[2],points[1]), (points[0], points[1]), (0,0,255), 2, cv2.LINE_AA )

                cv2.imshow("orig", img)
                
                img = self.tryCrop(fn)
                print img.shape
                if not img.shape[0] > 0 or not img.shape[1] > 0:
                        print "cropped is bad shape!"
                        return
                im = self.tryCrop(fn)
                cv2.imshow(fn, im)
                cv2.imwrite( "out/test-image.jpg", im )
                cv2.waitKey(0)
                cv2.destroyAllWindows()

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
                rotated = imutils.rotate(self.curImage, sk_angle)
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
        d = Deskew( "temp", "out", "pdfimage_????.jpg")
        im = d.doSingle( "temp/pdfimage_0000.jpg" )
        d.writeOutput( im )
#        cr = CropDeskewedImage( "out/deskewed_pdfimage_0000.jpg", "out" )
#        cr.process()
        gb = GridBounds( "out", "out", "deskewed_pdfimage_????.jpg" )
        gb.doSingle()
