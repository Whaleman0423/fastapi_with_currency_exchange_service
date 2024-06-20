# 實作 FastAPI API + 貨幣匯率轉換功能
使用 Python FastAPI 框架架設 API，並附加一個 Flutter 製作的 Web 前端作為功能測試頁面。

## 檔案目錄結構
```
.
├── Dockerfile
├── Dockerfile-dev
├── dependencies.py
├── docker-compose.yaml
├── main.py
├── readme.md
├── requirements.txt
├── routers # 路由
│   ├── __init__.py
│   └── router.py
├── schemas # 請求或 response 的 schema
│   ├── __init__.py
│   └── conversion_request.py
├── services # 邏輯服務類
│   ├── __init__.py
│   └── currency_exchange_service.py
├── tests # unit test
│   └── __init__.py
│   └── test_main.py
└── web # Flutter Web(基本匯率轉換輸入框、下拉選單、狀態欄與按鈕)
```

## 使用流程
1. 拉取程式碼並 Open Folder 開啟專案程式碼資料夾
2. (dev) 啟動容器並運行系統
3. (dev) 手動與單元測試 API  
a. GET Method, /ping  
b. GET Method, /ping  
c. Unit Test - Pytest  
d. 前端網頁測試
4. 觀察 OpenAPI Spec Docs
5. (prod) 生產部署

### 拉取程式碼並 Open Folder 開啟專案程式碼資料夾
```
git clone https://github.com/Whaleman0423/fastapi_with_currency_exchange_service.git
```

### (dev) 啟動容器並運行系統
接著啟動 Docker Desktop 或 Linux 的 Docker server，確認當下 port 並無 8000 port 後，執行以下指令：

```
# 開發用
# 啟動並進入容器
docker compose up -d
docker exec -it my-fastapi-app sh

# 啟動 fastapi 系統
uvicorn main:app --host 0.0.0.0 --reload
```
或
```
# 直接使用 Dockerfile 啟動系統
docker build -t fastapi-currency-converter .
docker run -d -p 8000:8000 fastapi-currency-converter
```

### (dev) 手動與單元測試 API
以下提供 API 的串接測試，可以使用 Postman 進行 API 測試，或是訪問 http://localhost:8000/ ，使用前端頁面串接後端 API 測試功能。

#### GET Method, /ping
使用 Postman GET 方法訪問或網頁瀏覽: http://localhost:8000/ping

Response: pong

#### GET Method, /convert?source=USD&target=JPY&amount=1,525
使用 Postman GET 方法訪問或網頁瀏覽:  
http://localhost:8000/convert?source=USD&target=JPY&amount=1,525

Response
```
# Status: 200
{
    "msg": "success",
    "amount": "170,496.53"
}
```

#### Unit Test - Pytest
在容器內部 /app 資料夾下，執行以下指令:
```
pytest
```
測試內容:  
* 測試 /ping 路由，確保服務器正常運行
* 測試正常的貨幣轉換
* 測試無效的來源貨幣
* 測試無效的目標貨幣
* 測試無效的金額輸入
* 測試帶有逗號的金額輸入

預期結果: 全部通過

#### 前端網頁測試
在啟動 fastapi 系統的前提下，訪問 http://localhost:8000/  
開啟前端網頁後，可以在「Amount」的輸入框輸入 數值，並選擇 Source 與 Target 的幣值，點選 Convert 進行轉換，測試情境參考以下:  
1. 正常轉換
a. Amount=1525、source=USD、target=JPY  
b. Amount=1,525、source=USD、target=JPY
c. Amount=1,525.00、source=USD、target=JPY
d. Amount=1,525.000、source=USD、target=JPY
2. 輸入值異常
a. Amount=1ax525、source=USD、target=JPY => Value Error, Invalid amount format
3. 未輸入
a. Amount=、source=USD、target=JPY => Value Error, Invalid amount format

#### 觀察 OpenAPI Spec Docs
fastapi 會自動生成 API 文件，訪問 http://localhost:8000/docs

#### (prod) 生產部署
提供 Dockerfile 作為 production 所使用。  

## Contact Author
Email: sheiyuray@gmail.com