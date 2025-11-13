
# 클라이언트 중 하나인 ‘Commander’에서는 서버 측의 ‘Coordinator’에 명령어를 전송
# 하여 현재 설정을 확인(“QUERY”)하거나 새로운 설정(“CONFIGURE)을 적용할 수 있다. 

# 서버 측의 ‘Coordinator’는 ‘Monitor’가 보내온 “POLLING” 메시지를 받고 온도가 변
# 경된다고 가정하여 내부 온도 측정 function을 수행한다. 
# (hint: while 반복문 내에 sleep 함수를 사용하여 반복적으로 send/receive를 수행) 

# 만약 설정해 놓은 온도의 범위를 벗어나면 ‘Monitor’에 경고 메시지(“warning”)를 전달한다. 
# 그렇지 않다면 “safe” 메시지를 전달한다.

# 내부 온도 측정 function
def print_response(message: str, current_temp: int, upper_bound: int, lower_bound: int) -> str:
    if message == "QUERY":
        response = f"현재 온도: {current_temp}, 상한: {upper_bound}, 하한: {lower_bound}"
                    
    # Commander가 최대 온도 설정을 30°C로 설정하고자 한다면: CONFIGURE UPPER_BOUND 30
    elif message.startswith("CONFIGURE UPPER_BOUND"):
        _, _, value = message.split()
        upper_bound = int(value)
        response = f"새로운 상한: {upper_bound}"

    elif message.startswith("CONFIGURE LOWER_BOUND"):
        _, _, value = message.split()
        lower_bound = int(value)
        response = f"새로운 하한: {lower_bound}"

    # 지속적으로 들어오는 POLLING 메시지 처리
    elif message == "POLLING":
        if current_temp > upper_bound or current_temp < lower_bound:
            response = "warning"
        else:
            response = "safe"

    elif message == "EXIT":
        response = "Exiting..."
        
    else:
        response = "Unknown command"
    return response

