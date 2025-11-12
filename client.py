import socket

def client_program(host='127.0.0.1', port=8080): 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 서버 연결 함수 def connect(self, address: _Address, /) -> None: ...
    # address: _Address = (host, port) -> 여기로 연결 요청
    client_socket.connect((host, port)) # 매개변수로 받은 호스트와 포트로 연결

    data = client_socket.recv(1024) # 버퍼 크기 1024바이트
    print(f"Received from server: {data.decode()}")
    client_socket.close()

if __name__ == '__main__':
    client_program()