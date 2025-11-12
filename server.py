import socket
import os

def start_server(host='127.0.0.1', port=8080): # 디폴트 호스트와 포트 설정
    # 서버 소켓 생성 socket모듈 안에 있는 socket()클래스 생성 -> (self, family, type, proto, fileno)
    # fimi = 주소체계 (ipv4), type = 소켓 타입 (tcp), 나머지는 기본값 사용
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # def bind(self, address: _Address, /) -> None: ...
    # start_server()함수에서 받은 매개변수로 바인딩
    server_socket.bind((host, port))

    # def listen(self, backlog: int = ...) -> None: ...
    # backlog: int = 5 -> 최대 대기 연결 수 설정 (5초)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}") # 리스닝 정보 출력

    # 무한 루프를 돌며 클라이언트 연결 대기
    while True:
        client_socket, addr = server_socket.accept() # 타임아웃은 sock.setblocking(True)
        print(f"Connection from {addr}") # 클라이언트 연결 정보 출력
        client_socket.sendall(b"Hello, World!") # 클라이언트에 바이트열 전송
        client_socket.close() # 클라이언트 소켓 닫기

        # pid = os.fork()
        # if pid == 0:  # 자식 프로세스 생성 
        #     # 자식 프로세스에서는 서버 소켓 닫기
        #     server_socket.close()  
        #     # 연결 수립 이후 통신 부분 -> 사용자 정의 함수 communicate()
        #     # 여기에 기능 코딩

        
        #     client_socket.close()
        #     os._exit(0)  # 자식 프로세스 종료
        # else:  # 부모 프로세스
        #     client_socket.close()  # 부모 프로세스에서는 클라이언트 소켓 닫기

if __name__ == '__main__':
    start_server()     





# # 디폴트 호스트와 포트 설정 (서버와 같은 이유는 루프백이라서?)
# def client_program(host='127.0.0.1', port=8080): 
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # 서버 연결 함수 def connect(self, address: _Address, /) -> None: ...
#     # address: _Address = (host, port)
#     client_socket.connect((host, port)) # 매개변수로 받은 호스트와 포트로 연결


#     data = client_socket.recv(1024)
#     print(f"Received from server: {data.decode()}")
#     client_socket.close()
