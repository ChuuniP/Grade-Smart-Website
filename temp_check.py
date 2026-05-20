import cv2, numpy as np, os
path = 'backend/ref/MDD.jpg'
img = cv2.imread(path)
print('path', path, 'exists', os.path.exists(path))
print('shape', img.shape if img is not None else None)
img_resized = cv2.resize(img, (500, 700))
imgPer = img_resized[35:685, 20:490]
print('per shape', imgPer.shape)
imgGray = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
print('th stats')
for t in [100,110,120,130,135,140,145,150,160]:
    th = cv2.threshold(imgGray, t, 255, cv2.THRESH_BINARY_INV)[1]
    print('th', t, 'nonzero', cv2.countNonZero(th))
height,width = imgPer.shape[:2]
rows,cols = 2,4
ph = height//rows
pw = width//cols
print('ph,pw', ph, pw)
for y in range(cols):
    for x in range(rows):
        x_start = pw*y + 38
        x_end = x_start + 65
        y_start = x*ph
        y_end = y_start + ph
        box = imgPer[y_start:y_end, x_start:x_end]
        g = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
        print('box', y, x, box.shape, 'mean', np.mean(g), 'nonzero', cv2.countNonZero(cv2.threshold(g, 140, 255, cv2.THRESH_BINARY_INV)[1]))
