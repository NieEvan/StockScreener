import os.path

import pandas as pd
from loguru import logger
import MetaTrader5

from base import Base
from config import STKConfig


class StrategyManager(Base):
    def __init__(self) -> None:
        # logger.add('logs\\stk.log')
        STKConfig.pop("extra")
        super().__init__("STK", None, ".", **STKConfig)
        self.get_symbols()

        self.first_run = False
        self.log_run = True

    def get_symbols(self) -> None:
        # 通达信目录
        tdx_path = r"C:\TDX"

        mt5_symbols = {
            symbol.name.replace('.NAS', ""): symbol.name for symbol in MetaTrader5.symbols_get(f"*.NAS")
        }
        mt5_symbols2 = {
            symbol.name.replace('.NYSE', ""): symbol.name for symbol in MetaTrader5.symbols_get(f"*.NYSE")
        }
        mt5_symbols.update(mt5_symbols2)

        # 筛选
        # df = pd.read_csv("resource/us_stocks.csv")
        # df = df[df["总金额"] >= 5000]
        # df.sort_values("活跃度", ascending=False, inplace=True) 
        # tdx_symbols = df["代码"].tolist()[:1000]TDX

        # 读取通达信 USB USS
        buy_path = os.path.join(tdx_path, r"T0002\blocknew\US3B.blk")
        with open(buy_path, 'r') as f:
            buy_blk = f.read()
        sell_path = os.path.join(tdx_path, r"T0002\blocknew\US3S.blk")
        with open(sell_path, 'r') as f:
            sell_blk = f.read()
        tdx_buy_symbols = [each.split("#")[-1] for each in buy_blk.split("\n") if each]
        tdx_sell_symbols = [each.split("#")[-1] for each in sell_blk.split("\n") if each]

        buy_symbols = []
        for symbol in tdx_buy_symbols:
            if symbol in mt5_symbols.keys():
                buy_symbols.append(mt5_symbols[symbol])

        sell_symbols = []
        for symbol in tdx_sell_symbols:
            if symbol in mt5_symbols.keys():
                sell_symbols.append(mt5_symbols[symbol])

        self.buy_symbols = buy_symbols
        self.sell_symbols = sell_symbols
        logger.info(f"len(self.buy_symbols): {len(self.buy_symbols)}")
        logger.info(f"len(self.sell_symbols): {len(self.sell_symbols)}")


def main() -> None:
    sm = StrategyManager()
    sm.start()


if __name__ == '__main__':
    main()
