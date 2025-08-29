import picar
from picar import front_wheels, back_wheels
import time

picar.setup()

fw = front_wheels.Front_Wheels()
bw= back_wheels.Back_Wheels()
print("testing wheels")

try:
	print("Turning left")
	fw.turn(60)
	time.sleep(10)
	
	print("Turning right")
	fw.turn(120)
	time.sleep(10)
	
	print("Centering")
	fw.turn(90)
	time.sleep(10)
	
	print("Driving forward")
	bw.speed = 50
	bw.forward()
	time.sleep(20)

	print("Driving backward")
	bw.speed = 50
	bw.backward()
	time.sleep(20)
	
	
	print("stopping")
	bw.stop()
	
except KeyboardInterrupt:
	print("Interrupted, stopping...")
	bw.stop()
	
finally:
	bw.stop()
	
