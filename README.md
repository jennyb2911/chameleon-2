# chameleon
Mini Face-recognition Client 简单的人脸识别端小脚本

## 环境
1. Python-3.4+
2. PostgreSQL-9.6.3
4. OpenCV3
5. dlib-19.4
6. docker-17.06（推荐）

## 起步
+ **搭建本机的 python3+opencv3+dlib 环境**

可以参考洋吴克的教程[这里]。(https://www.pyimagesearch.com/2017/04/17/real-time-facial-landmark-detection-opencv-python-dlib/)<br>
当然如果你嫌烦，或者机器真的有问题怎么也装不成功，那可以尝试我们自制的[docker镜像]。(https://hub.docker.com/r/adoo/python3-opencv3-dlib/)<br>

+ **运行**

如果你是直接用的本机环境，直接运行single-detector就可以了。eg: python3 single_detector.py -r rtsp://admin:admin123@192.168.2.95:554/h264/ch01/main/av_stream -s 0.88<br>
如果用docker，请运行﻿docker run -dit -v /your/code/path:/srv/chameleon --name face adoo/python3-opencv3-dlib 。

+ **视频源**

默认是调用本机的摄像头，用-r参数控制。同时也接受所有满足rtsp协议的视频源。详见single-detector line13 的注释说明。

+ **原理介绍**

[用深度学习识别人脸](https://zhuanlan.zhihu.com/p/24567586)<br>
此脚本也是用的欧式测距，128个特征值作为矩阵存放在了postgresql中（完全可以换nosql数据库）。

+ **导入数据**

可以利用 init_faces.py 导入你需要的人脸数据，源数据可以是满满一文件夹的头像。<br>
图片名就是这张脸的唯一名字。

## 一些错误提示
error1: https://stackoverflow.com/questions/32703296/dyld-library-not-loaded-usr-local-lib-libjpeg-8-dylib-homebrew-php





