import cv2
import numpy as np
import picar
import time

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


try:
    while True:
        ret, frame = camera.read()
        if not ret:
            continue
        
        roi = frame[120:240, :]
        
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        
        _, binary = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        
        
        contours,_ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            line = cv2.moments(largest_contour)
            if line ["m00"] != 0:
                x = int(line["m10"] / line["m00"])
                y = int(line["m01"] / line["m00"])
                
                cv2.circle(frame, (x, 120+y), 5, (0, 255, 0), -1)
        
        
        cv2.imshow("Camera", frame)
        
        
        if cv2.waitKey(1) == 27:
            break
        
finally:
    camera.release()
    cv2.destoryALLWindows()
    
        