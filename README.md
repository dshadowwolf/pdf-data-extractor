Extract black&white images from a PDF:
```
# mkdir temp && podofoimgextract <your PDF> temp
```

OpenCV is now handling all image manipulation duties alongside NumPy - no
other libraries are needed. Code in DataExtractorBase is robust as a trio of
library routines - one of utilities, one for cropping the image and one for
deskewing the image.

TODO:
A) Write test-suite to match known-good results to the output of code being produced and/or worked on
B) Write properly modular code for all existing image and data manipulation functions

Current YAML format of a file defining a form and how to find its identifying characteristics:
```yaml
!Identifier
name: Test
anchor: !Anchor { Left: 150 +2500,  Top: 2300 -2150 }
coordRange: !Offset { X: 150 +2500, Y: 2300 -2150 }
offsets:
- !Offset { X: 10 +10, Y: 20 +20 }
- !Offset { X: 0 +95,  Y: 100 +10 }
- !Offset { X: 0 +0, Y: 15 +35 }```

'!Identifier' marks this as a file containing a definition of where to locate identifying marks in an
image of a form.
'name' is the name of the Form this file describes
'anchor' defines the left and top bounds of the form in the forms defined coordinate space.[1][2]
'coordRange' defines the minimum and maximum values of the X and Y coordinates of the image as a pair of
item spans, which is best mapped as an "Offset" in the current form.[3]
'offsets' defines an array of offset rectangles[3] (as sets of spans/extents) defining each region of the
source form that might have markings to identify it as being this form.

[1] This is used to find the top-left corner of the form (hopefully) which can be used to map the incoming
offset rectangles to the coordinate space of the image being worked on.
[2] These are, technically, an "extent" (YAML Marker '!Extent' or in the form of the regular expression: 
``/\d+\s+[\+\-]\d+/`` - which define the "start" and "length" but is not a vector or even a line segment 
because there is no "direction" or even a defined orientation - it is a scale-less value pair only given
meaning by how it is utilized.
[3] '!Offset' is defined as a pair of extents[2] that define the top-left corner of a rectangle and how
far its sides expand along the X and Y axes of the coordinate-space

