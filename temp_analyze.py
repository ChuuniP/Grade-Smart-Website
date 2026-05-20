import sys
sys.path.insert(0, 'backend/ref')
import cv2, numpy as np
import mainOmr as m
import support as sp

img = cv2.imread('backend/ref/MDD.jpg')
img = cv2.resize(img, (m.WIDTH_IMG, m.HEIGHT_IMG))
student_answers, imgWarpColored, pt1, pt2, perX1, perX2, perY1, perY2 = m.extract_answers(img)
print('returned', len(student_answers), student_answers[:50])
print('correct first 40', m.FINAL_ANS)
print('analysis:')
for i, ans in enumerate(student_answers[:40]):
    print(i+1, ans, ['A','B','C','D'][ans] if ans>=0 else 'Blank')

imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.threshold(imgCvt, 140, 255, cv2.THRESH_BINARY_INV)[1]
boxes = sp.splitImg(imgThresh)
ans_images = sp.splitAns(boxes)
print('boxes', len(boxes), 'ans_images', len(ans_images))
for qi in range(40):
    arr = [cv2.countNonZero(ans_images[qi*4 + c]) for c in range(4)]
    print(qi+1, arr, np.argmax(arr), np.max(arr))
