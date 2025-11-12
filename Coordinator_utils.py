
# 클라이언트 중 하나인 ‘Commander’에서는 서버 측의 ‘Coordinator’에 명령어를 전송
# 하여 현재 설정을 확인(“QUERY”)하거나 새로운 설정(“CONFIGURE)을 적용할 수 있다. 

# 서버 측의 ‘Coordinator’는 ‘Monitor’가 보내온 “POLLING” 메시지를 받고 온도가 변
# 경된다고 가정하여 내부 온도 측정 function을 수행한다. 
# (hint: while 반복문 내에 sleep 함수를 사용하여 반복적으로 send/receive를 수행) 

# 만약 설정해 놓은 온도의 범위를 벗어나면 ‘Monitor’에 경고 메시지(“warning”)를 전달한다. 
# 그렇지 않다면 “safe” 메시지를 전달한다.

# 내부 온도 측정 function
def measure_temperature():
    return 0


 # 연결 수립 이후 통신 부분
def communicate(client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received from client: {data.decode()}")
            client_socket.sendall(b"ACK")