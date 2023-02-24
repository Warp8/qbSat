#YOU NEED TO INSTALL THE PYTHON MODULE "EVENTLET" FOR THIS TO WORK.
#It will execute without it, but won't run correctly which is why I mention it here.

#By default this script will run at startup, if you want to change this for development, set this to "False".
runAtStartup = True
#This changes the amount of time, in seconds, between each "snapshot", including data and photos.
timeBetweenSnapshots = 1.5
#This value cannot be below about 1 second because the time to take photos from both cameras is a little less than one second

if runAtStartup == False:
    quit()

#Import General Libraries
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from picamera import PiCamera
from datetime import datetime
from enviroplus import gas
import RPi.GPIO as GPIO
import threading
import asyncio
import base64
import time
import csv
import os

#Import Sensors
from bme280 import BME280 # Temperature / Pressure / Humidity Sensor
from ltr559 import LTR559 # Lights / Proximity

#Setup Sensor Variables
bme280 = BME280()
ltr559 = LTR559()

#Setup Server Variables
app = Flask(__name__, template_folder="qbSat/templates", static_folder="qbSat/static")
app.config["SECRET_KEY"] = "CubeSats!"
socket = SocketIO(app, logger=False, engineio_logger=False) #Disable these diagnostics for possible better performance on final build.

#Setup Camera Variables for consistent photos
camera = PiCamera(resolution=(800, 600))
g = 0

#GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17 , GPIO.OUT)
GPIO.setup(4 , GPIO.OUT)
time.sleep(0.5) #Time for setup to take effect

#Setup Global Variables
global currentConnections
currentConnections = 0
global activeRecord
activeRecord = False
global currentlyTakingPhotos
currentlyTakingPhotos = False
global currentlyWriting
currentlyWriting = False
global startTime
startTime = time.time()

#Define general functions.

def millis():
    return round((time.time()-startTime)*1000)
#Gives the time since the script started in milliseconds, this is really useful because some functions don't execute instantly, so you can't trust sleep() accurately.

def SwitchCamera(camera):
    if camera == 1:
        try:
            print("Selecting Camera A")
            os.system("sudo i2cset -y 0 0x70 0x00 0x01")
            GPIO.output(17, GPIO.LOW)
            GPIO.output(4, GPIO.LOW)
        except:
            print("Failure to select Camera A")
    elif camera == 2:
        try:
            print("Selecting Camera B")
            os.system("sudo i2cset -y 0 0x70 0x00 0x02")
            GPIO.output(17, GPIO.LOW)
            GPIO.output(4, GPIO.HIGH)
        except:
            print("Failure to select Camera B")
    else:
        print("Invalid Input, please select Camera A or Camera B, 1 or 2")

