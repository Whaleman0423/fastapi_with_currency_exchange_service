from pydantic import ValidationError
from dependencies import get_exchange_service
from fastapi import APIRouter, Depends, HTTPException
from schemas.conversion_request import ConversionRequest
from services.currency_exchange_service import CurrencyExchangeService
from decimal import Decimal, ROUND_HALF_UP

# 創建一個 FastAPI 路由器實例
router = APIRouter()

@router.get("/ping")
async def hello_world():
    """定義一個 GET 路由，測試服務器是否運行正常"""
    return 'pong'

# API路由
@router.get("/convert")
def convert_currency(source: str, target: str, amount: str, service: CurrencyExchangeService = Depends(get_exchange_service)):
    """
    執行匯率轉換並返回結果

    :param source: 來源貨幣
    :param target: 目標貨幣
    :param amount: 轉換金額
    :param service: 依賴注入的匯率服務
    :return: 轉換結果
    """
    try:
        # 創建請求對象並驗證輸入
        request = ConversionRequest(source=source, target=target, amount=amount)
    except ValidationError as e:
        print(type(e.errors()[0]))
        print(e.errors()[0]["msg"])
        raise HTTPException(status_code=400, detail=str(e.errors()))
    
    # 獲取匯率
    rate = service.get_rate(request.source, request.target)
    # 計算轉換後的金額並四捨五入到小數點後兩位
    request_amount = Decimal(str(request.amount))
    rate = Decimal(str(rate))
    converted_amount = (request_amount * rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # 格式化金額，加入千分位逗號
    formatted_amount = "{:,.2f}".format(converted_amount)
    
    return {"msg": "success", "amount": formatted_amount}
    