# 해당 system은 세 가지 entities로 구성되며, 클라이언트 측의 ‘Commander’와 ‘Monitor’, 
# 서버 측의 ‘Coordinator’로 이루어져 있다. 

# 클라이언트 중 하나인 ‘Commander’에서는 서버 측의 ‘Coordinator’에 명령어를 전송
# 하여 현재 설정을 확인(“QUERY”)하거나 새로운 설정(“CONFIGURE)을 적용할 수 있다. 

# 서버 측의 ‘Coordinator’는 ‘Monitor’가 보내온 “POLLING” 메시지를 받고 온도가 변
# 경된다고 가정하여 내부 온도 측정 function을 수행한다. 
# (hint: while 반복문 내에 sleep 함수를 사용하여 반복적으로 send/receive를 수행) 

# 서버 측의 ‘Coordinator’는 ‘Monitor’가 보내온 “POLLING” 메시지를 받고 온도가 변
# 경된다고 가정하여 내부 온도 측정 function을 수행한다. 만약 설정해 놓은 온도의 범
# 위를 벗어나면 ‘Monitor’에 경고 메시지(“warning”)를 전달한다. 그렇지 않다면 “safe” 
# 메시지를 전달한다.

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
    