import cv2
import numpy as np
import glob
import re
import sys
import warnings
import time

warnings.filterwarnings('ignore')
#from textops import *

#empty list to store template images
image = cv2.imread('ocr-test.png', cv2.IMREAD_COLOR)  # the image with somewhat blurry text (meaning a human eye can somewhat figure out each letter)
template = cv2.imread('cp-d[d].png', cv2.IMREAD_COLOR) # somewhat blurry letter (meaning, it's a known letter w/o mistake) to try and find all instances of


h, w = template.shape[:2]

method = cv2.TM_CCOEFF_NORMED

# ensures that more letters are detected, definitely doesn't miss compared to 0.90 which missed like 6-7 or so
threshold = 0.80

start_time = time.time()

res = cv2.matchTemplate(image, template, method)

# fake out max_val for first run through loop
max_val = 1
prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = None, None, None, None
while max_val > threshold:
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # Prevent infinite loop. If those 4 values are the same as previous ones, break the loop.
    if prev_min_val == min_val and prev_max_val == max_val and prev_min_loc == min_loc and prev_max_loc == max_loc:
        break
    else:
        prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = min_val, max_val, min_loc, max_loc
    
    if max_val > threshold:
        # Prevent start_row, end_row, start_col, end_col be out of range of image
        start_row = max_loc[1] - h // 2 if max_loc[1] - h // 2 >= 0 else 0
        end_row = max_loc[1] + h // 2 + 1 if max_loc[1] + h // 2 + 1 <= res.shape[0] else res.shape[0]
        start_col = max_loc[0] - w // 2 if max_loc[0] - w // 2 >= 0 else 0
        end_col = max_loc[0] + w // 2 + 1 if max_loc[0] + w // 2 + 1 <= res.shape[1] else res.shape[0]

        res[start_row: end_row, start_col: end_col] = 0
        image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,255,0) )

cv2.imwrite('output.png', image) # final image w/ all the matched instances marked
