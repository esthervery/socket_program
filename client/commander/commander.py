# 사용자가 직접 입력한 명령을 서버(Coordinator)에 전달
# QUERY
# CONFIGURE UPPER_BOUND <숫자>
# CONFIGURE LOWER_BOUND <숫자>
# exit  ← (프로그램 종료용)
import socket
def commander_program(host='127.0.0.1, port=8080'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        command = input("Enter command (QUERY, CONFIGURE UPPER_BOUND <num>, CONFIGURE LOWER_BOUND <num>, EXIT): ")
        client_socket.sendall(command.encode())

        if command == "EXIT":
            print("Exiting commander.")
            break

        data = client_socket.recv(1024)
        print(f"Response from server: {data.decode()}")

    client_socket.close()
    
if __name__ == '__main__':
    commander_program()