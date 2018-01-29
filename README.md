Extract black&white images from a PDF, deskew them and crop them to size. Current size works for the known and
provided "OH-3" that came in as a proof-of-concept test. The deskewing is not 100% but seems to get within 1% of pure
vertical. (This makes a lot of sense as the deskew appears to work on horizontal checking and the horizontal lines
seem to be level)

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

