# /usr/bin/python
import tcp_ip as com
from datetime import datetime

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

if __name__ == '__main__':
    conn = com.Communication(TCP_IP, TCP_PORT)
    ## main loop
    while True:
        ret = conn.get_cmds()
        if ret == None:
            continue
        else:
            print("{}".format(ret))

    conn.close()