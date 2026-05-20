import cv2
import numpy as np
import sys
sys.path.insert(0, r'e:\Antigravity\Grade Smart\\backend\\ref')
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4
FINAL_ANS = [1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2,1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2]

img = cv2.imread(r'e:\Antigravity\Grade Smart\\backend\\ref\\MDD.jpg')
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)
pointContour = np.zeros((4,2),dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0,0],[WIDTH_IMG,0],[0,HEIGHT_IMG],[WIDTH_IMG,HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1,pt2)
imgWarp = cv2.warpPerspective(img,matrix,(WIDTH_IMG,HEIGHT_IMG))
perX1,perX2,perY1,perY2 = 15,480,35,680
imgPer = imgWarp[perY1:perY2, perX1:perX2]
gray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
th=160
imgThresh = cv2.threshold(gray,th,255,cv2.THRESH_BINARY_INV)[1]

height,width = imgThresh.shape
rows=2; cols=4
ph=height//rows; pw=width//cols
counts=[]
for y in range(cols):
    for x in range(rows):
        x_start = pw*y + (0 if y==0 else 10)
        x_end = x_start + pw - (0 if y==cols-1 else 15)
        y_start = x*ph; y_end = y_start+ph
        box = imgThresh[y_start:y_end, x_start+20:x_end]
        bh,bw = box.shape
        cell_h = bh//15; cell_w = bw//4
        for r in range(15):
            for c in range(4):
                cy1 = r*cell_h; cy2 = (r+1)*cell_h
                cx1 = c*cell_w; cx2 = (c+1)*cell_w
                cell = box[cy1:cy2, cx1:cx2]
                hh,ww = cell.shape
                sub = cell[hh//4:hh*3//4, ww//4:ww*3//4]
                counts.append(int(cv2.countNonZero(sub)))
counts = np.array(counts).reshape(-1,4)
correct = 0
for i,arr in enumerate(counts[:40]):
    sel = int(np.argmax(arr))
    if sel==FINAL_ANS[i]: correct +=1
    if i<10:
        print(i+1, arr.tolist(), sel, FINAL_ANS[i])
print('correct', correct)
