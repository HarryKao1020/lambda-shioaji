# for aws lambda


import shioaji as sj
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import date, timedelta


def lambda_handler(event, context):
    api_key = event["apiKey"]
    secret_key = event["secretKey"]
    action = event["action"]

    if not api_key or not secret_key:
        return {"statusCode": 400, "body": json.dumps("Bad Request")}

    api = sj.Shioaji(simulation=True)
    accounts = api.login(api_key, secret_key)

    if len(accounts) == 0:
        return {"statusCode": 404, "body": json.dumps("No accounts found")}

    if action == "get_account_id":
        return {"statusCode": 200, "body": accounts[0].account_id}

    elif action == "get_ma_stop_loss":
        stock_code = event["stockCode"]
        buy_price = event["buyPrice"]
        ma_diff_data = get_current_ma_diff(event, stock_code, buy_price=buy_price)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"account_id": accounts[0].account_id, "responseData": ma_diff_data}
            ),
        }
    elif action == "get_macd_info":
        macd_info = get_index_macd(event)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"account_id": accounts[0].account_id, "responseData": macd_info}
            ),
        }
    elif action == "get_stock_macd":
        stock_code = event["stockCode"]
        stock_macd = get_stock_macd(event, stock_code)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"account_id": accounts[0].account_id, "responseData": stock_macd}
            ),
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "account_id": accounts[0].account_id,
                    "responseData": "Get Shioaji API Error Occur !",
                }
            ),
        }


def calculate_moving_averages(event, stock_code, window=60, buy_price=None):

    api_key = event["apiKey"]
    secret_key = event["secretKey"]
    # 創建，比如現在時間的前180天
    today = date.today()
    delta = timedelta(days=180)
    date_180 = today - delta
    # 取得歷史股價資料
    # k棒的api使用方式
    api = sj.Shioaji(simulation=True)
    accounts = api.login(api_key, secret_key)
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


# //// 計算ma跟買價的假差
def get_current_ma_diff(event, stock_code, buy_price=None):
    ma_data = calculate_moving_averages(event, stock_code, buy_price=buy_price)
    current_5ma_diff = ma_data["5MA_diff"].iloc[-1]
    current_10ma_diff = ma_data["10MA_diff"].iloc[-1]
    current_20ma_diff = ma_data["20MA_diff"].iloc[-1]
    current_60ma_diff = ma_data["60MA_diff"].iloc[-1]
    current_2060_diff = ma_data["20MA/60MA"].iloc[-1]

    result = {
        "5MA_diff": current_5ma_diff,
        "10MA_diff": current_10ma_diff,
        "20MA_diff": current_20ma_diff,
        "60MA_diff": current_60ma_diff,
        "20ma_60ma_diff": current_2060_diff,
    }
    return json.dumps(result)


# ////////// 取加權指數&櫃買指數的MACD方向
def get_index_macd(event):
    start_day = date.today() - timedelta(days=365)
    end_day = date.today()
    api_key = event["apiKey"]
    secret_key = event["secretKey"]
    api = sj.Shioaji(simulation=True)
    accounts = api.login(api_key, secret_key)
    tse_index = api.Contracts.Indexs.TSE["001"]
    otc_index = api.Contracts.Indexs.OTC["101"]

    # 取得加權指數資料
    tse_kbars = api.kbars(contract=tse_index, start=str(start_day), end=str(end_day))
    # 取得櫃買指數資料
    otc_kbars = api.kbars(contract=otc_index, start=str(start_day), end=str(end_day))

    tse_df = pd.DataFrame({**tse_kbars})
    tse_df.ts = pd.to_datetime(tse_df.ts)
    tse_df.set_index("ts", inplace=True)
    otc_df = pd.DataFrame({**otc_kbars})
    otc_df.ts = pd.to_datetime(otc_df.ts)
    otc_df.set_index("ts", inplace=True)

    # 日k13:30的K棒
    tse_daily_df = tse_df.resample("D").last().dropna()
    otc_daily_df = otc_df.resample("D").last().dropna()

    tse_macd_df = calculate_macd(tse_daily_df)
    otc_macd_df = calculate_macd(otc_daily_df)

    tse_response_msg = index_macd_notify(tse_macd_df["Hist"])
    otc_response_msg = index_macd_notify(otc_macd_df["Hist"])

    result = {"TSE_MACD": tse_response_msg, "OTC_MACD": otc_response_msg}
    return json.dumps(result)


# 取個股macd方向
def get_stock_macd(event, stock_code):
    start_day = date.today() - timedelta(days=365)
    end_day = date.today()
    api_key = event["apiKey"]
    secret_key = event["secretKey"]
    api = sj.Shioaji(simulation=True)
    accounts = api.login(api_key, secret_key)
    kbars = api.kbars(
        contract=api.Contracts.Stocks[stock_code],
        start=str(start_day),
        end=str(end_day),
    )
    df = pd.DataFrame({**kbars})
    df.ts = pd.to_datetime(df.ts)
    df.set_index("ts", inplace=True)

    # 日k13:30的K棒
    df = df.resample("D").last().dropna()
    stock_macd_df = calculate_macd(df)
    stock_macd_message = stock_macd_notify(stock_macd_df["Hist"])
    result = {"STOCK_MACD": stock_macd_message}
    return json.dumps(result)


# 計算 EMA
def calculate_ema(df, column, span):
    return df[column].ewm(span=span, adjust=False).mean()


# 計算 MACD
def calculate_macd(df, short_span=12, long_span=26, signal_span=9):
    df["EMA_short"] = calculate_ema(df, "Close", short_span)
    df["EMA_long"] = calculate_ema(df, "Close", long_span)
    df["MACD"] = df["EMA_short"] - df["EMA_long"]
    df["Signal"] = calculate_ema(df, "MACD", signal_span)
    df["Hist"] = df["MACD"] - df["Signal"]
    return df


# 判斷MACD的趨勢
def index_macd_notify(df):
    today_hist = df.iloc[-1]
    yesterday_hist = df.iloc[-2]
    if today_hist > 0:
        if today_hist > yesterday_hist:
            response_message = "『紅柱增長』\n 可以積極做多\n"

            response_message += "找到主流族群中最好的,打好打滿"
        else:
            response_message = "『紅柱縮短』\n 降低槓桿跟部位,不再買入,庫存留倉觀察"
    else:
        if today_hist < yesterday_hist:
            response_message = (
                "『綠柱增長』\n 不要看盤了,買了錢會賠光光!會賠光!會很痛苦\n"
            )
            response_message += "禁止買入任何部位,也嚴禁抄底"
            response_message += "如果持股已經套牢，彈上來是給你停損的"
        else:
            response_message = "『綠柱縮短』\n 可以嘗試做多強勢族群,不上槓桿,嚴守停損\n"
            response_message += "記住這是搶反彈,停損一定要守在成本!"
            response_message += "如果持股已經套牢，彈上來是給你停損的"

    return response_message


def stock_macd_notify(df):
    today_hist = df.iloc[-1]
    yesterday_hist = df.iloc[-2]
    if today_hist > 0:
        if today_hist > yesterday_hist:
            response_message = "『紅柱增長』,續抱"
        else:
            response_message = "『紅柱縮短』,停利降低部位"
    else:
        if today_hist < yesterday_hist:
            response_message = "『綠柱增長』,不要買進"
        else:
            response_message = "『綠柱縮短』,嘗試抄底建倉\n 小量進場試單"

    return response_message


# ////////// End 取加權指數&櫃買指數的MACD方向 //////
