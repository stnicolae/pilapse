from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import RPi.GPIO as GPIO
import time
import signal, os, subprocess

#kill conflicting gpho2 process
def killgphoto2Process():
	p=subprocess.Popen(['ps'], '-A', stdout=subprocess.PIPE)
	out, err = p.communicate()
	
	#find process to kill
	for line in out.splitlines():
		if b'gvfsd-gphoto2' in line:
			pid = int(line.split(None,1) [0])
			os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = "PiShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Desktop/timelapse/images/" + folder_name

def createSaveFolder():
	try:
		os.makedirs(save_location)
	except:
		#print("Failed to create new directory")
		exception = True
	
	os.chdir(save_location)
	
def captureImages():
	gp(triggerCommand)
	sleep(3)
	gp(downloadCommand)
	gp(clearCommand)
	
def renameFiles(ID):
	for filename in os.listdir("."):
		if len(filename) < 13:
			if filename.endswith(".JPG"):
				os.rename(filename, (shot_time + ID + ".JPG"))
				print("Renamed JPG")
			elif filename.endswith(".CR2"):
				os.rename(filename, (shot_time + ID + ".CR2"))
				print("Renamed CR2")

#killgphoto2Process()
gp (clearCommand)

while True:
	shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	createSaveFolder()
	captureImages()
	renameFiles(picID)
	sleep (5)
		

	
#scan distance to printer head
GPIO.setmode(GPIO.BOARD)

TRIG = 7
ECHO = 12

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(ECHO, GPIO.IN)

time.sleep(0.1)

print ("Starting measure...")

GPIO.output(TRIG,1)
time.sleep(0.00001)
GPIO.output(TRIG,0)

while GPIO.input(ECHO) ==0:
	pass

start = time.time()

while GPIO.input(ECHO) ==1:
	pass
	
stop = time.time()

print ((stop - start) * 17000)

GPIO.cleanup()

