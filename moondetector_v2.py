from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils	
import time
import cv2
# from opencv_contrib_python import cv2
import numpy as np


# print(cv2.__version__)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
"""
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}
"""

# grab the appropriate object tracker using our dictionary of
# OpenCV object tracker objects
#tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
# tracker = cv2.TrackerMIL_create()
tracker = cv2.TrackerCSRT_create()

# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

"""
# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
"""
vs = cv2.VideoCapture("moon_timelapse_nuage_1080.mp4")
# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
i = 0
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	grabbed, frame = vs.read()
	#
	#  check if the frame was successfully grabbed
	if not grabbed:
		print("[INFO] Unable to grab a frame. End of video")
		break
	#frame = frame[1] if args.get("video", False) else frame
	# check to see if we have reached the end of the stream
	if frame is None:
		print("Breaking")
		break
	# resize the frame (so we can process it faster) and grab the
	# frame dimensions
	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]

	# check to see if we are currently tracking an object
	if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)
		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
		# update the FPS counter
		fps.update()
		fps.stop()
		# initialize the set of information we'll be displaying on
		# the frame
		info = [
			("Tracker", args["tracker"]),
			("Success", "Yes" if success else "No"),
			("FPS", "{:.2f}".format(fps.fps())),
		]
		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if i % 100 == 0:
		
		# Try to detect the moon in the frame
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #gray_scale the image
		_, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY) #threshold the image
		gray = cv2.GaussianBlur(gray, (3, 3), 0) #blur the grayscale image
		
		# cv2.imshow("mask", thresh)
		
		
		#detecting circles
		moon = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 300, param1=300, param2=10, minRadius=10, maxRadius=40)
		moon = moon[0][0]
		moon = np.uint16(np.around(moon))

		cv2.circle(frame, (moon[0], moon[1]), moon[2], (0, 255, 255), 2) 
		alpha = 1.2 #Parameter for the square around the moon
		print_rect = [moon[0]-alpha*moon[2], moon[0]+alpha*moon[2], moon[1]-alpha*moon[2], moon[1]+alpha*moon[2]]
		print_rect = tuple(map(int, print_rect))
		print_rect = np.uint16(np.around(print_rect))
		cv2.rectangle(frame, (print_rect[0], print_rect[2]), (print_rect[1], print_rect[3]), (255, 255, 0), 2)
		# print("Detection =", type(print_rect[0]), print_rect)

		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		# initBB_select = cv2.selectROI("Frame", frame, fromCenter=False,
		# 	showCrosshair=True)
		initBB = [moon[0]-alpha*moon[2], moon[1]-alpha*moon[2], 2*alpha*moon[2], 2*alpha*moon[2]]
		initBB = list(map(int, initBB))
		# print(f"Selection = {type(initBB_select)},  {initBB_select}")
		# print(f"Automatic = {type(initBB)},  {initBB}")

		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		tracker.init(gray, initBB)
		fps = FPS().start()
	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

	i += 1
"""
# if we are using a webcam, release the pointer
if not args.get("video", False):
	vs.stop()

# otherwise, release the file pointer
else:
"""
vs.release()	
# close all windows
cv2.destroyAllWindows()