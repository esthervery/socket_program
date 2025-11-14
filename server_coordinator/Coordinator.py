import socket
from Coordinator_utils import print_response
from TempManager import TemperatureManager

import threading

# 전역 TemperatureManager 인스턴스 (모든 스레드가 공유)
tm = TemperatureManager()
 
def handle_client(client_socket, addr):
    """클라이언트 연결을 처리하는 함수"""
    print(f"server log: Client socket Created. Connection {addr}")
    
    # 5분(300초) timeout 설정
    client_socket.settimeout(300)
    
    while True:
        try:
            data = client_socket.recv(1024)
                
            # 클라이언트가 연결을 끊은 경우 (not data)
            if not data:
                print(f"server log: Client disconnected (no data) with {addr}")
                client_socket.close()
                break

            message = data.decode()
            # 온도 갱신
            tm.refresh_temp()
            response = print_response(message, tm)
            
            # 응답 전송
            client_socket.sendall(response.encode())
            
            if response == "Exiting...":
                print(f"server log: Exit command received from {addr}")
                print(f"server log: Client socket closed by client from {addr}")

        except socket.timeout:
            # 5분 동안 메시지가 없으면 연결 종료
            print(f"server log: No message from {addr} for 5 minutes (Timeout)")
            client_socket.sendall(b"Connection timeout. Closing connection...")
            client_socket.close()
            break
                
        except Exception as e:
            print(f"예기치 못한 에러 발생. {addr}: {e}")
            client_socket.close()
            break


def start_server(host='127.0.0.1', port=8080): 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    # accept() 타임아웃 설정 (1초)
    server_socket.settimeout(1)
    print(f"Server listening on {host}:{port}") 

    try: # 강제종료 예외처리 
        while True: # 클라이언트 연결 대기 무한 루프
            try:
                # connection 기다림 (블로킹)
                client_socket, addr = server_socket.accept()

                # connection 수락 후 출력
                print(f"server log: connection(Syn) Accepted, from {addr}")
                
                # 새로운 스레드에서 클라이언트 처리
                client_thread = threading.Thread(
                    target=handle_client, 
                    args=(client_socket, addr),
                    daemon=True
                )
                client_thread.start()
            except socket.timeout:
                # accept() 타임아웃 (계속 루프)
                continue
    
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
    
    finally:
        server_socket.close()
        print("서버 소켓이 닫혔습니다.")

if __name__ == '__main__':  
    start_server()
