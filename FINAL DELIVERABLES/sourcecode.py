import time
import sys
import ibmiotf.application
import ibmiotf.device
import random


#Provide your IBM Watson Device Credentials
organization = "7um9ms"
deviceType = "PNTRTEAM454567"
deviceId = "DEVICE454567"
authMethod = "token"
authToken = "2bB!y?GuCED9(8THRD"

# Initialize GPIO


def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    status=cmd.data['command']
    if status=="motoron":
        print ("motor is on")
    else :
        print ("motor is off")
   
    #print(cmd)
    
        


try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #Get Sensor Data from DHT11
        
        soil=random.randint(0,100)
        temp=random.randint(0,100)
        hum=random.randint(0,100)
        
        data = { 'soil moisture': soil, 'temperature':temp, 'humidity':hum}
        #print data
        def myOnPublishCallback():
            print ( "Published Soil Moisture = %s %%" % soil,"Temperature = %s C" % temp, "Humidity = %s %%" % hum, "to IBM Watson")

        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
