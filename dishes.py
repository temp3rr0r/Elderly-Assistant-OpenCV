import cv2
import numpy as np

#calculate the average brightness of an image
#used to work out if its night time and turn the alarms off
def getMeanBrightness(img):	
	
	# Return the mean Val/Brightness from the HSV colour space of the image
	return cv2.mean(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:,:,2])[0]

def main():
	
        cap = cv2.VideoCapture(-1) # Load default video capture device
	ret, frame = cap.read() # Load one frame from capture device
	
	#cv2.imwrite('border3.png',frame) # Store frame as png
	meanBrightness = getMeanBrightness(frame)
	print("Mean Brightness: " + str(meanBrightness))

	if meanBrightness < 30:
		pring("Exiting, too low brightness")
		exit()

	thresholdCanny = 200
	grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Create grayscale image
	edges = cv2.Canny(grayScale, thresholdCanny, thresholdCanny /2, 3) # Edge detection
	smoothEdges = cv2.GaussianBlur(grayScale, (3, 3), 0)# Smooth edges
	#houghCircles = cv2.HoughCircles(grayScale, cv2.HOUGH_GRADIENT, 2, grayScale.width / 18, thresholdCanny, 300, 0, 0)# TODO: Find hough circles

	circles = cv2.HoughCircles(grayScale, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=thresholdCanny, minRadius=0, maxRadius=0)

	if circles is not None:
		print "Circles found: " + str(len(circles))
		print "Circles array: "
		print circles

		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
			cv2.circle(grayScale,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle
			cv2.circle(grayScale,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle

	cv2.imwrite('grayScale.png', grayScale) # Store frame as png
	cv2.imwrite('edges.png', edges) # Store frame as png
	cv2.imwrite('smoothEdges.png', smoothEdges) # Store frame as png

	cap.release()
	cv2.destroyAllWindows()

main()
