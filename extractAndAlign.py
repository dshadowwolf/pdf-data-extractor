#!/usr/bin/env python
import os
import sys
import argparse
import tempfile
import cv2
import numpy as np
from dataExtract import *

def extract(files, target):
    for file in files:
        os.system( "podofoimgextract %s %s" % (file, target) )

def do_align( target_dir, source_dir, files ):
    for file in files:
        print "Working on %s/%s" % (source_dir, file)
        try:
            d = Deskew.Deskew( "%s/%s" % (source_dir, file) )
            cv2.imwrite( "%s/%s" % (target_dir, file), d.rotate() )
        except Exception as e:
            print "Exception processing file %s/%s" % (source_dir, file)
            print e
            
def align(source_dir, target_dir):
    os.path.walk( source_dir, do_align, target_dir )

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description='Extract all images from a provided set of PDF\'s and attempt to align them if the image itself happens to be skewed',
                                      epilog='''Notes:
     At the moment there is no good way to detect if an image has the needed information for the de-skew procedure
     to work and this might cause issues if such an image is present and handed to the library code handling this.
                                      ''')
    parser.add_argument( '-t', '--temp', help='Temporary directory for extracted and possibly skewed images', nargs=1 )
    parser.add_argument( '-o', '--output', help='Directory where final output images will be placed', nargs=1, required=True )
    parser.add_argument( 'files', nargs=argparse.REMAINDER )

    if len( sys.argv ) <= 1:
        parser.print_help()

    args = parser.parse_args()
    tpath = None
    if hasattr( args, "temp" ):
        tpath = os.path.abspath(os.path.expanduser(os.path.expandvars(args.temp[0])))
    else:
        tpath = os.path.abspath(os.path.expanduser(os.path.expandvars(tempfile.gettempdir())))

    outpath = os.path.abspath(os.path.expanduser(os.path.expandvars(args.output[0])))
    
    if not os.path.exists(outpath):
        os.makedirs(outpath)
        
    if not os.path.exists(tpath):
        os.makedirs(tpath)

    extract( args.files, tpath )
    align( tpath, outpath )
    
    
