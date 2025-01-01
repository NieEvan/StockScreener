from strategies.MyTT.MyTT import *
from strategies.STRATEGY_BASE import SG_BASE


# 策略名称
class B15(SG_BASE):
    def __init__(self):
        super().__init__("15M", "买入")

    def on_signal(self, data):
        # K线
        KLINE = data[self.period][:-1]
        OPEN, HIGH, LOW, CLOSE = KLINE['open'], KLINE['high'], KLINE['low'], KLINE['close']

        # 指标
        DIFF = EMA(CLOSE, 12) - EMA(CLOSE, 26)
        DEA = EMA(DIFF, 9)
        MACD = (DIFF - DEA) * 2
        MA20 = MA(CLOSE, 20)

        # CCB1 == REF(MACD,2)<REF(MACD,1) & REF(MACD,3)>==REF(MACD,2) & REF(MACD,4)>REF(MACD,3)
        # CCB2 == REF(MACD,2)<REF(MACD,1) & REF(MACD,3)<REF(MACD,2) & REF(MACD,4)>==REF(MACD,3)
        # CCB == CCB1 | CCB2
        ptzl = (REF(HHV(CLOSE, 3), 1) - REF(LLV(OPEN, 3), 1)) / REF(LLV(OPEN, 3), 1) <= (3 / 100)
        AB1 = BARSLAST(REF(CROSS(DIFF, DEA), 1))
        B1 = (REF(CLOSE, (AB1) + 1) < CLOSE) & (REF(DIFF, (AB1) + 1) < DIFF)
        # AB2 == BARSLAST(REF(CROSS(DEA,DIFF),2))
        # B2 == REF(CLOSE,AB2+1)>REF(CLOSE,AB1+1) & REF(DIFF,AB2+1)<REF(DIFF,AB1+1)
        BBB = (CROSS(CLOSE, MA20)) & (B1) & (DEA > -0.5)

        RETURN = BBB
        return RETURN[-1]
