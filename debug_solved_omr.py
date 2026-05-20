import cv2
import numpy as np
import os
import sys
sys.path.insert(0, r'e:\Antigravity\Grade Smart\\backend\\ref')
import solved_omr as so
res = so.solve_omr(r'e:\Antigravity\Grade Smart\\backend\\ref\\MDD.jpg', questions=40, choices=4)
print('len', len(res))
print(res[:40])
