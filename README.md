Extract black&white images from a PDF:
```
# mkdir temp && podofoimgextract <your PDF> temp
```

OpenCV is now handling all image manipulation duties alongside NumPy - no
other libraries are needed. Code in DataExtractorBase is robust as a trio of
library routines - one of utilities, one for cropping the image and one for
deskewing the image.

TODO:
* Write test-suite to match known-good results to the output of code being produced and/or worked on
* Write properly modular code for all existing image and data manipulation functions

Current YAML format of a file defining a form and how to find its identifying characteristics:
```yaml
!Identifier
name: Test
anchor: !Anchor { Left: 150 +2500,  Top: 2300 -2150 }
coordRange: !Offset { X: 150 +2500, Y: 2300 -2150 }
offsets:
- !Offset { X: 10 +10, Y: 20 +20 }
- !Offset { X: 0 +95,  Y: 100 +10 }
- !Offset { X: 0 +0, Y: 15 +35 }
```

The '!Identifier' specifier marks this as a file containing a definition of where to locate identifying marks in an
image of a form. (It also tells PyYAML to feed the result of the parsing to the constructor of a specific class)

The 'name' feild is for the name of the Form this file describes

The 'anchor' field defines the left and top bounds of the form in the forms defined coordinate space.[1][2][3]

The 'coordRange' field defines the minimum and maximum values of the X and Y coordinates of the image as a pair of
item spans, which is best mapped as an "Offset" in the current form.[3][4]

The 'offsets' field defines an array of offset rectangles[4] (as sets of spans/extents) defining each region of the
source form that might have markings to identify it as being this form.

[1] This is used to find the top-left corner of the form (hopefully) which can be used to map the incoming
offset rectangles to the coordinate space of the image being worked on. The '!Anchor' which starts the data
causes it to be fed to the correct Python class.

[2] These are, technically, an "extent" (YAML Marker '!Extent' or in the form of the regular expression: 
``/\d+\s+[\+\-]\d+/`` - which define the "start" and "length" but is not a vector or even a line segment 
because there is no "direction" or even a defined orientation - it is a scale-less value pair only given
meaning by how it is utilized.

[3] If a better or more descriptive means can be found for representing any of this data - including means
of removing nested data (such as the extents[2] in the '!Anchor' specifier) - they should be added to make
the data easier. To this end the final version of the format will probably have version specifiers attached
to the various specifiers to make this possible.

[4] '!Offset' is defined as a pair of extents[2] that define the top-left corner of a rectangle and how
far its sides expand along the X and Y axes of the coordinate-space

Final note: You can, of course, construct a data-structure of the proper classes entirely in-code and have PyYAML
produce a syntactically correct and complete version. It will even include any of the various streamlined
representations that are provided, such as gets used for the "!Extent" specification in the above example.
(Without the streamlining, an "extent" would look something like the following:
```yaml
!Extent 
start: 150
extent: 2500
```
...That's kind terrible and even squeezing it down to one line, like the !Offset would still leave it looking
kinda bad.
