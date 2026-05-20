import cv2
import numpy as np
import support as sp
import solveImg as si

WIDTH_IMG=500
HEIGHT_IMG=700
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
imgThresh=cv2.threshold(gray,140,255,cv2.THRESH_BINARY_INV)[1]

# scan first box top-left with different offsets
height,width=imgThresh.shape
piece_width=width//4
piece_height=height//2
box=imgThresh[0:piece_height, 0:piece_width]
print('box shape',box.shape)
for left_offset,choices_width in [(38,65),(42,62),(30,80),(35,85),(20,100)]:
    x0=left_offset; x1=x0+choices_width
    sub=box[:,x0:x1]
    print('offset',left_offset,'w',choices_width,'sub shape',sub.shape)
    col_w=sub.shape[1]//4
    for r in range(15):
        row=sub[r*sub.shape[0]//15:(r+1)*sub.shape[0]//15,:]
        sums=[int(cv2.countNonZero(row[:,c*col_w:(c+1)*col_w])) for c in range(4)]
        print(r+1,sums)
    print('---')
