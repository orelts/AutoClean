"""!
@brief communication: client for TCP_IP. will be run on robot, and allow it to send information when ground station requests.
"""
import tcp_ip as com
import time



## public IP of ground station
TCP_IP = '79.176.137.151'
## port that was pre-opened on ground station (via internet router)
TCP_PORT = 5005


if __name__ == '__main__':
    ##
    # @brief try to establish communication with the ground station.
    # once established, wait for word 'info', and upon that send a message.
    # the message will contain readings from the sensors

    while True:
        try:
            conn = com.Communication(TCP_IP, TCP_PORT)
            print("Connection Established")
            while True:
                try:
                    conn.transmit("-") # for server status detection
                    ret = conn.get_cmds() # recieve data from ground station
                    conn.handle_data(ret) # if data contain word 'info' transmit readings from sensors
                except Exception as e:
                    raise e
        except Exception as e:
            print(e)
            print("Trying to reconnect\n")
            time.sleep(1)
            continue

    conn.close()
