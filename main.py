import cv2
import numpy as np
import picar
import time

time.sleep(0)

class PID:
    def __init__(self):
        self.kp = 0.1
        self.ki = 0.0
        self.kd = 0.01
        self.prev_error = 0.0
        self.integral = 0.0
        self.speed = 45
        self.smooth_factor = 0.3
        self.max_angle_delta = 10
        self.threshold = 100
        
        
    def compute(self, error):
        self.integral += error
        derivative = error - self.prev_error
        self.output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.output = error
        return self.output
    
# Setup Car
picar.setup()
fw = picar.front_wheels.Front_Wheels()
bw = picar.back_wheels.Back_Wheels()

pid = PID()

fw.offset = 0
fw.turn(90)
bw.speed = 0
bw.backward()
prev_angle = 90
prev_cx = 640/2
    
    
# Setup Camera
camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
center = 320


try:
    while True:
        # Detectlane 
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
                # Find Center
                x = int(line["m10"] / line["m00"])
                y = int(line["m01"] / line["m00"])
                
                cx_smoothed = (1 - pid.smooth_factor) * prev_cx + pid.smooth_factor * center
                
                prev_cx = cx_smoothed
                
                
                error = x - cx_smoothed
                # Correct only if error is larger than threshold
                if abs(error) > pid.threshold:
                    correction = pid.compute(error)
                else:
                    correction = 0
                steering = 90 + correction
                # Limit steering angle to 60-120 degree
                steering = max(60, min(120, steering))
                # Steering angle only change by max_angle_delta each time
                if abs(steering - prev_angle) > pid.max_angle_delta:
                    if steering > prev_angle:
                        new_angle = prev_angle + pid.max_angle_delta
                    else:
                        new_angle = prev_angle - pid.max_angle_delta
                else:
                    new_angle = steering
                prev_angle = new_angle
                fw.turn(new_angle)
                
                
                 
                
                cv2.circle(frame, (x, 120+y), 5, (0, 255, 0), -1)
        
        
        
        cv2.imshow("Camera", frame)
        bw.speed = pid.speed
        
        
        if cv2.waitKey(1) == 27:
            bw.speed = 0
            bw.stop()
            break
        
finally:
    camera.release()
    cv2.destoryALLWindows()
    bw.speed = 0
    bw.stop()
    
        