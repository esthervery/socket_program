import threading
import random

class TemperatureManager:
    def __init__(self):
        self.current_temp = 25
        self.upper_bound = 30
        self.lower_bound = -5
        self.lock = threading.Lock()
    
    def refresh_temp(self):
        """온도 갱신 (스레드 안전)"""
        with self.lock:
            self.current_temp += random.randint(-1, 1)
            return self.current_temp
    
    def get_temp(self):
        """현재 온도 조회"""
        with self.lock:
            return self.current_temp
    
    def set_upper_bound(self, value):
        """상한 설정"""
        with self.lock:
            self.upper_bound = value
    
    def set_lower_bound(self, value):
        """하한 설정"""
        with self.lock:
            self.lower_bound = value
    
    def get_bounds(self):
        """상한, 하한 조회"""
        with self.lock:
            return self.upper_bound, self.lower_bound
    
    def get_all(self):
        """모든 값 조회"""
        with self.lock:
            return self.current_temp, self.upper_bound, self.lower_bound
    
    def set_bounds(self, upper, lower):
        """상한, 하한 설정"""
        with self.lock:
            self.upper_bound = upper
            self.lower_bound = lower
