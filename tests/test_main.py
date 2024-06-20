import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ping():
    """
    測試 /ping 路由，確保服務器正常運行
    """
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == 'pong'

def test_convert_success():
    """
    測試正常的貨幣轉換
    """
    response = client.get("/convert", params={"source": "USD", "target": "JPY", "amount": "1000"})
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "success"
    assert "amount" in data

def test_convert_invalid_source():
    """
    測試無效的來源貨幣
    """
    response = client.get("/convert", params={"source": "XXX", "target": "JPY", "amount": "1000"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid source or target currency"

def test_convert_invalid_target():
    """
    測試無效的目標貨幣
    """
    response = client.get("/convert", params={"source": "USD", "target": "XXX", "amount": "1000"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid source or target currency"

def test_convert_invalid_amount():
    """
    測試無效的金額輸入
    """
    response = client.get("/convert", params={"source": "USD", "target": "JPY", "amount": "abc"})
    assert response.status_code == 400
    data = response.json()
    assert "Invalid amount format" in eval(data["detail"])[0]["msg"]

def test_convert_amount_with_comma():
    """
    測試帶有逗號的金額輸入
    """
    response = client.get("/convert", params={"source": "USD", "target": "JPY", "amount": "1,000"})
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "success"
    assert "amount" in data
