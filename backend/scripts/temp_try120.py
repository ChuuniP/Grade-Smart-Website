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

# use variant of splitImg120 from get_all_detected_bubbles.py

def splitImg120(img):
    height,width = img.shape[:2]
    rows,cols = 2,4
    piece_height = height // rows
    piece_width = width // cols
    boxes=[]
    for y in range(cols):
        for x in range(rows):
            x_start = piece_width*y + (0 if y == 0 else 10)
            x_end = x_start + piece_width - (0 if y == cols-1 else 15)
            y_start = x * piece_height
            y_end = y_start + piece_height
            piece = img[y_start:y_end, x_start + 20:x_end]
            boxes.append(piece)
    return boxes

def splitAns120(boxes):
    rows,cols=15,4
    ans=[]
    for image in boxes:
        height,width = image.shape[:2]
        piece_height = height // rows
        piece_width = width // cols
        for y in range(rows):
            for x in range(cols):
                start_x=x*piece_width; end_x=start_x+piece_width
                start_y=y*piece_height; end_y=start_y+piece_height
                ans.append(image[start_y:end_y,start_x:end_x])
    return ans

for thresh in [130,140,145,150,155,160]:
    gray=cv2.cvtColor(imgWarp[35:680,15:480], cv2.COLOR_BGR2GRAY)
    imgThresh=cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV)[1]
    boxes=splitImg120(imgThresh)
    ans_images=splitAns120(boxes)
    pixel_vals=np.zeros((120,4),dtype=np.int32)
    for index, cell in enumerate(ans_images[:120]):
        pixel_vals[index//4,index%4]=cv2.countNonZero(cell)
    preds=[]
    for idx in range(40):
        arr=pixel_vals[idx]
        sel=int(np.argmax(arr))
        preds.append(sel)
    score=sum(1 for i,p in enumerate(preds) if p==FINAL_ANS[i])
    print('th',thresh,'score',score)
    if thresh==150:
        print('first 10',[(i+1,preds[i],FINAL_ANS[i], pixel_vals[i].tolist()) for i in range(10)])
