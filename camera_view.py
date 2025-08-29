import cv2



camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not camera.isOpened():
	print("Failed to open camera.")
	exit()

print("Press ESC to exit.")

while True:
	ret, frame = camera.read()
	if not ret:
		print("Failed to capture frame.")
		break
	cv2.imshow("camera", frame)
	
	if cv2.waitKey(1) == 27:
		break
		
camera.release()
cv2.destroyAllWindows()

