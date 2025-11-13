import socket
# import os
from Coordinator_utils import print_response

current_temp = 25
upper_bound = 30
lower_bound = -5

import threading

def handle_client(client_socket, addr):
    """클라이언트 연결을 처리하는 함수"""
    print(f"Connection from {addr}")
    
    # 5분(300초) timeout 설정
    client_socket.settimeout(300)
    
    try:
        client_socket.sendall(b"Hello, World!")
        
        while True:
            try:
                data = client_socket.recv(1024)
                # data = client_socket.recv(1024)
                # 여기서 멈춰있음 (블로킹)
                # 데이터가 올 때까지 대기... -> None을 반환하지 않음
                
                # 클라이언트가 연결을 끊은 경우 (not data)
                if not data:
                    print(f"Client {addr} disconnected")
                    break

                message = data.decode()

                global current_temp, upper_bound, lower_bound

                response = print_response(message, current_temp, upper_bound, lower_bound)
                
                # 응답을 먼저 전송
                client_socket.sendall(response.encode())
                
                # Exiting 메시지를 받으면 연결 종료
                if response == "Exiting":
                    print(f"Exit command received from {addr}")
                    break

            except socket.timeout:
                # 5분 동안 메시지가 없으면 연결 종료
                print(f"Timeout: No message from {addr} for 5 minutes")
                client_socket.sendall(b"Connection timeout. Closing connection.")
                break
                
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                break
            
    # 무슨 일이 있어도 항상 실행되는 코드 블록
    finally:
        client_socket.close()
        print(f"Connection closed from {addr}")


def start_server(host='127.0.0.1', port=8080): 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}") 

    try: # 강제종료 예외처리 
        while True: # 클라이언트 연결 대기 무한 루프 (server_socket) 활용
            client_socket, addr = server_socket.accept()
            
            # 새로운 스레드에서 클라이언트 처리
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, addr),
                daemon=True # 메인 프로그램 종료시 스레드도 종료
            )
            client_thread.start()
    
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
    
    finally:
        server_socket.close()
        print("서버 소켓이 닫혔습니다.")

if __name__ == '__main__':  
    start_server()
 

#   class Thread(
#     group: None = None,              # group 파라미터, 타입은 None, 기본값 None
#     target: ((...) -> object) | None = None,  # target 파라미터, 함수 또는 None
#     name: str | None = None,         # name 파라미터, 문자열 또는 None
#     args: Iterable[Any] = (),        # args 파라미터, 반복가능한 객체, 기본값 빈 튜플
#     kwargs: Mapping[str, Any] | None = None,  # kwargs 파라미터, 딕셔너리 또는 None
#     *,                                # 이후 파라미터는 반드시 키워드로 지정
#     daemon: bool | None = None        # daemon 파라미터, bool 또는 None
# )  