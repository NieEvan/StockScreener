from strategies.MyTT.MyTT import *
from strategies.STRATEGY_BASE import SG_BASE


# 策略名称
class SSS15(SG_BASE):
    def __init__(self):
        super().__init__("15M", "卖出")

    def on_signal(self, data):
        # K线
        KLINE = data[self.period][:-1]
        OPEN, HIGH, LOW, CLOSE = KLINE['open'], KLINE['high'], KLINE['low'], KLINE['close']

        # 指标
        MA20 = MA(CLOSE, 20)
        MA60 = MA(CLOSE, 60)
        XZ = MIN(MIN(MA(CLOSE, 5), MA(CLOSE, 10)), MA(CLOSE, 20))
        DZ = MAX(MAX(MA(CLOSE, 5), MA(CLOSE, 10)), MA(CLOSE, 20))

        均线角度20 = ATAN(((MA(CLOSE, 20) / REF(MA(CLOSE, 20), 1) - 1) * 100)) * 180 / 3.1416

        Sg = (LOW < XZ) & (HIGH >= DZ) & (CLOSE < OPEN) & (均线角度20 < -0.5) & CROSS(REF(LOW, 1), CLOSE) & (
                    MA20 < MA60)
        RETURN = Sg
        return RETURN[-1]
