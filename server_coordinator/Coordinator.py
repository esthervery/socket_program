import socket
import os
from Coordinator_utils import print_response

current_temp = 25
upper_bound = 30
lower_bound = -5

def start_server(host='127.0.0.1', port=8080): 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}") 

    # 클라이언트 연결 대기 무한 루프
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.sendall(b"Hello, World!")

        # 서버 연결이 생성되면 자식 프로세스 생성, 1:1 통신 전환
        pid = os.fork()
        if pid == 0: 
            # 자식 프로세스에서는 서버 소켓 닫기
            server_socket.close() 
            
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break  # 연결 종료

                    message = data.decode()

                    global current_temp, upper_bound, lower_bound

                    response = print_response(message, current_temp, upper_bound, lower_bound)
                    if response == "Exiting":
                        break
                    client_socket.sendall(response.encode())

                except Exception as e:
                    client_socket.close()
                    os._exit(0) 
        else:  
            client_socket.close()  # 부모 프로세스에서는 클라이언트 소켓 닫고 서버 소켓으로 돌아감


if __name__ == '__main__':  
    start_server()

 
    