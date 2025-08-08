from strategies.MyTT.MyTT import *


# 策略名称
class test:
    def __init__(self):
        # 策略周期
        self.period = "1M"
        # 策略方向
        self.direction = "买入"
        self.conditions = f"{self.__class__.__name__}_{self.period}"

    def on_signal(self, data):
        return True
