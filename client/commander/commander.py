# 사용자가 직접 입력한 명령을 서버(Coordinator)에 전달
# QUERY
# CONFIGURE UPPER_BOUND <숫자>
# CONFIGURE LOWER_BOUND <숫자>
# exit  ← (프로그램 종료용)

import socket

def is_valid_command(command: str) -> bool:
    """명령어 검증"""
    if command == "QUERY" or command == "EXIT":
        return True
    
    if command.startswith("CONFIGURE UPPER_BOUND"):
        parts = command.split()
        if len(parts) == 3:
            try:
                int(parts[2])
                return True
            except ValueError:
                return False
    
    if command.startswith("CONFIGURE LOWER_BOUND"):
        parts = command.split()
        if len(parts) == 3:
            try:
                int(parts[2])
                return True
            except ValueError:
                return False
    
    return False

def commander_program(host='127.0.0.1', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # 서버로부터 초기 메시지 수신
    initial_data = client_socket.recv(1024)
    print(initial_data.decode())

    while True:
        command = input("Enter command (QUERY, CONFIGURE UPPER_BOUND <num>, CONFIGURE LOWER_BOUND <num>, EXIT): ")
        
        if not command.strip(): # 빈 명령어 처리 (Enter만 눌렀을 때)
            print("Error: 명령어를 입력하지 않았습니다. 다시 시도하세요.")
            continue
        
        if not is_valid_command(command):
            print("Error: 잘못된 명령어 형식입니다. 다시 시도하세요.")
            continue
            
        # 잘못된 명령어가 아닌 경우 전송 (EXIT 포함)
        client_socket.sendall(command.encode())

        # EXIT 명령의 경우 짧은 타임아웃 설정
        if command == "EXIT":
            client_socket.settimeout(1)  # 1초 타임아웃
        else:
            client_socket.settimeout(None)  # 무제한 대기

        # 서버로부터 응답 대기 (try로 예외처리)
        try: 
            data = client_socket.recv(1024)
            
            if not data:  # 서버가 연결을 끊은 경우
                print("서버에서 연결이 종료되었습니다.")
                client_socket.close()
                break
            
            response_msg = data.decode()
            print(f"Response from server: {response_msg}")
            
            # EXIT 응답을 받으면 종료
            if command == "EXIT":
                print("프로그램을 종료합니다.")
                client_socket.close()
                break
            
        except socket.timeout:
            # EXIT 명령 시 타임아웃 발생 (서버가 응답하지 않음)
            if command == "EXIT":
                print("프로그램을 종료합니다.")
                client_socket.close()
                break
            else:
                print("서버 응답 타임아웃")
                client_socket.close()
                break
                
        except Exception as e:
            print(f"예기치 못한 에러 발생: {e}")
            client_socket.close()
            break
        # finally:
        #     client_socket.close()
    
if __name__ == '__main__':
    commander_program()