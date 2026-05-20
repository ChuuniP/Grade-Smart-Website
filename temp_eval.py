import cv2, numpy as np, sys
sys.path.insert(0,'backend/ref')
import support as sp, solveImg as si
FINAL_ANS=[1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2,1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2]
img=cv2.imread('backend/ref/MDD.jpg')
img=cv2.resize(img,(500,700))
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgCanny=cv2.Canny(imgGray,50,150)
contours,_=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
contours=sp.rectContour(contours)
pointContour=np.zeros((4,2),dtype=np.float32)
img, pointContour=si.TakeImgAnswer(img.copy(),pointContour,contours)
pt1=np.float32([pointContour[0],pointContour[1],pointContour[2],pointContour[3]])
pt2=np.float32([[0,0],[500,0],[0,700],[500,700]])
matrix=cv2.getPerspectiveTransform(pt1,pt2)
imgWarp=cv2.warpPerspective(img.copy(),matrix,(500,700))

for x1,x2 in [(15,480),(20,490),(10,480)]:
    for y1,y2 in [(35,680),(35,685),(30,675)]:
        for th in [140,145,150,155,160]:
            per=imgWarp[y1:y2,x1:x2]
            gray=cv2.cvtColor(per,cv2.COLOR_BGR2GRAY)
            thresh=cv2.threshold(gray,th,255,cv2.THRESH_BINARY_INV)[1]
            h,w=thresh.shape
            ph=h//2; pw=w//4
            answers=[]
            for col in range(4):
                for row in range(2):
                    x_start=pw*col + (0 if col==0 else 10)
                    x_end=x_start+pw - (0 if col==3 else 15)
                    y_start=row*ph; y_end=y_start+ph
                    box=thresh[y_start:y_end, x_start+20:x_end]
                    rh, rw=box.shape
                    r_h=rh//15; r_w=rw//4
                    for rr in range(15):
                        for cc in range(4):
                            cell=box[rr*r_h:(rr+1)*r_h, cc*r_w:(cc+1)*r_w]
                            answers.append(int(np.argmax(np.bincount(cell.flatten()[cell.flatten()>0])) if np.count_nonzero(cell)>0 else 0))
            # We only need first 40
            preds=answers[:40]
            score=sum(1 for i,a in enumerate(preds) if a==FINAL_ANS[i])
            if score>=19:
                print('coords',x1,x2,y1,y2,'th',th,'score',score)
