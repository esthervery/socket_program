# QUERY: 현재 온도 및 설정된 상한/하한값을 반환, Commander로부터 수신
# 응답 형태: "Current: 25, Upper: 30, Lower: -5"

# CONFIGURE: 새로운 상한/하한값을 설정, Commander로부터 수신
# 응답 형태: "Updated upper bound to 30"

# POLLING: 현재 온도가 안전범위 내인지 검사, Monitor로부터 수신
# 응답 형태: "warning" 또는 "safe"

# 상태 변수 
current_temp = 25
upper_bound = 30
lower_bound = -5


import socket
import os
from Coordinator_utils import print_response

def start_server(host='127.0.0.1', port=8080): 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}") 

    # 무한 루프를 돌며 클라이언트 연결 대기
    while True:
        # server_socket.accept()는 클라이언트 하나와 연결된  새로운 소켓 (client_socket)을 반환
        # 이 client_socket은 해당 클라이언트 전용, 그런데 서버는 한 번에 하나의 클라이언트만 처리
        # 여러 클라이언트가 동시에 접속하려면 자식 프로세스를 만들어서 현재 클라이언트를 처리하고
        # 다시 부모 프로세스가 원래 서버 소켓으로 돌아가 accept() 대기 상태로 있어야 함
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.sendall(b"Hello, World!")
        # client_socket.close()

        # 서버 연결이 생성되면 자식 프로세스 생성, 1:1 통신 전환
        pid = os.fork()
        if pid == 0:  # 자식 프로세스 생성
            # 자식 프로세스에서는 서버 소켓 닫기
            # 자식 프로세스에서 server_socket.close()를 해도, 부모 프로세스가 여전히 그 소켓을 열고 있다면 서버는 계속 listen 상태를 유지
            server_socket.close() 
            
            # 클라이언트측 데이터 확인
            data = client_socket.recv(1024)
            if not data:
                client_socket.close()
                os._exit(0) # 데이터 없으면 소켓 닫고 자식 프로세스 종료
            else:
                try: # try-except문으로 예외처리
                    message = data.decode()

                    # 함수 안에서 전역 변수(global variable)를 수정할 때 사용
                    global current_temp, upper_bound, lower_bound

                    # 자식 프로세스 내부에서 수신 메세지에 따른 동작 구현 -> utils 모듈 형태
                    response = print_response(message, current_temp, upper_bound, lower_bound)
                    client_socket.sendall(response.encode())

                except Exception as e:
                    client_socket.sendall(f"Error: {str(e)}".encode())
            
            client_socket.close()
            os._exit(0)  # 응답 메세지 전송 후 자식 프로세스 종료

 
    