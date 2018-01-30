Extract black&white images from a PDF:
\# mkdir temp && podofoimgextract <your PDF> temp

Deskewing, cropping and other image processing is a work in progress. Use of
"alyn" has been stopped to try and limit the amount of support libraries that
are needed (alyn using scikit-image for its "Hough Lines" transform, OpenCV
also provides one and that can be used instead - see "Deskew" in
ImageProcess.py).

More... only one or two support libraries will truly be needed if the code is shifted
to C++ - OpenCV and a generic image library for handling the cropping and
rotation needed for the deskew. (Okay, okay, so we could turn the "skew angle"
into an Affine Matrix and use the OpenCV "warpAffine" methods, but...)

TODO: 
A) Test cases for de-skewing and cropping checks. 
B) Implement code to wrap around podofoimgextract and handle the checks to make sure the image is strictly 
   black&white in that code. (hrm... instead of an extrema() sum against an expected maximum, comparing the extrema 
   of img.convert("L") and img.convert("1") would do the same and remove an un-needed summing operation...)
C) Data-file mapping top-left and bottom-right corners of blocks where wanted data should be located
D) Data-file mapping location of markers for figuring out which form is being viewed
E) Data-file mapping page-number for multi-page forms to help with collation of the form images and also locating
   the data
F) OCR all the stuff
G) Test cases for everything outside the de-skewing and cropping

