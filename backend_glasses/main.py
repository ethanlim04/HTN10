from sensor import Glasses
import time
import cv2
import numpy as np
import math
import torch
import translators as ts
ts.translate_text("hello", translator='google', to_language='ko')

#Combined
# cam_mat = [[1.27488115e+03, 0.00000000e+00, 9.12894051e+02],
#  [0.00000000e+00, 1.28254108e+03, 5.31598120e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

# cam_disort = [[ 0.16586182, -0.61164189, -0.00499006, -0.00627141,  0.78180477]]

#OLD
cam_mat = [[1.25531919e+03, 0.00000000e+00, 9.34265450e+02],
 [0.00000000e+00, 1.26150217e+03, 5.34860321e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

cam_disort = [[ 1.09126656e-01, -4.24326297e-01,  3.87627821e-04 , 2.33006437e-03,
   4.83839339e-01]]


#NEW (Paper only)
# cam_mat = [[1.27336990e+03, 0.00000000e+00, 9.32543155e+02],
#  [0.00000000e+00, 1.27553680e+03, 5.31138609e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

# cam_disort = [[ 0.13225044, -0.44806734, -0.00187028,  0.0007114,   0.49178104]]

cam_mat = np.array(cam_mat)
cam_disort = np.array(cam_disort)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
classes = model.names
def score_frame(frame):
    """
    Takes a single frame as input, and scores the frame using yolo5 model.
    :param frame: input frame in numpy/list/tuple format.
    :return: Labels and Coordinates of objects detected by model in the frame.
    """
    frame = [frame]
    results = model(frame)
    labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    return labels, cord

def class_to_label(x):
    """
    For a given label value, return corresponding string label.
    :param x: numeric label
    :return: corresponding string label
    """
    return classes[int(x)]
def plot_boxes(results, frame, x, y):
    """
    Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
    :param results: contains labels and coordinates predicted by model on the given frame.
    :param frame: Frame which has been scored.
    :return: Frame with bounding boxes and labels ploted on it.
    """
    labels, cord = results
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]
    for i in range(n):
        row = cord[i]
        if row[4] >= 0.3:
            x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
            bgr = (0, 255, 0)
            if((x1 <= x and x <= x2 and y1 <= y and y <= y2)):
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                # ts.translate_text("AA", translator='google', to_language='en')
                # cv2.putText(frame, class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
                cv2.putText(frame, ts.translate_text(class_to_label(labels[i]), translator='google', to_language='fr'), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

    return frame


if __name__ == '__main__':

    glasses = Glasses(None)
    try:
        while True:
            res, video = glasses.video.read()

            coords = np.array([glasses.pointer[0], -glasses.pointer[1], -glasses.pointer[2]])
            # if(not (math.isnan(coords[0]) or math.isnan(coords[1]) or math.isnan(coords[2]) or (coords[0] == 0 or coords[1] == 0 or coords[2] == 0))):

            if(not glasses.evalmode):
                try:
                    pts, jac = cv2.projectPoints(coords, np.eye(3), np.array([0.0, 0.0, 0.0]), cam_mat, cam_disort)
                    # print("POINTS", pts)
                    # video = cv2.circle(video, (pts[0][0].astype(int)[0] - 250, pts[0][0].astype(int)[1] - 150), radius=20, color=(0, 0, 255), thickness=-1) #gaze (1080p)
                    ptx = pts[0][0].astype(int)[0] - 150
                    pty = pts[0][0].astype(int)[1] - 250
                    if (glasses.wink):
                        results = score_frame(video)
                        video = plot_boxes(results, video, ptx, pty)
                    video = cv2.circle(video, (ptx, pty), radius=20, color=(0, 0, 255), thickness=-1) #gaze (1080p)
                except:
                    if(glasses.frame - glasses.lasteval > 100):
                        print("Eval mode enabled")
                        glasses.evalmode = True
                        glasses.lasteval = glasses.frame
            else:
                try:
                    pts, jac = cv2.projectPoints(coords, np.eye(3), np.array([0.0, 0.0, 0.0]), cam_mat, cam_disort)
                    # print("POINTS", pts)
                    # video = cv2.circle(video, (pts[0][0].astype(int)[0] - 250, pts[0][0].astype(int)[1] - 150), radius=20, color=(0, 0, 255), thickness=-1) #gaze (1080p)
                    ptx = pts[0][0].astype(int)[0]
                    pty = pts[0][0].astype(int)[1]


                    if(not glasses.evalCalibrated and glasses.frame - glasses.lasteval > 150):
                        glasses.calibX = ptx
                        glasses.calibY = pty
                        glasses.evalCalibrated = True
                        print("Calibbration Complete")
                    print(ptx - glasses.calibX, pty - glasses.calibY, glasses.calibX, glasses.calibY)
                    # video = cv2.circle(video, (450 - glasses.calibX + ptx, 550 - glasses.calibY + pty), radius=20, color=(0, 0, 255), thickness=-1) #gaze (1080p)
                    video = cv2.circle(video, (ptx, pty), radius=20, color=(0, 0, 255), thickness=-1) #gaze (1080p)
                except:
                    if(glasses.frame - glasses.lasteval > 100):
                        print("Eval mode disabled")
                        glasses.evalmode = False
                        glasses.evalCalibrated = False
                        glasses.lasteval = glasses.frame


            # results = score_frame(video)
            # video = plot_boxes(results, video)

            cv2.waitKey(1)
            

            cv2.imshow("stream", video)


    except (KeyboardInterrupt, SystemExit):
        glasses.shutdown()
        # pass