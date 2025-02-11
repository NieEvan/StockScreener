import importlib
import sys
import time
import traceback
from datetime import datetime
from glob import glob
from pathlib import Path
from types import ModuleType
from typing import Dict, Any
import pymongo
from pymongo import MongoClient

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import (
    MONGO_USER, 
    MONGO_PASSWORD, 
    MONGO_DATABASE, 
    MONGO_HOST, 
    MONGO_PORT
)
from datetime import datetime
from loguru import logger
import MetaTrader5

from modules.FdtWarningApp import FdtWarningApp, to_email


class BaseApp:
    def __init__(
            self, market: str, symbols: list = None, symbol_sep: str = None, mt5_path: str = None,
            warn_user: str = None, email_user: str = None, email_pwd: str = None, email_reception: list = None,
            symbols_dict: dict = None
    ):
        print("BaseApp instance created")
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
        
        # Connect to MongoDB
        self.db, self.error = self.connect_to_mongodb()
        if self.error:
            print(f"Connection failed: {self.error}")
            quit()
        self.collection = self.db["BarData"]

    def connect_to_mongodb(self):
        try:
            uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}?authSource={MONGO_DATABASE}"
            client = MongoClient(uri)

            client.admin.command('ping')
            print("Successfully connected to MongoDB!")

            db = client[MONGO_DATABASE]
            return db, None

        except pymongo.errors.ConnectionFailure as e:
            error_message = f"Could not connect to MongoDB: {e}"
            print(error_message)
            return None, error_message
        except Exception as e:
            error_message = f"An error occurred: {e}"
            print(error_message)
            return None, error_message


    def load_strategy_class(self) -> None:
        path = Path.cwd().joinpath("./strategies")
        module_name = "strategies"
        for suffix in ["py", "pyd", "so"]:
            pathname = str(path.joinpath(f"*.{suffix}"))
            print(f"GLOB for '.{suffix}': ", glob(pathname))
            for filepath in glob(pathname):
                if filepath != 'F:\\StockScreener-main\\strategies\\STRATEGY_BASE.py':
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
    def get_mt5_data(symbol: str, count: int = 1) -> Dict[str, Any]:
        data_map = {
            "1M": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_M1, 0, count),
            "5M": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_M5, 0, count),
            "1H": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_H1, 0, count),
            "4H": MetaTrader5.copy_rates_from_pos(symbol, MetaTrader5.TIMEFRAME_H4, 0, count),
        }
        return data_map

    def start(self) -> None:
        """开始检测"""
        self.symbol_time = {}
        if self.symbols is None:
            self.all_symbols = [["买入", self.buy_symbols], ["卖出", self.sell_symbols]]
        else:
            self.all_symbols = [["买卖", self.symbols]]
        while True:
            init_time = time.time()
            self._process_all_symbols()
            self._handle_logging_and_sleep(init_time)
    
    def _store_data(self, symbol, period, data):
        document = {
            "symbol": symbol,
            "timeframe": period,
            "timestamp": int(data[period][-1][0]),
            "open": float(data[period][-1][1]),
            "high": float(data[period][-1][2]),
            "low": float(data[period][-1][3]),
            "close": float(data[period][-1][4]),
            "tick_volume": int(data[period][-1][5]),
            "spread": int(data[period][-1][6]),
            "real_volume": int(data[period][-1][7]),
        }
        print("document", document)
        try:
            self.collection.insert_one(document)
        except pymongo.errors.DuplicateKeyError:
            pass

    def _process_all_symbols(self) -> None:
        """处理所有交易对"""
        for direction, symbols in self.all_symbols:
            for symbol in symbols:
                self._process_single_symbol(symbol, direction)

    def _process_single_symbol(self, symbol: str, direction: str) -> None:
        """处理单个交易对"""
        new_data = self.get_mt5_data(symbol)  # 取数据
        # 如果是新symbol
        if symbol not in self.symbol_time.keys():
            self.symbol_time[symbol] = {}
    
        
        self._process_symbol_periods(symbol, direction, new_data)

    def _process_symbol_periods(self, symbol: str, direction: str, new_data: dict) -> None:
        """处理交易对的所有周期 """
        for period in ["1M", "5M", "1H", "4H"]:
            if self._is_new_data(symbol, period, new_data):
                print('yes')
                self._store_data(symbol, period, new_data) # store the latest data
                # Process the retrieved data
                retrieved_data = {}
                cursor = self.collection.find(
                    {"symbol": symbol, "timeframe": period},
                    {"_id": 0}
                ).sort("timestamp", -1).limit(200)
                retrieved_data = list(cursor)

                self._handle_period_data(symbol, period, direction, retrieved_data)

    def _is_new_data(self, symbol: str, period: str, data: dict) -> bool:
        """检查是否有新数据"""
        # 如果symbol_time里还没有某个period的数据（第一次）
        if not self.symbol_time[symbol].get(period):
            if data[period] is None:
                return False
            self.symbol_time[symbol][period] = data[period][-1][0]
            if self.first_run:
                self.symbol_time[symbol][period] = 0
            return False
        
        # 有新的数据（不是第一次
        return data[period][-1][0] != self.symbol_time[symbol][period]

    def _handle_period_data(self, symbol: str, period: str, direction: str, data: list) -> None:
        """处理周期数据并发送信号"""
        for name, cls in self.classes.items():
            print("Check for:", name)
            signal_info = self._check_strategy_signal(symbol, name, cls, period, direction, data)
            if signal_info:
                print("Signal generated")
                # self._send_signal_notifications(signal_info)
                
        # 更新数据
        if data:
            self.symbol_time[symbol][period] = data[0]['timestamp']

    def _check_strategy_signal(self, symbol, name: str, cls, period: str, direction: str, data: dict) -> dict:
        """检查策略信号"""
        signal_info = {}
        try:
            if period == cls.period and (cls.direction == direction or direction == "买卖"):
                print("checking for signal")
                # 如果是复合的策略
                signal = cls.on_signal(data)
                if signal:
                    signal_info = {
                        "market": self.market + period + ('B' if cls.direction == '买入' else 'S'),
                        "symbol": symbol.split(self.symbol_sep)[0],
                        "direction": cls.direction,
                        "conditions": cls.conditions,
                    }
        except Exception as e:
            logger.info(f"{name}({e}):\n{traceback.format_exc()}")
        
        return signal_info

    def _send_signal_notifications(self, signal_info: dict) -> None:
        """发送信号通知"""
        # 发送WebSocket警告
        self.ws.send_warning(**signal_info)
        
        # 发送邮件通知
        email_txt = [
            datetime.now().strftime('%m-%d %H:%M'),
            signal_info['symbol'],
            signal_info['direction'][0],
            signal_info['conditions'],
        ]
        email_txt = " ".join(email_txt)
        to_email(self.email_reception, email_txt, self.email_pwd, self.email_user)
        logger.info(signal_info)

    def _handle_logging_and_sleep(self, init_time: float) -> None:
        """处理日志和休眠"""
        if self.log_run:
            logger.info(f"运行(s)：{time.time() - init_time}")
        
        # 计算到下一个5分钟的休眠时间
        sleep_s = (time.time() // (60 * 1) + 1) * (60 * 1) - time.time() + 1
        time.sleep(sleep_s)
