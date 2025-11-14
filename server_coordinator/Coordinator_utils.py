def print_response(message: str, tm) -> str:
    """
    TempManager 객체를 받아서 메시지 처리
    """
    if message == "QUERY":
        current_temp, upper_bound, lower_bound = tm.get_all()
        response = f"현재 온도: {current_temp}, 상한: {upper_bound}, 하한: {lower_bound}"
                    
    elif message.startswith("CONFIGURE UPPER_BOUND"):
        _, _, value = message.split()
        upper_bound = int(value)
        tm.set_upper_bound(upper_bound)
        response = f"새로운 상한: {upper_bound}"

    elif message.startswith("CONFIGURE LOWER_BOUND"):
        _, _, value = message.split()
        lower_bound = int(value)
        tm.set_lower_bound(lower_bound)
        response = f"새로운 하한: {lower_bound}"

    elif message == "POLLING":
        current_temp, upper_bound, lower_bound = tm.get_all()
        if current_temp > upper_bound or current_temp < lower_bound:
            response = "warning"
        else:
            response = "safe"

    elif message == "EXIT":
        response = "Exiting..."
    
    else:
        response = "Unknown command"
        
    return response
