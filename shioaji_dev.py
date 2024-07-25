# for local test
import json
import shioaji as sj
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import date, timedelta


def calculate_moving_averages(stock_code, window=60, buy_price=None):
    # 創建，比如現在時間的前180天
    today = date.today()
    delta = timedelta(days=180)
    date_180 = today - delta
    # 取得歷史股價資料
    # k棒的api使用方式
    kbars = api.kbars(
        contract=api.Contracts.Stocks[stock_code],
        start=str(date_180),
        end=str(today),
    )
    df = pd.DataFrame({**kbars})
    df.ts = pd.to_datetime(df.ts)
    df.set_index("ts", inplace=True)

    # 日k13:30的K棒
    df = df.resample("D").last().dropna()

    # 計算移動平均線
    df["5MA"] = df["Close"].rolling(window=5).mean().round(2)
    df["10MA"] = df["Close"].rolling(window=10).mean().round(2)
    df["20MA"] = df["Close"].rolling(window=20).mean().round(2)
    df["60MA"] = df["Close"].rolling(window=60).mean().round(2)
    df["20MA/60MA"] = (df["20MA"] / df["60MA"]).round(2)
    # 計算價格差距百分比
    if buy_price is not None:
        df["5MA_diff"] = ((buy_price - df["5MA"]) / buy_price * 100).round(2)
        df["10MA_diff"] = ((buy_price - df["10MA"]) / buy_price * 100).round(2)
        df["20MA_diff"] = ((buy_price - df["20MA"]) / buy_price * 100).round(2)
        df["60MA_diff"] = ((buy_price - df["60MA"]) / buy_price * 100).round(2)

    return df[
        [
            "5MA",
            "10MA",
            "20MA",
            "60MA",
            "20MA/60MA",
            "5MA_diff",
            "10MA_diff",
            "20MA_diff",
            "60MA_diff",
        ]
    ].dropna()


def get_current_ma_diff(stock_code, buy_price=None):
    ma_data = calculate_moving_averages(stock_code, buy_price=buy_price)
    current_5ma_diff = ma_data["5MA_diff"].iloc[-1]
    current_10ma_diff = ma_data["10MA_diff"].iloc[-1]
    current_20ma_diff = ma_data["20MA_diff"].iloc[-1]
    current_60ma_diff = ma_data["60MA_diff"].iloc[-1]

    result = {
        "5MA_diff": current_5ma_diff,
        "10MA_diff": current_10ma_diff,
        "20MA_diff": current_20ma_diff,
        "60MA_diff": current_60ma_diff,
    }
    return json.dumps(result)


if __name__ == "__main__":
    api = sj.Shioaji(simulation=True)

    SHIOAJI_APIKEY = "DP6ayTE7r7zsyWfad4wfu5ZMDdQ4NA6wk1vPESXVihyG"
    SHIOAJI_SECRETKEY = "65bqwy975DsaDHamDxje8M3yUyqKCEuNRA9szAkrt996"
    accounts = api.login(SHIOAJI_APIKEY, SHIOAJI_SECRETKEY)
    print(accounts)

    print(calculate_moving_averages("2330", buy_price=979))
