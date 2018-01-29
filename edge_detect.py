import numpy as np
import cv2
from PIL import Image

im1 = cv2.imread('out/pdfimage_0000.jpg')
img1gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
edges1 = cv2.Canny(img1gray,50,150,apertureSize = 3)

# this is enough to get the 'outermost crop'
minLineLength=im1.shape[1]-600
lines = cv2.HoughLinesP(image=edges1, rho=0.125, theta=np.pi/180, threshold=5, lines=np.array([]), minLineLength=minLineLength, maxLineGap=20)

print lines
points = [im1.shape[1], im1.shape[0], 0, 0]

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

im3 = Image.open("out/pdfimage_0000.jpg")
im4 = im3.crop( (points[0], points[1], points[2], points[3]) )
im4.save("out/pdfimage_0000_autocropped.jpg")
im2 = cv2.imread('out/pdfimage_0000_autocropped.jpg')
img2gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
edges2 = cv2.Canny(img2gray,50,150,apertureSize = 3)

lines = cv2.HoughLinesP(image=edges2, rho=0.02, theta=np.pi/180, threshold=10, lines=np.array([]), minLineLength=75, maxLineGap=10)

a,b,c = lines.shape
im5 = np.zeros((im2.shape[0],im2.shape[1],3), np.uint8)
for i in xrange(a):
        for line_ in lines[i]:
                cv2.line( im5, (line_[0], line_[1]), (line_[2], line_[3]), (255,255,255), 2, cv2.LINE_AA )
                
cv2.imwrite("out/pdfimage_0000_edge_detect.jpg", edges2)
cv2.imwrite("out/pdfimage_0000_cropped_marked.jpg", im5)
cv2.imshow('edges', edges2)
cv2.imshow('result', im5)
cv2.waitKey(0)
cv2.destroyAllWindows()
