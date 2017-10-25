# -*- coding: utf-8 -*-
import dlib
import cv2
import base64
from imutils import face_utils


class FrameCropper:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()

    def work(self, frame, callback):
        # 直接剪裁画面并处理
        recs = self.detector(frame, 1)
        if len(recs) >= 1:
            try:
                for (i, rect) in enumerate(recs):
                    (x, y, w, h) = face_utils.rect_to_bb(rect)
                    rect_img = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                    _, buffer = cv2.imencode('.jpg', rect_img)
                    # You can save images like this:
                    # cv2.imwrite('face.jpg', rect_img)
                    jpg_as_text = base64.b64encode(buffer)
                    callback(jpg_as_text)
                    return True
            except Exception:
                return False
        else:
            return False
