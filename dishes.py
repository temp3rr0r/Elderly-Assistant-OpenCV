import cv2
import numpy as np
import datetime
import sqlite3
import time

sleepInterval = 60 * 60 # 60 minutes
verbose = False

def saveDishesCountDb(brightness, dishes):
	conn = sqlite3.connect('dishes.db')
	c = conn.cursor()
	c.execute("INSERT INTO dishes VALUES (?, ?, ?)",(datetime.datetime.now(), brightness, dishes) )
	conn.commit()
	conn.close()


# Calculate the average brightness of an image
def getMeanBrightness(img):		
	# Return the mean Val/Brightness from the HSV colour space of the image
	return cv2.mean(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:,:,2])[0]

def main():
	
	while True: # Loop forever, sleep every sleepInterval
	        cap = cv2.VideoCapture(-1) # Load default video capture device
		ret, frame = cap.read() # Load one frame from capture device
	
		meanBrightness = getMeanBrightness(frame)
		if verbose:
			print("Mean Brightness: " + str(meanBrightness))

		if meanBrightness < 30:
			if verbose:
				print("Exiting, too low brightness")
			exit()

		thresholdCanny = 200
		grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Create grayscale image
		grayScale = cv2.GaussianBlur(grayScale, (9, 9), 0) # Smooth edges	
		circles = cv2.HoughCircles(grayScale, cv2.HOUGH_GRADIENT, \
			# Inverse ratio of resolution
			 1,\
			# Minimum distance between centers
			20,\
			# Upper threshold for the internal Canny Edge detector
			param1=200, \
			# Threshold for center detection
			param2=100, \
			minRadius=0, \
			maxRadius=0)

		if circles is not None:
			if verbose:
				print "Circles found: " + str(len(circles[0]))
				print "Circles array: "
				print circles
			saveDishesCountDb(meanBrightness, len(circles[0]))

			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle
				cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle

		cv2.imwrite('frame.png', frame) # Store frame as png

		cap.release()
		cv2.destroyAllWindows()
		time.sleep(sleepInterval)
main()
