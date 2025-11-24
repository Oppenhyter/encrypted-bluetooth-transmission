# Encrypted-Bluetooth-Transmission
![raspberrypi](https://img.shields.io/badge/RaspberryPi-4B-maroon?logo=raspberrypi)
![python](https://img.shields.io/badge/Python-v3.12.3-blue?logo=python)

Takes in data, ecrypts and sends to another device to decrypt. 
This was initially created to run on a Windows 11 host, recieving data from the Raspberry Pi's built-in bluetooth module. 

### Host Setup
- Modify the `host/host_config.ini` file to have the correct items (there should be no quotation marks around any items).

### Raspberry Pi Setup
- Modify the `deploy_config.ini` file to have the correct items (there should be no quotation marks around any items).

- To push the code to the RPi use: \
`scp ./src/ [USER]@[IP ADDRESS] ~/Documents/ecryptedBT/` \
Replacing your username, IP address and file location as necessary

- Log onto your Raspberry Pi (directly or through SSH)
  Verify that the files have been transferred to `~/Documents/encryptedBT/src/`
  run the following installs: \
  `sudo apt install update && sudo apt install upgrade` \
  `sudo apt install bluez`
