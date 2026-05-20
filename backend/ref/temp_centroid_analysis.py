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
perX1,perX2,perY1,perY2=20,490,35,685
imgPer=imgWarp[perY1:perY2,perX1:perX2]
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
                centroids.append((cx,cy,area,x,y,ww,hh))

print('num',len(centroids))
boxes=[[] for _ in range(8)]
for (cx,cy,area,x,y,ww,hh) in centroids:
    by=int(cy//ph)
    bx=int(cx//pw)
    if by<0 or by>=2 or bx<0 or bx>=4: continue
    idx=bx*2+by
    boxes[idx].append((cx,cy,area,x,y,ww,hh))

for idx, box in enumerate(boxes):
    print('box', idx, 'count', len(box))
    xs=[c[0] for c in box]
    ys=[c[1] for c in box]
    print('  x min/max', min(xs), max(xs), 'mean', np.mean(xs), 'std', np.std(xs))
    print('  x centers', sorted(xs)[:20])
    if len(xs)>0:
        hist, edges=np.histogram(xs, bins=20, range=(0,w))
        print('  hist top bins', sorted([(hist[i],edges[i],edges[i+1]) for i in range(len(hist))], reverse=True)[:10])

