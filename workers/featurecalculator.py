# -*- coding: utf-8 -*-
import dlib
import numpy as np


class FeatureCalculator:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('./shape/shape_predictor_68_face_landmarks.dat')
        self.recognition = dlib.face_recognition_model_v1('./shape/dlib_face_recognition_resnet_model_v1.dat')

    def work(self, frame, callback):
        # 计算128位特征值
        recs = self.detector(frame, 1)
        if len(recs) >= 1:
            for r in recs:
                shape = self.predictor(frame, r)
                # landmarks
                face_descriptor = self.recognition.compute_face_descriptor(frame, shape)
                int_arr = np.array([int(x * 10000) for x in face_descriptor])
                callback(int_arr)
            return True
        else:
            return False


