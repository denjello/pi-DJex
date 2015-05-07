#!/usr/bin/env python3

'''
To DO
    start pd from this script
    implement relais
    test on/off switch


'''

import os
import subprocess
import socket
import RPi.GPIO as GPIO
import time
from time import sleep
import threading
from runpd import runpd

DJexOnOffPin=   11
RelaisPin=      22
DJexPwmWarnPin= 12

dbThreshold =   80
dbMax       =   100 # we asume PureData will outbut no more then 100 db

RelaisOnTime =  7


def stoppd():
    os.system("sudo pkill pd")

def getLevelsfile ():
    file = open ('/var/www/levels.txt')
    string = file.readline()
    print (string)
    print (type(string))
    string = float(string)
    print (string)
    print (type(string))
    file.close()
    
    return string

def stoppd():
    subprocess.Popen(["sudo", "pkill", "pd"])


def main():


    
    print ("setup GPIO...")
    
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(DJexOnOffPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #enable pull down resistor
    
    GPIO.setup(RelaisPin, GPIO.OUT)
    GPIO.setup(DJexPwmWarnPin, GPIO.OUT)
    
    
    
    pwm = GPIO.PWM(DJexPwmWarnPin, 1000)
    pwm.start (50) # 50 %    

    pwm.ChangeDutyCycle(50)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(50)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(0)    
    time.sleep(0.2)
    pwm.ChangeDutyCycle(50)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(0)    
    
    
    print ("reading levels.txt...")
    dbMax = getLevelsfile()
    dbThreshold = dbMax - 10
    print ("maximum db value: " + str(dbMax))
    print ("dbThreshold for warning: "+ str(dbThreshold))

    
    print ("starting pd Thread")
    pd_thread = threading.Thread(target= subprocess.Popen(["sudo", "pd", "-nogui","-alsa", "-audiodev", "3" , "/home/pi/adcnetsendpatch.pd"]))
    pd_thread.deamon = True
    pd_thread.start()
    print (pd_thread)      
    
   # print ("running pd...")
    
    #runpd()
   
    print ("waiting for connection...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("localhost", 31100)
    s.bind(address)
    s.listen(10)
    print (s)
    conn_sock, client_address = s.accept()
    print ("connected to: \n" + str(client_address) + "\nvia Socket: \n" + str(conn_sock) + "\n") 

    
    while True:
        if GPIO.input(DJexOnOffPin):
            subprocess.Popen(["sudo", "pkill", "pd"])
            while GPIO.input(DJexOnOffPin):    
                print("DJex has been turned inactive")
                time.sleep(5)
            conn_sock.close()
            s.close()            
            stoppd()
            main()
        
        
            
        else:
            try:
                data = conn_sock.recv(32)
                if data:
                    
                    data = data.decode()
                    data = data.replace(";", "")
                    try:
                        data = float(data)
                    except Exception as e:
                        print (e)
                        conn_sock.close()
                        s.close()
                        pwm.stop()
                        GPIO.cleanup()
                        stoppd()           
                        main()
                       
                    print (str(data) + " db " + str(type(data)) )
                      
                    pwmValue = (data/dbMax) *100
                    print ("percent of threshold: " + str(pwmValue) + "%")
                      
                    if data > dbThreshold :
                        pwm.ChangeDutyCycle(data)
                        print ("Warning: Close to db Limit !")  
                            
                        if data >= dbMax:
                            print ("!!! Over Limit !!!")
                                
                            GPIO.output(RelaisPin, GPIO.HIGH)
                              
                            pwm.ChangeDutyCycle(50)
                            time.sleep(0.2)
                            pwm.ChangeDutyCycle(0)
                            time.sleep(0.2)
                            pwm.ChangeDutyCycle(50)
                            time.sleep(0.2)
                            pwm.ChangeDutyCycle(0)    
                            time.sleep(0.2)
                            pwm.ChangeDutyCycle(50)
                            time.sleep(0.2)
                            pwm.ChangeDutyCycle(0)    
                                
                            time.sleep(RelaisOnTime)
                            GPIO.output(RelaisPin, GPIO.LOW)
                            
                        
                            
                    else:
                        pwm.ChangeDutyCycle(0)
                        
                else:
                    print ("no more data")
                    main()
                    
            except Exception as e:
                print (e)
                conn_sock.close()
                s.close()
                stoppd()
                main()
                #pwm.stop()
                #GPIO.cleanup()
        
                

            
if __name__ == "__main__" :
    main()
