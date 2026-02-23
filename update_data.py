import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

# 1. 分類整理標的清單
# 台股上市 (個股/ETF)
tw_listed = [
    "0050", "0056", "006208", "00713", "00850", "00878", "00940",
    "00929", "00646", "00662", "1101", "1102", "1217", "1218",
    "1432", "1609", "1904", "2002", "2201", "2204", "2303",
    "2356", "2379", "2409", "2646", "2880", "2883", "2885",
    "2886", "2887", "2890", "2891", "3034", "3231", "4588",
    "6282", "8046", "2324", "2353"
]

# 台股上櫃 (主要為債券 ETF 與部分個股)
tw_otc = [
    "00719B", "00722B", "00751B", "00761B", "00772B", "00937B", "6233", "8040", "6648"
]

# 美股標的
us_market = ["QQQM", "VOO", "IAU", "VT", "VWO"]

# 格式化所有 Tickers
all_tickers = [t + ".TW" for t in tw_listed] + [t + ".TWO" for t in tw_otc] + us_market

# 2. 開始抓取數據
results = []
us_list = ["QQQM", "VOO", "VT", "VWO"]

all_tickers += us_list
results = []

print(f"🚀 開始抓取數據 (全預估模式)... 共 {len(all_tickers)} 檔")

for t in all_tickers:
    try:
        tk = yf.Ticker(t)
        divs = tk.dividends.tail(5) # 抓最近 5 筆
        
        if not divs.empty:
            for date, val in divs.items():
                ex_date = date.date()
                
                # 判斷市場並設定預估天數
                offset = 30 if (".TW" in t or ".TWO" in t) else 20
                pay_date_est = ex_date + timedelta(days=offset)
                
                results.append({
                    "Ticker": t.split('.')[0],
                    "Ex-Date": ex_date,
                    "Pay-Date": pay_date_est,
                    "Amount": val,
                    "Market": "TW" if ".TW" in t or ".TWO" in t else "US"
                })
            print(f"✅ {t} 完成")
        else:
            print(f"⚠️ {t} 無配息數據")
        
        time.sleep(0.5) # 避免 API 拒絕連線
    except Exception as e:
        print(f"❌ {t} 錯誤: {e}")

# 2. 儲存結果
df = pd.DataFrame(results)
if not df.empty:
    df = df.sort_values(by="Ex-Date", ascending=False)
    df.to_csv("dividend_data.csv", index=False)
    print("\n🎊 全部完成！資料已存入 dividend_data.csv")
