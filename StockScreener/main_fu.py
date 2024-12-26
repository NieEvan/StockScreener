import time
import traceback
from datetime import datetime, time as dtime

from loguru import logger
from tqsdk import TqApi, TqAuth

from connect import to_email
from base import Base
from config import FUTConfig


class StrategyManage(Base):
    def __init__(self) -> None:
        extra = FUTConfig.pop("extra")
        super().__init__("FUT", [], "", **FUTConfig)
        self.tq_user = extra.get("tq_user")
        self.tq_pwd = extra.get("tq_pwd")
        self.api = None
        self.symbols_map = {}

    def connect(self) -> None:
        self.api = TqApi(auth=TqAuth(self.tq_user, self.tq_pwd))
        symbols = self.api.query_quotes(ins_class="CONT")
        for s in symbols:
            symbol = (s.split(".")[-1] + "L8").upper()
            self.symbols_map[symbol] = {
                "5M": self.api.get_kline_serial(s, 60 * 5, data_length=1000),
                "15M": self.api.get_kline_serial(s, 60 * 15, data_length=1000),
                "1H": self.api.get_kline_serial(s, 60 * 60 * 1, data_length=1000),
                "4H": self.api.get_kline_serial(s, 60 * 60 * 4, data_length=1000),
            }

    def disconnect(self) -> None:
        if self.api:
            try:
                self.api.close()
            except Exception as e:
                print(e)
            self.api = None
            logger.info(f"断开连接：{len(self.symbols_map.keys())}")

    def start(self) -> None:
        while True:
            now = datetime.now()
            run_time = ((now.time() < dtime(2, 30)) or (
                    dtime(8, 55) < now.time() < dtime(15, 0)
            ) or (now.time() > dtime(20, 55))) and now.weekday() < 5

            if run_time:
                try:
                    if not self.api:
                        self.connect()
                        logger.info(f"建立连接：{len(self.symbols_map.keys())}")
                    self.api.wait_update()

                    for symbol in self.symbols_map.keys():
                        for p in self.symbols_map[symbol].keys():
                            if not self.api.is_changing(self.symbols_map[symbol][p].iloc[-1], "datetime"):
                                continue
                            for name, cls in self.classes.items():
                                signal_info = {}
                                try:
                                    period = cls.period
                                    if period == p:
                                        signal = cls.on_signal(self.symbols_map[symbol])
                                        if signal:
                                            signal_info = {
                                                "market": self.market + period,
                                                "symbol": symbol.split(self.symbol_sep)[0],
                                                "direction": cls.direction,
                                                "conditions": cls.conditions,
                                            }
                                except Exception as e:
                                    logger.info(f"{name}({e}):\n{traceback.format_exc()}")

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

                except Exception as error:
                    self.disconnect()
                    logger.info(f"异常断开：{error}")
            else:
                self.disconnect()
            time.sleep(1)


def main() -> None:
    sm = StrategyManage()
    sm.start()


if __name__ == '__main__':
    main()
