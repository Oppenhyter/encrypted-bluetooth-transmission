import bluetooth
import time
import errno
from encryption import encrypt_data

class Connection:
    '''
    ## Connection
    I made this OO so that the connection would robustly handle itself and wait
    if the host is transmitting or not.
    '''
    
    def __init__(self, MAC, channel, encryption_key=None) -> None:
        self.sock:bluetooth.BluetoothSocket = None
        self.MAC:str = MAC
        self.channel:str = channel
        self.unconnected:bool = True
        self.notified:bool = False
        self.transmitting:bool = False
        self.encrypted:bool = False if encryption_key == None else True
        self.encryption_key = encryption_key
        self.connect() #initiate the connection listener
    
    def connected(self, sock:bluetooth.BluetoothSocket) -> None:
        '''
        ## Connected
        Helper function to reset some variables and display status

        * **sock** [BluetoothSocket] : the socket to keep as the sock
        '''
        self.sock=sock
        self.unconnected=False
        self.notified=False
        print("Connection Secured")

    def connect(self) -> None:
        '''
        ## Connect
        Try for connection, waiting if connection refused 
         (usually because the host isnt running something to listen on the port)
        '''
        self.unconnected=True
        while self.unconnected:
            try:
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((self.MAC, self.channel))
                self.connected(sock)
                
                time.sleep(2)   # somewhere I saw it was a good idea to let it stablize, but I have no problems with it. 
                                # Left here just in case.

            except bluetooth.btcommon.BluetoothError as e:
                self.awaitConnection(e)
                self.notified=True
            except Exception as e:
                print(f"Big problem: {e}")

    def transmit(self, message:str) -> None:
        '''
        ## Transmit
         Encode and send the message over the bluetooth connection.
         Ensures that the connection is handled if something bad happens during
         transmission

        * **message** [str]: the message to send
        '''
        try:
            
            if self.encrypted: 
                cmsg = encrypt_data(message, self.encryption_key)
                self.sock.send(cmsg)
                self.sock.send("\n")
            else:
                message = message.encode('utf-8')
                self.sock.send(message)
            
            time.sleep(0.01)    #for stability

            if not self.transmitting:
                print("Transmitting...") 
                self.transmitting = True
        
        except bluetooth.btcommon.BluetoothError as e:
            print("Transmission Stopped\n")
            self.transmitting = False
            self.awaitConnection(e)
            
        except Exception as e:
            print("Transmission Stopped")
            self.transmitting = False
            print(f"Big problem: {e}")


    def awaitConnection(self, e:Exception | bluetooth.btcommon.BluetoothError):
        '''
        ## Await Connection
        Wait for a transmission if nothing sent, or retry getting connection

        * **e** [Exception | BluetoothError] : the error to diagnose
        '''

        if (e.errno == errno.ECONNREFUSED) | (e.errno == errno.EHOSTDOWN):
                if not self.notified: print(f"Problems connecting to Host: {e}\nWaiting...")
                time.sleep(3)
        elif (e.errno == errno.ENOTCONN) | (e.errno == 104):
            if not self.notified: print(f"Problems with connection: {e}\nReconnecting...")
            self.connect()
        else:
            print(f"Big problem: {e}")

