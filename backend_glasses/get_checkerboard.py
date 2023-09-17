from sensor import Glasses
import time
import cv2
import numpy as np

if __name__ == '__main__':
    i = 0
    try:
        while True:
            res, video = cv2.VideoCapture(0).read()
            cv2.imwrite(f'checkers2/checker_{i}.png', video)
            i += 1
            time.sleep(1)
            print(i)

    except (KeyboardInterrupt, SystemExit):
    #     glasses.shutdown()
        pass