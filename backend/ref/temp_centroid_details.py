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
if len(contours)==0:
    raise SystemExit('No contours')
pointContour=np.zeros((4,2),dtype=np.float32)
img,pointContour=si.TakeImgAnswer(img,pointContour,contours)
pt1=np.float32([pointContour[0],pointContour[1],pointContour[2],pointContour[3]])
pt2=np.float32([[0,0],[WIDTH_IMG,0],[0,HEIGHT_IMG],[WIDTH_IMG,HEIGHT_IMG]])
matrix=cv2.getPerspectiveTransform(pt1,pt2)
imgWarp=cv2.warpPerspective(img,matrix,(WIDTH_IMG,HEIGHT_IMG))
imgPer=imgWarp[35:685,20:490]
gray=cv2.cvtColor(imgPer,cv2.COLOR_BGR2GRAY)
imgThresh=cv2.threshold(gray,140,255,cv2.THRESH_BINARY_INV)[1]
h,w=imgThresh.shape
rows=2; cols=4
pw=w/cols; ph=h/rows
contours,_=cv2.findContours(imgThresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
centroids=[]
for cnt in contours:
    area=cv2.contourArea(cnt)
    if 50<area<3000:
        x,y,ww,hh=cv2.boundingRect(cnt)
        if 5<ww<60 and 5<hh<60:
            M=cv2.moments(cnt)
            if M['m00']!=0:
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                col=int(cx//pw)
                row=int(cy//ph)
                if 0<=col<4 and 0<=row<2:
                    centroids.append((col,row,cx,cy,area,x,y,ww,hh))
centroids=sorted(centroids,key=lambda t:(t[0],t[1],t[3],t[2]))
for c in centroids:
    print('col',c[0],'row',c[1],'cx',c[2],'cy',c[3],'area',round(c[4],1),'box',c[5:])
print('total',len(centroids))
