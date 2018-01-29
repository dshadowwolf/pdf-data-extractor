#!/bin/env python

from alyn import Deskew
from PIL import Image

d = Deskew( input_file='pdfimage_0000.jpg',
            output_file='pdfimage_0000_deskewed.jpg',
            display_image=True,
            r_angle=0 )

d.run()

im = Image.open("pdfimage_0000_deskewed.jpg")
cropped = im.crop((100,110,1630,2120))
cropped.show()
cropped.save("pdfimage_0000_deskewed_cropped.jpg")

