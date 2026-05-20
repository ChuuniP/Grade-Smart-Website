import cv2
import numpy as np
import os
import sys

sys.path.append(r'e:\Antigravity\Grade Smart\\backend\\ref')
import solveImg as si
import support as sp

WIDTH_IMG = 500
HEIGHT_IMG = 700
CHOICES = 4
FINAL_ANS = [1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2,1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2]

img = cv2.imread(r'e:\Antigravity\Grade Smart\\backend\\ref\\MDD.jpg')
img = cv2.resize(img,(WIDTH_IMG,HEIGHT_IMG))
imgAns=img.copy()
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgCanny=cv2.Canny(imgGray,50,150)
contours,_=cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours=sp.rectContour(contours)
pointContour=np.zeros((4,2),dtype=np.float32)
img, pointContour=si.TakeImgAnswer(img,pointContour,contours)
pt1=np.float32([pointContour[0],pointContour[1],pointContour[2],pointContour[3]])
pt2=np.float32([[0,0],[WIDTH_IMG,0],[0,HEIGHT_IMG],[WIDTH_IMG,HEIGHT_IMG]])
matrix=cv2.getPerspectiveTransform(pt1,pt2)
imgWarp=cv2.warpPerspective(imgAns,matrix,(WIDTH_IMG,HEIGHT_IMG))
perX1,perX2,perY1,perY2=20,490,35,685
imgPer=imgWarp[perY1:perY2,perX1:perX2]
imgCvt=cv2.cvtColor(imgPer,cv2.COLOR_BGR2GRAY)
imgThresh=cv2.threshold(imgCvt,135,255,cv2.THRESH_BINARY_INV)[1]

height,width=imgThresh.shape
piece_height=height//2
piece_width=width//4

pixel_vals=[]
for y in range(4):
    for x in range(2):
        col_start = piece_width*y
        box_x1=col_start+40
        box_x2=box_x1+65
        box_y1=x*piece_height
        box_y2=(x+1)*piece_height
        box=imgThresh[box_y1:box_y2, box_x1:box_x2]
        box_h, box_w=box.shape
        cell_h=box_h//15
        cell_w=box_w//4
        for q in range(15):
            row_start=q*cell_h
            row_end=(q+1)*cell_h
            row_vals=[]
            for choice in range(4):
                col_start=choice*cell_w
                col_end=(choice+1)*cell_w
                cell=box[row_start:row_end,col_start:col_end]
                row_vals.append(int(cv2.countNonZero(cell)))
            pixel_vals.append(row_vals)

for i in range(40):
    arr=pixel_vals[i]
    sel=int(np.argmax(arr))
    print(f'Q{i+1:02d} exp={FINAL_ANS[i]} counts={arr} sel={sel}')
