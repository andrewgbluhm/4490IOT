#imports
import RPi.GPIO as GPIO #GPIO library/package
import time #enables time.sleep funtion to let us run this every 1 second
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #required package to connect to AWS IoT
from random import randrange#package for picking a random number

#Connection to the AWS IoT Core with Root CA certificate and unique device credentials (keys and certificate) previously retrieved

#For certificate based connection
myMQTTClient = AWSIoTMQTTClient("Kwameclientid")
#For TLS mutual authentication
myMQTTClient.configureEndpoint("a39nu1xs62gahx-ats.iot.us-east-1.amazonaws.com", 8883)
#Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("/home/pi/awsiot/AmazonRootCA1.pem.txt", "/home/pi/awsiot/92e8ceef8e-private.pem.key", "/home/pi/awsiot/92e8ceef8e-certificate.pem.crt") #Set path for Root CA and unique device credentials (use the private key and certificate retrieved from the logs in Step 1)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
 
print('Initiating IoT Core Topic ...')#print to terminal to make show user that board is reaching out for a connection
myMQTTClient.connect()#connect to aws iot


#GPIO INPUTS -- in order presented
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)#photoresistor number 1 (input mode)
GPIO.setup(17,GPIO.IN)#photoresistor number 2 (input mode)
GPIO.setup(5,GPIO.IN)#photoresistor number 3 (input mode)
GPIO.setup(6,GPIO.IN)#photoresistor number 4 (input mode)
GPIO.setup(26,GPIO.IN)#photoresistor number 5 (input mode)


#array of thirty passwords
passwords = ['11111','11001','11010','01101','00001','01100','10001','10011','10010','10110','01100','00110','00010',
             '10010','11100','10010','00101','00101','01000','00100','01110','10010','00001','00110','10111','10001',
             '00110','01111','10111','10011','01001']

#i variable to pick an array value
i=0

while True:
	photo1 = str(GPIO.input(5))#determine value of photoresistor 1 and set it as a string
	photo2 = str(GPIO.input(6))#determine value of photoresistor 2 and set it as a string
	photo3 = str(GPIO.input(16))#determine value of photoresistor 3 and set it as a string
	photo4 = str(GPIO.input(17))#determine value of photoresistor 4 and set it as a string
	photo5 = str(GPIO.input(26))#determine value of photoresistor 5 and set it as a string

        #if statement to determine if correct pattern is being entered
        if (photo1+photo2+photo3+photo4+photo5) == passwords[i] :
            randomVariable = randrange(30)#chooses a random number between 0 and 30
            i=randomVariable#assigns random number to variable i
            payload = "Access Enabled: Your new password is " + passwords[i]+"."#states what the new password is
            myMQTTClient.publish("home/helloworld",payload,0)#publishes to aws iot core topic
        else:#if input is not correct, do not allow access
            payload = "Access Denied"
        print(payload)#prints to terminal if access is granted or not
        time.sleep(1)#run this every one second


