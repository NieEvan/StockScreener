from strategies.MyTT.MyTT import *


class SG_BASE:
    # 策略名称
    def __init__(self, period, direction):
        # 策略周期
        self.period = period
        # 策略方向
        self.direction = direction
        self.conditions = f"{self.__class__.__name__}_{self.period}"

    def on_signal(self, data) -> bool:
        return False
