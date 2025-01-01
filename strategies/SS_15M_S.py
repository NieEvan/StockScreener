from strategies.MyTT.MyTT import *
from strategies.STRATEGY_BASE import SG_BASE


# 策略名称
class S15(SG_BASE):
    def __init__(self):
        super().__init__("15M", "卖出")

    def on_signal(self, data):
        # K线
        KLINE = data[self.period][:-1]
        OPEN, HIGH, LOW, CLOSE = KLINE['open'], KLINE['high'], KLINE['low'], KLINE['close']

        # 指标
        DIFF = EMA(CLOSE, 12) - EMA(CLOSE, 26)
        DEA = EMA(DIFF, 9)
        MACD = (DIFF - DEA) * 2
        MA20 = MA(CLOSE, 20)

        平台整理 = (REF(HHV(CLOSE, 3), 1) - REF(LLV(OPEN, 3), 1)) / REF(LLV(OPEN, 3), 1) <= (3 / 100)
        AB1 = BARSLAST(REF(CROSS(DEA, DIFF), 1))
        BB1 = (REF(CLOSE, (AB1) + 1) > CLOSE) & (REF(DIFF, (AB1) + 1) > DIFF)
        # AB2=BARSLAST ( REF(CROSS(DEA,DIFF),2))
        # BB2=( REF(CLOSE,(AB2)+1) < REF(CLOSE,AB1+1) ) & ( REF(DIFF,(AB2)+1)>REF(DIFF,(AB1)+1))

        XG = (CROSS(MA20, CLOSE)) & (BB1) & (DEA < 3)
        RETURN = XG
        return RETURN[-1]
