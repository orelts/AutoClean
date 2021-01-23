# /usr/bin/python
import tcp_ip as com
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005


if __name__ == '__main__':
    while True:
        try:
            conn = com.Communication(TCP_IP, TCP_PORT)
            print("Connection Established")
            while True:
                try:
                    conn.transmit("-") # for server status detection
                    ret = conn.get_cmds()
                    conn.handle_data(ret)
                except Exception as e:
                    raise e
        except Exception as e:
            print(e)
            print("Trying to reconnect\n")
            time.sleep(1)
            continue

    conn.close()
