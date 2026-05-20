import cv2, numpy as np, support as sp, solveImg as si
WIDTH_IMG=500; HEIGHT_IMG=700
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
imgThresh=cv2.threshold(gray,140,255,cv2.THRESH_BINARY_INV)[1]

PARAMS=[
    {'left_offset':38,'choices_width':65,'y_top':0,'y_bottom':0},
    {'left_offset':42,'choices_width':62,'y_top':-5,'y_bottom':-5},
    {'left_offset':35,'choices_width':85,'y_top':0,'y_bottom':0},
    {'left_offset':30,'choices_width':100,'y_top':0,'y_bottom':0},
]
for p in PARAMS:
    height,width=imgThresh.shape
    piece_height=height//2; piece_width=width//4
    pixel_vals=np.zeros((40,4),dtype=int)
    question=0
    for y in range(4):
        for x in range(2):
            col_start=piece_width*y
            x_start=col_start+p['left_offset']
            x_end=x_start+p['choices_width']
            y_start=x*piece_height + (p['y_top'] if x==0 else 0)
            y_end=y_start+piece_height + (p['y_bottom'] if x==1 else 0)
            x_start=max(0,min(width,x_start)); x_end=max(0,min(width,x_end))
            y_start=max(0,min(height,y_start)); y_end=max(0,min(height,y_end))
            box=imgThresh[y_start:y_end,x_start:x_end]
            bh, bw=box.shape
            ch = bh/15.0; cw = bw/4.0
            for q in range(15):
                for c in range(4):
                    if question>=40: break
                    cy1=int(q*ch); cy2=int((q+1)*ch)
                    cx1=int(c*cw); cx2=int((c+1)*cw)
                    cell=box[cy1:cy2,cx1:cx2]
                    pixel_vals[question,c]=cv2.countNonZero(cell)
                    question+=1
                if question>=40: break
            if question>=40: break
        if question>=40: break
    correct=0; blanks=0; sel=[]
    for i in range(40):
        arr=pixel_vals[i]; mx=arr.max()
        if mx>15:
            s=int(np.argmax(arr)); sel.append(s)
            if s==FINAL_ANS[i]: correct+=1
        else:
            sel.append(-1); blanks+=1
    print(p, 'correct',correct,'blanks',blanks)
    print(sel[:40])
