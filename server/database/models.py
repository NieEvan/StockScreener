from typing import Dict, Any

class DataModel:
    @staticmethod
    def create_document(symbol: str, market: str, timeframe: str, time: str, 
                       direction: str, conditions: str, warn_id: str) -> Dict[str, Any]:
        return {
            "symbol": symbol,
            "market": market,
            "timeframe": timeframe,
            "time": time,
            "direction": direction,
            "conditions": conditions,
            "warn_id": warn_id
        } 

class SignalModel:
    @staticmethod
    def create_document(symbol: str, market: str, time: str, 
                       direction: str, conditions: str, warn_id: str) -> Dict[str, Any]:
        return {
            "symbol": symbol,
            "market": market,
            "time": time,
            "direction": direction,
            "conditions": conditions,
            "warn_id": warn_id
        } 
        