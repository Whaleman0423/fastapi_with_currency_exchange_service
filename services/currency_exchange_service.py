from fastapi import  HTTPException
from typing import Dict


# 匯率服務
class CurrencyExchangeService:
    def __init__(self, rates: Dict):
        self.rates = rates

    def get_rate(self, source: str, target: str) -> float:
        """
        獲取來源貨幣到目標貨幣的匯率

        :param source: 來源貨幣
        :param target: 目標貨幣
        :return: 匯率
        """
        # 若輸入的 source 或 target 系統並不提供時的案例
        if source not in self.rates or target not in self.rates[source]:
            raise HTTPException(status_code=400, detail="Invalid source or target currency")
        return self.rates[source][target]