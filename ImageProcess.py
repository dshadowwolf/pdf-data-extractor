#!/bin/env python
import numpy as np
import cv2
from PIL import Image
import math
import glob

class ImageProcess:
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
                
        def loadImagePIL(self, filename):
                return Image.open(filename)

        def makeGrayscale(self, image):
                return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        def edgeDetect(self, image):
                return cv2.Canny(image, 50, 150, apertureSize=3)

        def prepCVImage(self, filename):
                img = loadImageCV(self,filename)
                gray = makeGrayscale(self,img)
                edges = edgeDetect(self,img)
                return img, gray, edges

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

        def cropImage(self, filename):
                img, gray, edges = prepCVImage(self, filename)
                lines = cv2.HoughLinesP(image=edges, rho=0.125, theta=np.pi/180, threshold=5, 
                                        lines=np.array([]), minLineLength=img.shape[1]-600, maxLineGap=20)
                points = findMaximaAndMinima( self, lines, img.shape[1], img.shape[0] )
                toCrop = loadImagePIL( self, filename )
                toCrop.crop( (points[0], points[1], points[2], points[3]) ).save( filename )
                
        def max3( itemA, itemB, itemC ):
                return int( math.floor( max( max( itemA, itemB ), itemC ) ) )
        
        def min3( itemA, itemB, itemC ):
                return int( math.floor( min( min( itemA, itemB), itemC ) ) )

        def findCornerPoints(self, filename):
                img, gray, edges = prepCVImage(self, filename)
                lsd = cv2.createLineSegmentDetector(_refine = cv2.LSD_REFINE_ADV )
                lines,width,prec,nfa = lsd.detect( edges2 )
                
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
                        print "working on %s, output at %s" % (filename, output)
                        self.cropImage(filename)
                        cv2.imwrite( output, self.drawBorderLines(filename) )


# use:
# worker = ImageProcess( indir = <input directory>, outdir = <output directory>, fnpattern = <glob pattern> )
# worker.run()
