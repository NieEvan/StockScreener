import importlib
import sys
import time
import traceback
from datetime import datetime
from glob import glob
from pathlib import Path
from types import ModuleType
from typing import Dict, Any

from loguru import logger
import MetaTrader5

from connect import FdtWarningApp, to_email

sys.path.append("strategies")


class Base:
    def __init__(
            self, market: str, symbols: list = None, symbol_sep: str = None, mt5_path: str = None,
            warn_user: str = None, email_user: str = None, email_pwd: str = None, email_reception: list = None,
            symbols_dict: dict = None
    ):
        self.market = market
        self.mt5_path = mt5_path
        self.warn_user = warn_user
        self.email_user = email_user
        self.email_pwd = email_pwd
        self.email_reception = email_reception if email_reception else []
        self.symbols = symbols
        if (self.symbols is None) and symbols_dict:
            self.buy_symbols = symbols_dict['buy_symbols']
            self.sell_symbols = symbols_dict['sell_symbols']
        else:
            self.buy_symbols = self.symbols
            self.sell_symbols = self.symbols
        self.symbol_sep = symbol_sep

        self.first_run = False
        self.log_run = False
        self.classes = {}
        self.load_strategy_class()
        self.ws = FdtWarningApp(bool(self.warn_user))
        if self.mt5_path:
            MetaTrader5.initialize(self.mt5_path)
        logger.info(f"初始化（{len(self.symbols) if self.symbols else 0}）：{self.classes.keys()}")

    def load_strategy_class(self) -> None:
        path = Path.cwd().joinpath("./strategies")
        module_name = "strategies"
        for suffix in ["py", "pyd", "so"]:
            pathname = str(path.joinpath(f"*.{suffix}"))
            print("GLOB: ", glob(pathname))
            for filepath in glob(pathname):
                # print(filepath)
                filename = Path(filepath).stem
                name = f"{module_name}.{filename}"
                self.load_strategy_class_from_module(name)
    def load_strategy_class_from_module(self, module_name: str) -> None:
        try:
            module: ModuleType = importlib.import_module(module_name)
            importlib.reload(module)
            for name in dir(module):
                value = getattr(module, name)
                if isinstance(value, type):
                    self.classes[value.__name__] = value()
        except Exception as e:
            print(f"策略文件{module_name}加载失败，触发异常({e})：\n{traceback.format_exc()}")

    @staticmethod
    def get_mt5_data(symbol: str, count: int = 2000) -> Dict[str, Any]:
        data_map = {
            "5M": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_M5, 0, count),
            "15M": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_M15, 0, count),
            "1H": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_H1, 0, count),
            "4H": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_H4, 0, count),
        }
        return data_map

    def start(self) -> None:
        symbol_time = {}
        if self.symbols is None:
            all_symbols = [["买入", self.buy_symbols], ["卖出", self.sell_symbols]]
        else:
            all_symbols = [["买卖", self.symbols]]
        
        """开始检测"""
        while True:
            init_time = time.time()
            # 循环买卖symbols
            for direction, symbols in all_symbols:
                # 循环symbol
                for symbol in symbols:
                    data = self.get_mt5_data(symbol) # 去数据
                    if symbol not in symbol_time.keys(): # 如果是新symbol
                        symbol_time[symbol] = {}
                    
                    # 循环周期变更
                    for period in data.keys():
                        print(data[period][-1])
                        if not symbol_time[symbol].get(period): # 如果symbol_time里还没有某个period的数据（第一次）
                            if data[period] is None:
                                print("no data")
                                continue
                            symbol_time[symbol][period] = data[period][-1][0]
                            if self.first_run:
                                symbol_time[symbol][period] = 0
                        if data[period][-1][0] != symbol_time[symbol][period]: # 有新的数据（不是第一次）
                            # 循环策略
                            for name, cls in self.classes.items():
                                signal_info = {}
                                try:
                                    if period == cls.period and (cls.direction == direction or direction == "买卖"): #
                                        # 如果是复合的策略
                                        signal = cls.on_signal(data)
                                        # print(f"on_signal({cls.__class__.__name__}): {signal}")
                                        if signal:
                                            signal_info = {
                                                "market": self.market + period + (
                                                    'B' if cls.direction == '买入' else 'S'),
                                                "symbol": symbol.split(self.symbol_sep)[0],
                                                "direction": cls.direction,
                                                "conditions": cls.conditions,
                                            }
                                except Exception as e:
                                    logger.info(f"{name}({e}):\n{traceback.format_exc()}")

                                # 信号
                                if signal_info:
                                    self.ws.send_warning(**signal_info)
                                    email_txt = [
                                        datetime.now().strftime('%m-%d %H:%M'),
                                        signal_info['symbol'],
                                        signal_info['direction'][0],
                                        signal_info['conditions'],
                                    ]
                                    email_txt = " ".join(email_txt)
                                    to_email(self.email_reception, email_txt, self.email_pwd, self.email_user)
                                    logger.info(signal_info)
                            symbol_time[symbol][period] = data[period][-1][0] # 跟新数据


            if self.log_run:
                logger.info(f"运行(s)：{time.time() - init_time}")
            sleep_s = (time.time() // (60 * 5) + 1) * (60 * 5) - time.time() + 1
            time.sleep(sleep_s)
