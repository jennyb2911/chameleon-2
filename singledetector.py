# you can call me chameleon
from __future__ import print_function
from imutils.video import WebcamVideoStream
from workers import framecropper
from workers import featurecalculator
from sql import face

import argparse
import imutils
import cv2
import platform
import config as c
import stp

####### Commandline parameters #######
newParser = argparse.ArgumentParser()
# stream source location
# eg: I use HIKVISION IPCAM for capturing frames,
# so I set VideoStream Source(-r) as `rtsp://admin:admin123@192.168.1.91:554/h264/ch01/main/av_stream`.
# If you have a local-cam, you can set -r 0
newParser.add_argument("-r", "--resource", dest="resource", help="Select a Input Frame Resource Link")
# If you use Face-local-worker to recognize faces,
# you should set score for filtering miss-matched faces.
newParser.add_argument("-s", "--score", dest="score", help="Set an underscore of Face-match")
args = newParser.parse_args()

if args.resource is None:
    print("Please set an input frame resource.")
    exit(0)
elif args.resource == '0':
    args.resource = 0

if args.score is None:
    args.score = c.config['Standard']['Score']

print("[START]...")

if __name__ == '__main__':
    # Stomp Broker
    mqueue = stp.Messenger(host=c.config['Aq']['Host'], destination=c.config['Aq']['Destination'])
    # VideoCapture
    vs = WebcamVideoStream(src=args.resource).start()

    # Method1 Crop Frame and send it
    worker = framecropper.FrameCropper()
    callback = mqueue.addqueue

    # Method2 1:n Face recognize locally
    # worker = featurecalculator.FeatureCalculator()
    # facemodel = face.Face()
    # callback = facemodel.match

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

        if frame is not None:
            print(worker.work(frame, callback))

        # display on the screen
        if platform.system() != 'Linux':
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

    # cleanup
    cv2.destroyAllWindows()
    vs.stop()