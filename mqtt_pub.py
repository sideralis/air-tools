'''
Created on 28 nov. 2018

@author: gautier
'''

import paho.mqtt.publish as publish
from time import sleep
import random
import time

debug = True

if debug:
    field = "test"
else:
    field = "pm25"
    
def main():
    pm25_center = 5
    pm10_center = 20
    range25 = 3
    range10 = 5
    
    pm25 = pm25_center
    pm10 = pm10_center
    while(True):
        r25 = random.random()*range25-range25/2
        r10 = random.random()*range10-range10/2
        m25 = (3*pm25+pm25_center)/4
        m10 = (3*pm10+pm10_center)/4
        
        pm25 = m25+r25
        pm10 = m10+r10
        
        #print (r25, m25, pm25)
        #print (r10, m10, pm10)
        id = int(time.time()/60-25726416)            # Start date was on 30 nov 2018 14:36
        myPayload = '{{"id":{},"{}":{},"pm10":{}}}'.format(id, field, round(pm25), round(pm10))
 
        print(myPayload)
        publish.single(topic='iot-2/evt/pm/fmt/json', payload=myPayload, hostname='penwv1.messaging.internetofthings.ibmcloud.com', port=8883, client_id='d:penwv1:air:382b7803d71d',auth={'username':'use-token-auth','password':'2nUIQ2o*F&*9YRYZoa'}, tls={'ca_certs':'/home/gautier/snap/mosquitto/common/orgId.messaging.internetofthings.ibmcloud.com.pem'})    
        sleep(60)

if __name__ == '__main__':
    main()
        