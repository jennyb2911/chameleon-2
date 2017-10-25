import psycopg2
import config as c
import numpy as np
import time
import json
from scipy.special import expit


class Face:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=" + c.config["Db"]["dbname"] + " host=" + c.config["Db"]["Host"] + " port=" + c.config["Db"]["Port"])
        self.cur = self.conn.cursor()

    def get_feature_repo(self):
        self.cur.execute("SELECT id,name,feature,face_img FROM " + c.config["Db"]["table"] + " WHERE status=0")
        self.repo = self.cur.fetchall()

    def match(self, na, score=0.85):
        # Cache all database face features
        self.get_feature_repo()
        uid = 0
        tmp = 0
        most_face = ''
        face_img = ''
        for i in self.repo:
            distance = np.linalg.norm(na - i[2])
            conf = expit((6000 - distance) / 1000)
            if conf > tmp and conf >= score:
                uid = i[0]
                tmp = conf
                most_face = i[1]
                face_img = i[3]

        ret = {
            "id": uid,
            "name": most_face,
            "face_img": face_img,
            "attended_at": time.time(),
            "score": tmp,
            "status": 1
        }

        print(json.dumps(ret, ensure_ascii=False))

    def __del__(self):
        self.cur.close()
        self.conn.close()