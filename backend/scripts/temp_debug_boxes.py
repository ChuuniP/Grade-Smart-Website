import cv2, numpy as np, sys
sys.path.insert(0,'backend/ref')
import support as sp
import solveImg as si

img=cv2.imread('backend/ref/MDD.jpg')
img=cv2.resize(img,(500,700))
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgCanny=cv2.Canny(imgGray,50,150)
contours,_=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
contours=sp.rectContour(contours)
pointContour=np.zeros((4,2),dtype=np.float32)
img2, pointContour = si.TakeImgAnswer(img.copy(), pointContour, contours)
pt1=np.float32([pointContour[0],pointContour[1],pointContour[2],pointContour[3]])
pt2=np.float32([[0,0],[500,0],[0,700],[500,700]])
matrix=cv2.getPerspectiveTransform(pt1,pt2)
imgWarp=cv2.warpPerspective(img.copy(),matrix,(500,700))
per=imgWarp[35:685,20:490]
cv2.imwrite('temp_debug_warp.jpg', imgWarp)
cv2.imwrite('temp_debug_per.jpg', per)

# draw splitImg boxes and splitAns cells
boxes=[]
height,width=per.shape[:2]
rows,cols=2,4
piece_height=height//rows
piece_width=width//cols
for y in range(cols):
    for x in range(rows):
        x_start=piece_width*y+38
        x_end=x_start+65
        y_start=x*piece_height
        y_end=y_start+piece_height
        cv2.rectangle(per,(x_start,y_start),(x_end,y_end),(0,255,0),1)
        boxes.append((x_start,y_start,x_end,y_end))

cv2.imwrite('temp_debug_per_boxes.jpg', per)

# show 15 rows split of first box
box=per[0:piece_height, boxes[0][0]:boxes[0][2]]
box_copy=box.copy()
bh,bw=box.shape[:2]
pr=15
pc=4
ph=bh//pr
pw=bw//pc
for r in range(pr):
    for c in range(pc):
        sx=c*pw; ex=sx+pw; sy=r*ph; ey=sy+ph
        cv2.rectangle(box_copy,(sx,sy),(ex,ey),(255,0,0),1)
cv2.imwrite('temp_debug_box0_split.jpg', box_copy)
