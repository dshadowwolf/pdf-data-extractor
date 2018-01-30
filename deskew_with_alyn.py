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
        
def crop_work(file):
        im = Image.open(file)
        cropped = im.crop((100,100,1635,2155))
        cropped.save(file)

def setup(file):
        fn = "temp2/%s" % file
        ensure_dir(fn)
        copy2(file, fn)

def cleanup(file):
        fn = "out/%s" % file
        on = "temp2/%s" % file
        ensure_dir(fn)
        move(on,fn)

def deskew(file):
        rawname = os.path.basename(file)
        setup(file)
        tfn = os.path.abspath("temp2/%s" % rawname)
        base = os.path.abspath(file)
        
        im = Deskew( base, False, tfn, 0 )
        im.run()
        
        cleanup(rawname)


if __name__ == '__main__':
        files = glob.glob("temp/*.jpg")
        for file_ in files:
                print "working on temp/%s" % os.path.basename(file_)
                img = Image.open(file_)
                cv = sum(img.convert("L").getextrema())
                if cv != 255:
                        # we should have an extrema of (0, 255) - anything else and it isn't a form we can process
                        print "WARNING: image %s is not black&white - this image is not valid for processing" % file_
                else:
                        try:
                                deskew( file_ )
                        except:
                                print "Unexpected error processing file:", sys.exc_info()
                                
# im = Image.open("pdfimage_0000_deskewed.jpg")
# cropped = im.crop((100,100,1630,2155))
# cropped.save("pdfimage_0000_deskewed_cropped.jpg")
