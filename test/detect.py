import cv2
import numpy as np
import dlib
import imutils
from imutils import face_utils
from imutils.video import WebcamVideoStream


def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    # return a tuple of (x, y, w, h)
    return (x, y, w, h)


def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('../shape/shape_predictor_68_face_landmarks.dat')
recognition = dlib.face_recognition_model_v1('../shape/dlib_face_recognition_resnet_model_v1.dat')

vs = WebcamVideoStream(src='rtsp://admin:admin123@192.168.2.96:554/h264/ch01/main/av_stream').start()

Q = 1

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)
    if len(rects) >= 1:
        for (i, rect) in enumerate(rects):
            # convert dlib's rectangle to a OpenCV-style bounding box
            # [i.e., (x, y, w, h)], then draw the face bounding box
            (x, y, w, h) = rect_to_bb(rect)

            # cv2.rectangle(frame, (x - w * 0.2, y - h * 0.2), (x + w * 1.2, y + h * 1.2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0), 2)
            rect_img = frame[y - 10: y+h+10, x-10: x+w+10]
            # _, buffer = cv2.imencode('.jpg', rect_img)
            # cv2.imwrite(str(Q) + '.jpg', rect_img)
            # Q = Q + 1

    cv2.imshow("AAA", frame)
    key = cv2.waitKey(1) & 0xFF


cv2.destroyAllWindows()
vs.stop()
