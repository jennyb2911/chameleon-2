# -*- coding: utf-8 -*-
import dlib
import cv2
# import numpy as np
# import psycopg2
# import json
# import time
import base64
# import config as c
# from scipy.special import expit
from imutils import face_utils

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./shape/shape_predictor_68_face_landmarks.dat')
recognition = dlib.face_recognition_model_v1('./shape/dlib_face_recognition_resnet_model_v1.dat')

qt = 1

class Inside(object):

    def frame_sketch(self, frame, qfunc):
        global qt
        recs = detector(frame, 1)
        if len(recs) >= 1:
            try:
                for (i, rect) in enumerate(recs):
                    (x, y, w, h) = face_utils.rect_to_bb(rect)
                    rect_img = frame[y - 10: y + h + 10, x - 10: x + w + 10]

                    _, buffer = cv2.imencode('.jpg', rect_img)
                    cv2.imwrite(str(qt) + '.jpg', rect_img)
                    qt = qt + 1
                    jpg_as_text = base64.b64encode(buffer)
                    qfunc(jpg_as_text)
                    return True
            except Exception as e:
                return False
        else:
            return False


    # 不使用自用remark
    # def feature_calc(self, frame, qfunc):
    #     # get feature
    #     recs = detector(frame, 1)
    #     if len(recs) >= 1:
    #         for r in recs:
    #             shape = predictor(frame, r)
    #             # landmarks
    #             face_descriptor = recognition.compute_face_descriptor(frame, shape)
    #             int_arr = np.array([int(x * 10000) for x in face_descriptor])
    #             qfunc(json.dumps(int_arr.tolist(), ensure_ascii=False))
    #         return True
    #     else:
    #         return False


    # def __init__(self):
        # self.conn = psycopg2.connect("dbname=" + c.config["Db"]["dbname"] + " host=" + c.config["Db"]["Host"] + " port=" + c.config["Db"]["Port"])
        # self.cur = self.conn.cursor()


    # def get_feature_repo(self):
    #     self.cur.execute("SELECT id,name,feature,face_img FROM " + c.config["Db"]["table"] + " WHERE status=0")
    #     self.repo = self.cur.fetchall()


    # def match(self, frame, score):
    #     self.get_feature_repo()
    #     b, na = self.feature_calc(frame)
    #     id = 0
    #     tmp = 0
    #     most_face = ''
    #     face_img = ''
    #     if b:
    #         for i in self.repo:
    #             distance = np.linalg.norm(na - i[2])
    #             conf = expit((6000 - distance) / 1000)
    #             if conf > tmp and conf >= score:
    #                 id = i[0]
    #                 tmp = conf
    #                 most_face = i[1]
    #                 face_img = i[3]
    #
    #     ret = {
    #         "id": id,
    #         "name": most_face,
    #         "face_img": face_img,
    #         "attended_at": time.time(),
    #         "score": tmp,
    #         "status": 1
    #     }
    #
    #     return json.dumps(ret, ensure_ascii=False)


    # def __del__(self):
    #     self.cur.close()
    #     self.conn.close()