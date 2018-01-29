#!/bin/env python

from PIL import Image
from alyn import SkewDetect
from alyn import Deskew
from shutil import copy2, move, rmtree
import os, sys, glob

def ensure_dir(file_path):
        directory = os.path.dirname('%s/%s' % (os.getcwd(), file_path))
        if not os.path.exists(directory):
                os.makedirs(directory)
                
def get_skew(file):
        sd = SkewDetect( file )
        res = sd.process_single_file()
        angle = res['Estimated Angle']
        
        if angle >= 0 and angle <= 90:
                return angle - 90
        if angle >= -45 and angle < 0:
       	        return angle - 90 
        if angle >= -90 and angle < -45:
                return 90 + angle

def is_skewed(file):
        if get_skew(file) != 0:
                return True
        else:
                return False

def make_filename(start, ind):
        (root, ext) = os.path.splitext(start)
        return '%s_%d.%s' % (root, ind, ext)

def crop_work(file):
        im = Image.open(file)
        cropped = im.crop((100,100,1635,2155))
        cropped.save(file)

def setup(file):
        fn = "temp/%s" % file
        ensure_dir(fn)
        copy2(file, fn)

def cleanup(file):
        fn = "out/%s" % file
        on = "temp/%s" % file
        ensure_dir(fn)
        move(on,fn)

def deskew(file):
        setup(file)
        index = 0
        tfn = "temp/%s" % file
        
        while is_skewed( tfn ):
                fn = make_filename(tfn, index)
                im = Deskew( tfn, False, fn, 0 )
                im.run()
                move( fn, tfn )
                crop_work( tfn )
                index += 1
        
        cleanup(file)


if __name__ == '__main__':
        files = glob.glob("*.jpg")
        for file_ in files:
                print "working on %s" % file_
                img = Image.open(file_)
                cv = sum(Image.open(file_).convert("L").getextrema())
                if cv != 255:
                        # we should have an extrema of (0, 255) - anything else and it isn't a form we can process
                        print "WARNING: image %s is not black&white - this image is not valid for processing" % file_
                else:
                        try:
                                deskew( file_ )
                        except:
                                print "Unexpected error processing file:", sys.exc_info()[0]
                                
# im = Image.open("pdfimage_0000_deskewed.jpg")
# cropped = im.crop((100,100,1630,2155))
# cropped.save("pdfimage_0000_deskewed_cropped.jpg")
