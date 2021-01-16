# /usr/bin/python
import communication as com
from datetime import datetime

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

if __name__ == '__main__':
    now = datetime.now()
    conn = com.Communication(TCP_IP, TCP_PORT)
    ## main loop
    while True:
        ret = conn.get_cmds()
        current_time = now.strftime("%H:%M:%S")
        if ret == None:
            print(current_time)
        else:
            print(current_time + ":{}".format(ret))

    conn.close()