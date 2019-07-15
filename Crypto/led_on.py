import RPi.GPIO as GPIO
import time
import sys

N = 50
if len(sys.argv)==2:
	N = int(sys.argv[1])
	
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

for i in range(N):
	GPIO.output(16, GPIO.HIGH)
	time.sleep(.2)
	GPIO.output(16, GPIO.LOW)
	
# CLEAN UP ON EXIT
GPIO.cleanup()
print 'FINISHED FLASHING LED'
exit(0)
