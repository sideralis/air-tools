'''
Created on 28 nov. 2018

@author: gautier
'''

#import paho.mqtt.client as mqtt
#import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from time import sleep
import mysql.connector
import json
import password

debug = False

mydb = None
mycursor = None

if debug:
    table_name = ["test"]
else:
    table_name = ["pm25", "pm10"]

# def on_connect(client, userdata, flags, rc):
#     print("Connected", str(rc))
def database():
    global mydb, mycursor
    mydb = mysql.connector.connect(
      host="localhost",
      user="gautier",
      passwd=password.mypassword,       # Just mypassword='___...' in password.py file 
      database="air"
    )
    mycursor = mydb.cursor()   

def on_message_print(client, userdata, message):
    data = json.loads(message.payload)
    
    mac = message.topic[18:30]
    print("== New data received from {}: {} ==".format(mac, message.payload))
    
    # Check if we need to add columns
    sql = "DESC {}".format(table_name[0])
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    res = []
    for e in myresult:
        res.append(e[0])
    if mac not in res:
        for table in table_name:
            sql = "ALTER TABLE {} ADD %s SMALLINT".format(table)
            val = (mac,)
            mycursor.execute(sql)            
        mydb.commit()
        print("ALTER TABLE")
      
    # Check if we need to insert rows
    sql = "SELECT MAX(id) from {}".format(table_name[0])
    mycursor.execute(sql)
    myresult=mycursor.fetchall()
    print("SELECT MAX(id)" , myresult)

    maxid = myresult[0][0]
    
    # Now add rows until we get to id-1
    for i in range(maxid+1, data['id']+1):
        if i == maxid+1:
            print("INSERT INTO", data['id'] - maxid,"row(s)")
 
        for table in table_name:
            sql = "INSERT INTO {} (id) VALUES (%s)".format(table)
            val = (i,)
            mycursor.execute(sql, val)
        mydb.commit()

   
    # Update record
    for table in table_name:
        sql = "UPDATE {} SET {}=%s WHERE id=%s".format(table, mac)
        val = (data[table], data['id'])
        mycursor.execute(sql, val)
        mydb.commit()
        print("UPDATE row", data['id'], "with value", val)
        
        
def main():
    database()
    subscribe.callback(on_message_print, topics='iot-2/type/air/id/+/evt/pm/fmt/json', 
                       hostname='penwv1.messaging.internetofthings.ibmcloud.com', port=8883, 
                       client_id='a:penwv1:sk1g7fg5gp',
                       auth={'username':'a-penwv1-sk1g7fg5gp','password':'2aDAkUw_kW)NI5CUV-'}, 
                       tls={'ca_certs':'orgId.messaging.internetofthings.ibmcloud.com.pem'})
    while(True):
        sleep(1)

if __name__ == '__main__':
    print("mqtt subscribe - version 0.1.0")
    main()

