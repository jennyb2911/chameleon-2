# -*- coding: utf-8 -*-
# import the necessary packages
import numpy as np
import os
import cv2
import dlib
import psycopg2
import argparse
import config as c

newParser = argparse.ArgumentParser()
# newParser.add_argument("-d", "--database address", dest="database", help="Select a Local Database")
newParser.add_argument("-f", "--File Directory", dest="directory", help="Choose a Directory which contains Face-images")
args = newParser.parse_args()

if args.directory is None:
    print('No Face-Directory')
    exit(0)

# Face
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./shape/shape_predictor_68_face_landmarks.dat')
recognition = dlib.face_recognition_model_v1('./shape/dlib_face_recognition_resnet_model_v1.dat')

# construct the argument parser and parse the arguments

def feature_calc(frame):
    recs = detector(frame, 1)
    if len(recs) >= 1:
        shape = predictor(frame, recs[0])
        # landmarks
        face_descriptor = recognition.compute_face_descriptor(frame, shape)
        int_arr = np.array([int(x * 10000) for x in face_descriptor])
        return True, int_arr
    else:
        return False, None


def add_face_db(n, f, fn):
    try:
        cur.execute("INSERT INTO " + c.config["Db"]["table"] + "(name, feature, face_img) VALUES (%s, %s, %s)", (n, f, fn))
        print('Add ' + n + ' Successfully')
    except Exception as e:
        print(n + ' insert failed')
        print(str(e))

def init_faces(dir):
    for filename in os.listdir(dir):
        remark = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        try:
            if ext == '.jpg' or ext == '.jpeg' or ext == '.png':
                frame = cv2.imread(dir + '/' + filename)
                b, np = feature_calc(frame)
                if b :
                    add_face_db(remark, np.tolist(), filename)
        except Exception as e:
            print(filename + str(e))
            continue

if __name__ == '__main__':
    conn = psycopg2.connect("dbname=" + c.config["Db"]["dbname"] + " host=" + c.config["Db"]["Host"] + " port=" + c.config["Db"]["Port"])
    cur = conn.cursor()
    init_faces(args.directory)
    conn.commit()
    cur.close()
    conn.close()