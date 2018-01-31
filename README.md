Extract black&white images from a PDF:
```
# mkdir temp && podofoimgextract <your PDF> temp
```

OpenCV is now handling all image manipulation duties alongside NumPy - no
other libraries are needed. Code in DataExtractorBase is robust as a trio of
library routines - one of utilities, one for cropping the image and one for
deskewing the image.

TODO: 
A) Implement code to wrap around podofoimgextract and handle the checks to make sure the image is strictly 
   black&white in that code. (hrm... instead of an extrema() sum against an expected maximum, comparing the extrema 
   of img.convert("L") and img.convert("1") would do the same and remove an un-needed summing operation...)
B) Data-file mapping top-left and bottom-right corners of blocks where wanted data should be located
C) Data-file mapping location of markers for figuring out which form is being viewed
D) Data-file mapping page-number for multi-page forms to help with collation of the form images and also locating
   the data
E) OCR all the stuff
F) Form Type Detection ?
G) Test cases for everything outside the de-skewing and cropping

