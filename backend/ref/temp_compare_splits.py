import cv2
import numpy as np
import support as sp
import solveImg as si

WIDTH_IMG=500
HEIGHT_IMG=700
FINAL_ANS=[1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2,1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2]

img=cv2.imread('MDD.jpg')
img=cv2.resize(img,(WIDTH_IMG,HEIGHT_IMG))
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgCanny=cv2.Canny(imgGray,50,150)
contours,_=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
contours=sp.rectContour(contours)
pointContour=np.zeros((4,2),dtype=np.float32)
img,pointContour=si.TakeImgAnswer(img,pointContour,contours)
pt1=np.float32([pointContour[0],pointContour[1],pointContour[2],pointContour[3]])
pt2=np.float32([[0,0],[WIDTH_IMG,0],[0,HEIGHT_IMG],[WIDTH_IMG,HEIGHT_IMG]])
matrix=cv2.getPerspectiveTransform(pt1,pt2)
imgWarp=cv2.warpPerspective(img,matrix,(WIDTH_IMG,HEIGHT_IMG))
imgPer=imgWarp[35:685,20:490]
gray=cv2.cvtColor(imgPer,cv2.COLOR_BGR2GRAY)
for thresh in [130,135,140,145,150]:
    imgThresh=cv2.threshold(gray,thresh,255,cv2.THRESH_BINARY_INV)[1]
    def score(split_img_func):
        boxes = split_img_func(imgThresh)
        pixel_vals=np.zeros((40,4),dtype=int)
        idx=0
        for box in boxes:
            h,w=box.shape[:2]
            row_h=h//15
            col_w=w//4
            for r in range(15):
                for c in range(4):
                    cell=box[r*row_h:(r+1)*row_h, c*col_w:(c+1)*col_w]
                    if idx<40:
                        pixel_vals[idx,c]=cv2.countNonZero(cell)
                    idx+=1
        correct=0; blanks=0
        det=[]
        for i in range(40):
            arr=pixel_vals[i]
            mx=arr.max()
            if mx>15:
                sel=int(np.argmax(arr))
                det.append(sel)
                if sel==FINAL_ANS[i]: correct+=1
            else:
                det.append(-1); blanks+=1
        return correct,blanks,det
    def split_current(img):
        height,width=img.shape[:2]
        rows=2; cols=4
        piece_height=height//rows; piece_width=width//cols
        boxes=[]
        for y in range(cols):
            for x in range(rows):
                col_start=piece_width*y
                left_offset=38
                choices_width=65
                x_start=col_start+left_offset
                x_end=x_start+choices_width
                y_start=x*piece_height
                y_end=y_start+piece_height
                boxes.append(img[y_start:y_end, x_start:x_end])
        return boxes
    def split_best(img):
        height,width=img.shape[:2]
        rows=2; cols=4
        piece_height=height//rows; piece_width=width//cols
        boxes=[]
        for y in range(cols):
            for x in range(rows):
                col_start=piece_width*y
                left_offset=42
                choices_width=62
                x_start=col_start+left_offset
                x_end=x_start+choices_width
                y_start=x*piece_height + (-5 if x==0 else 0)
                y_end=y_start+piece_height + (-5 if x==1 else 0)
                x_start=max(0,min(width,x_start))
                x_end=max(0,min(width,x_end))
                y_start=max(0,min(height,y_start))
                y_end=max(0,min(height,y_end))
                boxes.append(img[y_start:y_end, x_start:x_end])
        return boxes
    print('th',thresh,'current',score(split_current),'best',score(split_best))
