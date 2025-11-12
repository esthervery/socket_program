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

def start_server(host='127.0.0.1', port=8080): 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}") 

    # 무한 루프를 돌며 클라이언트 연결 대기
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.sendall(b"Hello, World!")
        client_socket.close()

        # 연결이 생성되면 자식 프로세스 생성, 1:1 통신 전환
        # 자식 프로세스 내부에서 수신 메세지에 따른 동작 구형
        # 동작은 utils로 분리하고 호출하는 구조 
    