import cv2
import numpy as np
import sys
sys.path.insert(0, r'e:\Antigravity\Grade Smart\\backend\\ref')
import support as sp
import solveImg as si

WIDTH_IMG=500; HEIGHT_IMG=700
img=cv2.imread(r'e:\Antigravity\Grade Smart\\backend\\ref\\MDD.jpg')
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
perX1,perX2,perY1,perY2=15,480,35,680
imgPer=imgWarp[perY1:perY2,perX1:perX2]
gray=cv2.cvtColor(imgPer,cv2.COLOR_BGR2GRAY)
imgThresh=cv2.threshold(gray,160,255,cv2.THRESH_BINARY_INV)[1]

col_sum=np.sum(imgThresh==255,axis=0)
row_sum=np.sum(imgThresh==255,axis=1)
print('width',imgThresh.shape[::-1])
print('col peaks', np.where(col_sum>np.percentile(col_sum,80))[0][:20])
print('row peaks', np.where(row_sum>np.percentile(row_sum,80))[0][:20])
print('col partitions', np.argwhere(col_sum<np.percentile(col_sum,20))[:20].flatten().tolist())
print('row partitions', np.argwhere(row_sum<np.percentile(row_sum,20))[:20].flatten().tolist())
np.savetxt('col_sum.csv', col_sum, fmt='%d', delimiter=',')
np.savetxt('row_sum.csv', row_sum, fmt='%d', delimiter=',')
cv2.imwrite('debug_projection_thresh.png', imgThresh)
print('saved debug_projection_thresh.png and sums')
