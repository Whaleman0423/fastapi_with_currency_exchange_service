import re

from pydantic import BaseModel, Field, field_validator


# 請求模型
class ConversionRequest(BaseModel):
    source: str = Field(..., pattern="^[A-Z]{3}$")
    target: str = Field(..., pattern="^[A-Z]{3}$")
    amount: str 

    @field_validator('amount')
    def validate_amount(cls, v):
        """
        驗證並轉換金額格式

        :param v: 金額字串
        :return: 金額數值
        """
        v = v.replace(',', '')
        if not re.match(r"^\d+(\.\d+)?$", v):
            raise ValueError('Invalid amount format')
        return float(v)