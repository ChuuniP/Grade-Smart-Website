import cv2, numpy as np, sys
sys.path.insert(0, 'backend/ref')
import support as sp

WIDTH_IMG=500
HEIGHT_IMG=700
CHOICES=4
FINAL_ANS=[1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2,1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2]
img=cv2.imread('backend/ref/MDD.jpg')
img=cv2.resize(img,(WIDTH_IMG,HEIGHT_IMG))
imgAns=img.copy()
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgCanny=cv2.Canny(imgGray,50,150)
contours,_=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
contours=sp.rectContour(contours)
pointContour=np.zeros((4,2),dtype=np.float32)
import solveImg as si
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
pt1=np.float32([pointContour[0],pointContour[1],pointContour[2],pointContour[3]])
pt2=np.float32([[0,0],[WIDTH_IMG,0],[0,HEIGHT_IMG],[WIDTH_IMG,HEIGHT_IMG]])
matrix=cv2.getPerspectiveTransform(pt1,pt2)
imgWarpColored=cv2.warpPerspective(imgAns,matrix,(WIDTH_IMG,HEIGHT_IMG))
perX1,perX2,perY1,perY2 = 20,490,35,685
imgPer=imgWarpColored[perY1:perY2, perX1:perX2]
imgCvt=cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh=cv2.threshold(imgCvt,135,255,cv2.THRESH_BINARY_INV)[1]

def splitImg120(img):
    height,width = img.shape[:2]
    rows,cols = 2,4
    piece_height = height//rows
    piece_width = width//cols
    boxes=[]
    for y in range(cols):
        for x in range(rows):
            x_start = piece_width*y + (0 if y==0 else 10)
            x_end = x_start + piece_width - (0 if y==cols-1 else 15)
            y_start = x*piece_height
            y_end = y_start + piece_height
            piece = img[y_start:y_end, x_start+20:x_end]
            boxes.append(piece)
    return boxes

def splitAns120(boxes):
    rows,cols = 15,4
    ans=[]
    for image in boxes:
        h,w=image.shape[:2]
        ph=h//rows
        pw=w//cols
        for y in range(rows):
            for x in range(cols):
                piece = image[y*ph:(y+1)*ph, x*pw:(x+1)*pw]
                ans.append(piece)
    return ans

boxes = splitImg120(imgThresh)
ans_images = splitAns120(boxes)
print('boxes', len(boxes), 'ans_images', len(ans_images))
pixel_vals = np.zeros((120,CHOICES),dtype=np.int32)
for index,cell in enumerate(ans_images):
    total_pixels = cv2.countNonZero(cell)
    row = index//CHOICES
    col = index%CHOICES
    pixel_vals[row][col]=total_pixels

answers=[]
for idx in range(40):
    arr = pixel_vals[idx]
    selected = int(np.argmax(arr))
    answers.append(selected)
print('pred', answers)
print('expected', FINAL_ANS)
print('correct', sum(1 for i,v in enumerate(answers) if v==FINAL_ANS[i]))
