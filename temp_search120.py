import cv2, numpy as np, sys
sys.path.insert(0, 'backend/ref')
import support as sp, solveImg as si

FINAL_ANS = [1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2,1,2,2,2,3,3,2,1,3,0,0,0,1,2,2,2,3,1,0,2]
img = cv2.imread('backend/ref/MDD.jpg')
img = cv2.resize(img, (500, 700))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray, 50, 150)
contours,_ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sp.rectContour(contours)
pointContour = np.zeros((4,2), dtype=np.float32)
img2, pointContour = si.TakeImgAnswer(img.copy(), pointContour, contours)
pt1=np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
pt2=np.float32([[0,0],[500,0],[0,700],[500,700]])
matrix = cv2.getPerspectiveTransform(pt1, pt2)
imgWarp = cv2.warpPerspective(img.copy(), matrix, (500,700))


def splitImgVariant(img, x_pad, x_gap, x_trim):
    height,width = img.shape[:2]
    rows,cols=2,4
    piece_height = height // rows
    piece_width = width // cols
    boxes=[]
    for y in range(cols):
        for x in range(rows):
            x_start = piece_width*y + (0 if y==0 else x_gap)
            x_end = x_start + piece_width - (0 if y==cols-1 else x_trim)
            y_start = x*piece_height
            y_end = y_start + piece_height
            piece = img[y_start:y_end, x_start + x_pad:x_end]
            boxes.append(piece)
    return boxes


def splitAns(boxes):
    rows,cols=15,4
    ans=[]
    for image in boxes:
        height,width = image.shape[:2]
        ph=height//rows; pw=width//cols
        for y in range(rows):
            for x in range(cols):
                ans.append(image[y*ph:(y+1)*ph, x*pw:(x+1)*pw])
    return ans

best=(0,None)
for x1 in [10,15,20,25,30]:
    for x2 in [470,475,480,485]:
        for y1 in [30,35,40]:
            for y2 in [675,680,685]:
                crop = imgWarp[y1:y2, x1:x2]
                for thresh in [130,140,145,150,155,160]:
                    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    imgThresh = cv2.threshold(gray, thresh,255,cv2.THRESH_BINARY_INV)[1]
                    for x_pad in [10,15,20,25,30]:
                        for x_gap in [0,5,10,15]:
                            for x_trim in [0,5,10,15]:
                                boxes=splitImgVariant(imgThresh,x_pad,x_gap,x_trim)
                                ans_images=splitAns(boxes)
                                pixel_vals=np.zeros((120,4),dtype=int)
                                for i, cell in enumerate(ans_images[:480]):
                                    pixel_vals[i//4, i%4] = cv2.countNonZero(cell)
                                preds=[int(np.argmax(pixel_vals[i])) for i in range(40)]
                                score=sum(1 for i,p in enumerate(preds) if p==FINAL_ANS[i])
                                if score>best[0]:
                                    best=(score, (x1,x2,y1,y2,thresh,x_pad,x_gap,x_trim))
print('BEST',best)
