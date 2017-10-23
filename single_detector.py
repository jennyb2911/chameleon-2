# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from classifier import inside

import argparse
import imutils
import cv2
import platform
import config as c
import stp

# stream source location
# eg: I use HIKVISION IPCAM for captruing frames, so I set VideoStream Source as `rtsp://admin:admin123@192.168.1.91:554/h264/ch01/main/av_stream`
# WebcamVideoStream(src=<HIKVISION-SOURCE-URL>).start()
# local = 0
# rtsp = 'rtsp://admin:admin123@192.168.2.95:554/h264/ch01/main/av_stream'

newParser = argparse.ArgumentParser()
newParser.add_argument("-r", "--resource", dest="resource", help="Select a Input Frame Resource Link")
newParser.add_argument("-s", "--score", dest="score", help="Set an underscore of Face-match")
args = newParser.parse_args()

mqueue = stp.Messenger(host=c.config['Stomp']['Host'], destination=c.config['Stomp']['Destination'])

if args.resource is None:
    print("Pls set an input frame resource.")
    exit(0)
elif args.resource == '0':
    args.resource = 0

if args.score is None:
    args.score = c.config['Standard']['Score']

print("[capture start]...")

vs = WebcamVideoStream(src=args.resource).start()

def face_request(frame, classifier=None):
    '''
    Send your frame into the classifier
    #### You can save your frame to check if base64 works well ####
    imgdata = base64.b64decode(str(ls, encoding = "utf-8"))
    file = open('2.jpg', 'wb')
    file.write(imgdata)
    file.close()
    ####
    :param frame:
    :param classifier:
    :return:
    '''
    # eg1: match face locally and give the result
    # s = float(args.score)
    # res = classifier.match(frame, s)
    # print(res)

    # eg2: match and offer the vector array
    # b, res = classifier.feature_calc(frame)
    res = classifier.frame_sketch(frame, qfunc=mqueue.addQueue)
    print(res)


if __name__ == '__main__':

    classifier = inside.Inside()

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        face_request(frame, classifier)

        # display on the screen
        if platform.system() != 'Linux':
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()