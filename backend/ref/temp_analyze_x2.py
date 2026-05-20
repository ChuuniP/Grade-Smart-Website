import cv2
import numpy as np
import support as sp
import solveImg as si

WIDTH_IMG = 500
HEIGHT_IMG = 700
img = cv2.imread('MDD.jpg')
img = cv2.resize(img, (WIDTH_IMG, HEIGHT_IMG))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)
if len(contours) == 0:
    raise SystemExit('No contours')
pointContour = np.zeros((4, 2), dtype=np.float32)
img, pointContour = si.TakeImgAnswer(img, pointContour, contours)
pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarp = cv2.warpPerspective(img, matrix, (WIDTH_IMG, HEIGHT_IMG))
perX1, perX2, perY1, perY2 = 20, 490, 35, 685
imgPer = imgWarp[perY1:perY2, perX1:perX2]
gray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)[1]

rows = 2
cols = 4
h, w = imgThresh.shape
piece_w = w // cols
piece_h = h // rows
print('region size', w, h)
for y in range(cols):
    for x in range(rows):
        x0 = piece_w * y
        x1 = x0 + piece_w
        y0 = x * piece_h
        y1 = y0 + piece_h
        box = imgThresh[y0:y1, x0:x1]
        col_sum = np.sum(box, axis=0)
        # normalize by height
        col_avg = col_sum / float(box.shape[0])
        thr = 0.15 * col_avg.max()
        high = np.where(col_avg > thr)[0]
        if len(high)==0:
            print('box', y, x, 'no high cols')
            continue
        groups=[]
        cur=[high[0]]
        for i in high[1:]:
            if i-cur[-1] > 1:
                groups.append((cur[0],cur[-1]))
                cur=[i]
            else:
                cur.append(i)
        groups.append((cur[0],cur[-1]))
        selected=[]
        for a,b in groups:
            width=b-a+1
            center=(a+b)/2
            selected.append((a,b,width,center, np.max(col_avg[a:b+1])))
        selected = sorted(selected, key=lambda t:t[1])
        print(f'box {y} {x}: groups count {len(selected)}')
        for a,b,width,center,val in selected:
            print('   ',a,b,width,round(center,1),round(val,1))
        # pick top 4 by max val
        top = sorted(selected, key=lambda t:t[4], reverse=True)[:4]
        print('   top4 centers', [round(t[3],1) for t in sorted(top,key=lambda t:t[3])])