def recording(): #Sets up the recording function as a thread so it can be executed in the background
    global activeRecord #You need to say that it's global in each function where you use it.
    global currentlyTakingPhotos
    global currentlyWriting
    global timeBetweenSnapshots
    frame = 0
    with open("qbSat/static/recordings/current-recording/Readings.csv", mode="w") as readingsFile:
        currentlyWriting = True #Tells other parts of the program when there is readings being taken.
        file = csv.writer(readingsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file.writerow(["Time", "Humidity", "Pressure", "Temperature", "Light", "Oxidizing", "Reducing", "NH3"])
        while activeRecord == True:
            if (millis()%(1000*timeBetweenSnapshots)<=2):
                frame += 1 
                now = datetime.now() 
                current_time = now.strftime("%m-%d-%Y_%I:%M:%S")
                
                readings = [
                    current_time, 
                    str(round(bme280.get_humidity(), 2))+" %",
                    str(round(bme280.get_pressure(), 2))+" hPa",
                    str(round(bme280.get_temperature(), 2))+" C",
                    str(round(ltr559.get_lux(), 2))+" Lux",
                    str(round((gas.read_all().oxidising / 1000), 2))+" kO",
                    str(round((gas.read_all().reducing / 1000), 2))+" kO",
                    str(round((gas.read_all().nh3 / 1000), 2))+" kO"
                ] #this is messy im sorry lmao

                file.writerow(readings)
                if currentConnections >= 1: #This is to prevent it from taking photos more than it has to.
                    while True:
                        if currentlyTakingPhotos == False: #If it tries to copy the temporary images while they're being captured, it makes an empty file.
                            try:
                                os.system("sudo cp qbSat/live-images/CameraA.jpg qbSat/static/recordings/current-recording/CameraA/{:05d}.jpg".format(frame))
                            except:
                                print("Failure to copy images from Camera A")
                            try:
                                os.system("sudo cp qbSat/live-images/CameraB.jpg qbSat/static/recordings/current-recording/CameraB/{:05d}.jpg".format(frame))
                            except:
                                print("Failure to copy images from Camera B")
                            break
                else:
                    try:
                        SwitchCamera(1)
                        time.sleep(0.1) #time to let the i2c bus settle
                        camera.awb_gains = g
                        camera.annotate_text = "Camera A"
                        camera.capture("qbSat/static/recordings/current-recording/CameraA/%05d.jpg" % frame, format="jpeg", quality=12)
                    except:
                        print("Failure to capture from Camera A")
                    try:
                        SwitchCamera(2)
                        time.sleep(0.1)
                        camera.awb_gains = g
                        camera.annotate_text = "Camera B"
                        camera.capture("qbSat/static/recordings/current-recording/CameraB/%05d.jpg" % frame, format="jpeg", quality=12)
                    except:
                        print("Failure to capture from Camera B")
        readingsFile.close()
        currentlyWriting = False

def jpgToB64(path):
    with open(path, "rb") as img:
        img64 = "data:image/jpg;base64, " + str(base64.b64encode(img.read()).decode("ascii")) #Converts image to base64, reformates and adds meta data.
        return(img64)

def sendData():
    global currentConnections
    g = camera.awb_gains #Stops white balance from constantly changing.
    while (currentConnections >= 1):
        socket.sleep(0) #This lets other stuff happen while this function is being looped. Probably not super effiecient but I don't care we're launching this tomorrow.
        if (millis()%(1000*timeBetweenSnapshots)<=2):
            takePhotos() #This function takes over 900 milliseconds to take photos, so we cannot take photos any faster than about 1000 milliseconds
            socket.emit("visibleLight", jpgToB64("qbSat/live-images/CameraA.jpg"))
            socket.emit("infraRed", jpgToB64("qbSat/live-images/CameraB.jpg"))
            socket.emit("Humidity", (round(bme280.get_humidity(), 2)))
            socket.emit("Pressure", (round(bme280.get_pressure(), 2)))
            socket.emit("Temperature", (round(bme280.get_temperature(), 2)))
            socket.emit("Light", (round(ltr559.get_lux(), 2)))
            socket.emit("Oxidized", (round((gas.read_all().oxidising / 1000), 2)))
            socket.emit("Reduced", (round((gas.read_all().reducing / 1000), 2)))
            socket.emit("NH3", (round((gas.read_all().nh3 / 1000), 2)))
            print("Number of connected clients: ", currentConnections)
            print("Number of active threads: ", threading.active_count())

def takePhotos():
    global currentlyTakingPhotos
    global timeBetweenSnapshots
    if currentlyTakingPhotos == False:
        currentlyTakingPhotos = True
        try:
            SwitchCamera(1)
            socket.sleep(0.1) #time to let the i2c bus settle
            camera.awb_gains = g
            camera.annotate_text = "Camera A"
            camera.capture("qbSat/live-images/CameraA.jpg", format="jpeg", quality=12)
        except:
            print("Failure to capture from Camera A")
        try:
            SwitchCamera(2)
            socket.sleep(0.1)
            camera.awb_gains = g
            camera.annotate_text = "Camera B"
            camera.capture("qbSat/live-images/CameraB.jpg", format="jpeg", quality=12)
        except:
            print("Failure to capture from Camera B")
        currentlyTakingPhotos = False

#@app.route is for serving the html webpages.

@app.route("/")
def index():
    return render_template("Home.html")

@app.route("/Downloads")
def downloads():
	return render_template("Downloads.html")

@app.route("/Advanced")
def advanced():
	return render_template("Advanced.html")

#@socket.on is for processing incoming web sockets.

@socket.on("connect") 
def connection():
    socket.emit("confirmConnect") #You can't start a loop on the first connect event for some reason.
    if activeRecord == True:
        socket.emit("recordingIndicatorOn")
    else:
        socket.emit("recordingIndicatorOff")
    global currentConnections
    currentConnections += 1 

@socket.on("disconnect")
def disconnect():
    print("WebSocket Connection Closed")
    global currentConnections
    currentConnections -= 1

@socket.on("confirmConnect")
def confirmConnect():
    print("New WebSocket Connection Established")
    global currentConnections
    if currentConnections == 1: #Makes sure to only run the transmitting code when one client is connected, but sometimes this doesn't work idk why
        sendData()

@socket.on("deleteCommand")
def deleteCommand():
    print("Delete command recieved")
    os.system("sudo rm qbSat/static/recordings/downloads/*")
    os.system("sudo rm qbSat/static/recordings/recordingIndex.txt")
    os.system('cd qbSat/static/recordings && echo "Error, no files found" > recordingIndex.txt && cd -')

@socket.on("rebootCommand")
def rebootCommand():
    print("Reboot command recieved")
    os.system("sudo reboot")

@socket.on("recordToggle")
def recordToggle():
    global currentlyWriting
    print("Record Toggle Signal Recieved")
    global recording
    recordingThread = threading.Thread(target=recording)
    global activeRecord
    if activeRecord == True:
        activeRecord = False
        #After the recording stops
        now = datetime.now() 
        current_time = now.strftime("%m-%d-%Y_%I:%M:%S")
        while True:
            socket.sleep(0.1) #This is extremely important for some dumb reason
            if currentlyWriting == False: #If it's writing the data while it's being zipped, the file will be empty.
                #Zips the current recording and names it with the current time and date
                os.system("cd qbSat/static/recordings/current-recording && zip -r /home/qbSat/qbSat/static/recordings/downloads/{}.zip ./* && cd -".format(current_time))
                #Deletes the temporary files so they're not in the next recording 
                os.system("sudo rm qbSat/static/recordings/current-recording/CameraA/*.jpg")
                os.system("sudo rm qbSat/static/recordings/current-recording/CameraB/*.jpg")
                os.system("sudo rm qbSat/static/recordings/current-recording/Readings.csv")
                os.system("cd qbSat/static/recordings && ls /home/qbSat/qbSat/static/recordings/downloads > recordingIndex.txt && cd -")
                #This last line makes a text file that lists all of the files in the recordings folder so that the javascript on the downloads page can make a new element for each file.
                socket.emit("recordingIndicatorOff")
                break
    else:
        activeRecord = True
        recordingThread.start() #Runs the recording function in the background so that the other code can run at the same time.
        socket.emit("recordingIndicatorOn")

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=80) #Running on port 80 requires sudo permissions.
