import shioaji as sj
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# ======= config ============
# 將上一層目錄加入路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 現在可以直接引入
from config import API_KEY, SECRET_KEY

# ======= end config ============

end_date = datetime.now().strftime("%Y-%m-%d")
print(f"end_date:{end_date}")


# === 拉取證卷未實現損益 ===
def get_stock_unrealized_profit_loss(api):
    """拉取證券未實現損益"""
    try:
        # 查詢未實現損益
        positions = api.list_positions(api.stock_account)
        if not positions:
            print("股票目前沒有持倉")
            return None

        # 將持倉資料轉換為 DataFrame
        df = pd.DataFrame(position.__dict__ for position in positions)
        # 計算總未實現損益
        total_pnl = df["pnl"].sum() if "pnl" in df.columns else 0

        # 輸出結果
        print(f"股票總未實現損益：{total_pnl}")

        return df
    except Exception as e:
        print(f"拉取股票未實現損益時發生錯誤: {str(e)}")
        return None


# === end 拉取證卷未實現損益 ===


# === 拉取證卷已實現損益 ====
def get_stock_profit_loss(api, start_date, end_date):
    """拉取證卷已實現損益"""
    try:
        profitloss = api.list_profit_loss(api.stock_account, start_date, end_date)
        df = pd.DataFrame(pnl.__dict__ for pnl in profitloss)
        # 計算總實現損益
        total_pnl = df["pnl"].sum() if "pnl" in df.columns else 0

        # 將 pr_ratio 轉換為百分比 (乘以 100) 但保持數字格式
        if "pr_ratio" in df.columns:
            df["pr_ratio"] = (df["pr_ratio"] * 100).round(2)
        # 輸出結果
        print(f"股票總已實現損益：{total_pnl}")
        return df
    except Exception as e:
        print(f"拉取股票已實現損益時發生錯誤: {str(e)}")
        return None


# === End 拉取證卷已實現損益 ====


# ======================== Future and Option =========================
# === 拉取期權未實現損益 ===
def get_futopt_unrealized_profit_loss(api):
    """拉取期權未實現損益"""
    try:
        # 查詢未實現損益
        positions = api.list_positions(api.futopt_account)

        if not positions:
            print("期權目前沒有持倉")
            return None

        # 將持倉資料轉換為 DataFrame
        df = pd.DataFrame(position.__dict__ for position in positions)
        # 計算總未實現損益
        total_pnl = df["pnl"].sum() if "pnl" in df.columns else 0

        # 輸出結果
        print(f"期權總未實現損益：{total_pnl}")

        return df
    except Exception as e:
        print(f"拉取期權未實現損益時發生錯誤: {str(e)}")
        return None


# === end 拉取期權未實現損益 ===


# === 拉取期權已實現損益 ====
def get_futopt_profit_loss(api, start_date, end_date):
    """拉取期權已實現損益"""
    try:
        profitloss = api.list_profit_loss(api.futopt_account, start_date, end_date)
        df = pd.DataFrame(pnl.__dict__ for pnl in profitloss)
        # 計算總已實現損益
        total_pnl = df["pnl"].sum() if "pnl" in df.columns else 0
        # 輸出結果
        print(f"期權總已實現損益：{total_pnl}")
        return df
    except Exception as e:
        print(f"拉取期權已實現損益時發生錯誤: {str(e)}")
        return None


# === End 拉取期權已實現損益 ====


# === connect to shioaji ===
def connect_shioaji():
    """連接到永豐金證券 API 並返回 API 物件"""
    try:
        # api = sj.Shioaji(simulation=True)  # 模擬模式
        api = sj.Shioaji()  # 正式模式
        accounts = api.login(api_key=API_KEY, secret_key=SECRET_KEY)
        print("登入成功")
        print(f"期貨帳戶：{api.futopt_account}")
        print(f"股票帳戶：{api.stock_account}")
        return api
    except Exception as e:
        print(f"登入失敗: {str(e)}")
        return None


if __name__ == "__main__":
    api = connect_shioaji()
    if api:
        try:
            # # 拉取未實現損益
            # stock_unrealized_pl_df = get_stock_unrealized_profit_loss(api)
            # print(stock_unrealized_pl_df)
            # # 拉取未實現損益
            # fuopt_unrealized_pl_df = get_futopt_unrealized_profit_loss(api)
            # print(fuopt_unrealized_pl_df)

            # stock已實現
            stock_pl_df = get_stock_profit_loss(api, "2025-01-01", "2025-03-25")
            print(stock_pl_df)

            # future/option 已實現
            futopt_pl_df = get_futopt_profit_loss(api, "2025-02-01", "2025-03-01")
            print(futopt_pl_df)

        finally:
            # 確保即使發生異常，也會登出
            api.logout()
            print("已登出")
