import time
from connection import Connection
from configparser import ConfigParser
import base64
import os

def bluetooth_service():
    config = ConfigParser()
    config.read('/home/pi/Documents/project9/src/deployed_config.ini')

    #init the connection
    mac = config.get('Bluetooth','MAC_ADDRESS') 
    channel = config.getint('Bluetooth','CHANNEL')
    lla_file = config.get('Files','LLA')

    if config.get('Encryption','KEY') != None:
        key = config.get('Encryption','KEY')
        key = base64.b64decode(key)
    else:
        print("No Key provided, transmission unencrypted")
        key=None

    conn = Connection(MAC=mac, channel=channel, encryption_key=key)
    while True:
        try:
            #retrieve the LLA and IMU data (as created in project 8)
            with open(lla_file, "r") as lla_src:
                lla = lla_src.readlines()
                lla_src.close()

            lla_file_payload = ""
            for line in lla:
                lla_file_payload += line 

            conn.transmit("*BEGIN*")
            conn.transmit(lla_file_payload)
            conn.transmit("*END*")

        except Exception as e:
            print(f"Unknown exception\n{e}\n\nWaiting...")
            time.sleep(5)

if __name__ == '__main__':
    bluetooth_service() 