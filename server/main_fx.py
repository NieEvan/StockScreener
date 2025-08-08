from modules.base import BaseApp
from config.settings import FXConfig


class StrategyManage(BaseApp):
    def __init__(self) -> None:
        fx_config = FXConfig.copy()
        fx_config.pop("extra")
        symbols = self.get_symbols()
        super().__init__("FX", symbols, "z", **fx_config)
        self.first_run = False
        self.log_run = True

    @staticmethod
    def get_symbols() -> list:
        symbols = [
            'EURAUDm', 'US30m', 'EURCADm', 'UKOILm', 'EURJPYm', 'EURNZDm', 'CHFJPYm', 'NZDUSDm', 'JP225m',
            'USTECm', 'XNGUSDm', 'CADJPYm', 'EURGBPm', 'GBPUSDm', 'GBPAUDm', 'XAUUSDm', 'XCUUSDm', 'USDCADm',
            'NZDCHFm', 'GBPNZDm', 'AUDCADm', 'CADCHFm', 'HK50m', 'GBPJPYm', 'USDCHFm', 'AUDNZDm', 'STOXX50m',
            'DE30m', 'XPBUSDm', 'GBPCHFm', 'AUDUSDm', 'FR40m', 'USOILm', 'US500m', 'NZDJPYm', 'XNIUSDm',
            'UK100m', 'AUDJPYm', 'EURUSDm', 'XZNUSDm', 'XAGUSDm', 'USDJPYm', 'XALUSDm', 'GBPCADm', 'AUS200m',
            'AUDCHFm', 'NZDCADm', 'EURCHFm'
        ]
        return symbols


def main() -> None:
    sm = StrategyManage()
    sm.start()


if __name__ == '__main__':
    main()
