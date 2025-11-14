# 일정 주기로 서버에 “POLLING” 메시지를 전송 → 현재 상태가 안전한지 확인
# 서버에서 받은 상태값("safe"/"warning")을 출력

import socket
import time 
def monitor_program(host='127.0.0.2', port=8080, interval=5): 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            client_socket.sendall(b"POLLING") 

            data = client_socket.recv(1024)
            print(f"Status from server: {data.decode()}")

            time.sleep(interval)  
    except KeyboardInterrupt:
        print("Exiting monitor.")
        client_socket.close()
    # finally:
    #     client_socket.close()
        
if __name__ == '__main__':
    monitor_program()