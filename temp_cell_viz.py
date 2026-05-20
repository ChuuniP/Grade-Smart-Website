import cv2, numpy as np, sys
sys.path.insert(0,'backend/ref')
import support as sp, solveImg as si
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
gray=cv2.cvtColor(per,cv2.COLOR_BGR2GRAY)
thresh=cv2.threshold(gray,140,255,cv2.THRESH_BINARY_INV)[1]
boxes=sp.splitImg(thresh)
ans=[]
for i,box in enumerate(boxes):
    h,w=box.shape[:2]
    ph=h//15; pw=w//4
    for r in range(15):
        for c in range(4):
            cell=box[r*ph:(r+1)*ph,c*pw:(c+1)*pw]
            ans.append(cell)

# compose first 40 cells in 5x8 grid
rows=5; cols=8
cell_h=ans[0].shape[0]; cell_w=ans[0].shape[1]
out=np.zeros((rows*cell_h, cols*cell_w), dtype=np.uint8)
for idx in range(40):
    r=idx//cols; c=idx%cols
    out[r*cell_h:(r+1)*cell_h,c*cell_w:(c+1)*cell_w]=ans[idx]
cv2.imwrite('temp_cells40.jpg', out)
