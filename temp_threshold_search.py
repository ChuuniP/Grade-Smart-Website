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
per=imgWarp[35:685,20:490]

# Define current splitImg and splitAns logic

def splitAns(image):
    h,w=image.shape[:2]
    row_height=h//15
    col_width=w//4
    cells=[]
    for row in range(15):
        for col in range(4):
            sx=col*col_width; ex=sx+col_width
            sy=row*row_height; ey=sy+row_height
            cells.append(image[sy:ey,sx:ex])
    return cells


def evaluate(thresh_image, label):
    boxes=sp.splitImg(thresh_image)
    cells=[]
    for box in boxes:
        cells.extend(splitAns(box))
    pixel_vals=np.array([[cv2.countNonZero(cell) for cell in cells[i*4:(i+1)*4]] for i in range(120)])
    result=[]
    for idx in range(40):
        arr=pixel_vals[idx]
        result.append(int(np.argmax(arr)))
    score=sum(1 for i,a in enumerate(result) if a==FINAL_ANS[i])
    print(label,'score',score)
    print('counts Q1-10:')
    for i in range(10):
        print(i+1,pixel_vals[i].tolist(), 'pred', result[i], 'exp', FINAL_ANS[i])
    return result, pixel_vals

for th in [120,130,135,140,145,150,155,160]:
    gray=cv2.cvtColor(per,cv2.COLOR_BGR2GRAY)
    thresh=cv2.threshold(gray,th,255,cv2.THRESH_BINARY_INV)[1]
    evaluate(thresh,f'Th={th}')

otsu=cv2.threshold(cv2.cvtColor(per,cv2.COLOR_BGR2GRAY),0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
evaluate(otsu,'Otsu')
