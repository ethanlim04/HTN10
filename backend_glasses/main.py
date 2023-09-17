from sensor import Glasses
import time
import cv2
import numpy as np

if __name__ == '__main__':

    glasses = Glasses(None)
    try:
        while True:
            res, video = glasses.video.read()
            # print(glasses.pointer[0],glasses.pointer[1], glasses.pointer[2])
            video = cv2.circle(video, (int(960 + glasses.pointer[0]*100), int(540 - glasses.pointer[1] * 100)), radius=20, color=(0, 0, 255), thickness=-1) #gaze (1080p)
            cv2.waitKey(1)
            cv2.imshow("stream", video)


    except (KeyboardInterrupt, SystemExit):
    #     glasses.shutdown()
        pass