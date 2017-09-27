# -*- coding: utf-8 -*-
import dlib
import numpy as np
import psycopg2
import json
import time
import config as c
from scipy.special import expit

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./shape/shape_predictor_68_face_landmarks.dat')
recognition = dlib.face_recognition_model_v1('./shape/dlib_face_recognition_resnet_model_v1.dat')

class Inside(object):

    def feature_calc(self, frame):
        # get feature
        recs = detector(frame, 1)
        if len(recs) >= 1:
            shape = predictor(frame, recs[0])
            # landmarks
            face_descriptor = recognition.compute_face_descriptor(frame, shape)
            int_arr = np.array([int(x * 10000) for x in face_descriptor])
            return True, int_arr
        else:
            return False, None


    def __init__(self):
        self.conn = psycopg2.connect("dbname=" + c.config["Db"]["dbname"] + " host=" + c.config["Db"]["Host"] + " port=" + c.config["Db"]["Port"])
        self.cur = self.conn.cursor()


    def get_feature_repo(self):
        self.cur.execute("SELECT id,name,feature,face_img FROM " + c.config["Db"]["table"] + " WHERE status=0")
        self.repo = self.cur.fetchall()


    def match(self, frame, score):
        self.get_feature_repo()
        b, na = self.feature_calc(frame)
        id = 0
        tmp = 0
        most_face = ''
        face_img = ''
        if b:
            for i in self.repo:
                distance = np.linalg.norm(na - i[2])
                conf = expit((6000 - distance) / 1000)
                if conf > tmp and conf >= score:
                    id = i[0]
                    tmp = conf
                    most_face = i[1]
                    face_img = i[3]

        ret = {
            "id": id,
            "name": most_face,
            "face_img": face_img,
            "attended_at": time.time(),
            "score": tmp,
            "status": 1
        }

        return json.dumps(ret, ensure_ascii=False)


    def __del__(self):
        self.cur.close()
        self.conn.close()