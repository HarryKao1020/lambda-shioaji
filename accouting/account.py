import shioaji as sj
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
import calendar

# ======= config ============
# 將上一層目錄加入路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 現在可以直接引入
from config import API_KEY, SECRET_KEY

# ======= end config ============


# 日期處理函數
def get_first_day_of_month(end_date_str):
    """根據月末日期取得該月第一天"""
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    first_day = end_date.replace(day=1)
    return first_day.strftime("%Y-%m-%d")


def get_first_day_of_quarter(end_date_str):
    """根據季末日期取得該季第一天"""
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    # 判斷該日期屬於哪個季度
    month = end_date.month
    if month in [1, 2, 3]:
        first_month = 1
    elif month in [4, 5, 6]:
        first_month = 4
    elif month in [7, 8, 9]:
        first_month = 7
    else:
        first_month = 10

    first_day = end_date.replace(month=first_month, day=1)
    return first_day.strftime("%Y-%m-%d")


def is_last_day_of_month(date_str):
    """判斷日期是否為月末最後一天"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
    return date_obj.day == last_day


def is_last_day_of_quarter(date_str):
    """判斷日期是否為季末最後一天"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    month = date_obj.month
    # 判斷月份是否為季末月份
    if month in [3, 6, 9, 12]:
        # 再判斷是否為該月最後一天
        return is_last_day_of_month(date_str)
    return False


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


# === 拉取證卷已實現損益 ====
def get_stock_profit_loss(api, start_date, end_date):
    """拉取證卷已實現損益"""
    try:
        print(f"查詢股票已實現損益期間: {start_date} 至 {end_date}")
        profitloss = api.list_profit_loss(api.stock_account, start_date, end_date)
        if not profitloss:
            print("該期間沒有股票已實現損益資料")
            return None

        df = pd.DataFrame(pnl.__dict__ for pnl in profitloss)
        # 計算總實現損益
        total_pnl = df["pnl"].sum() if "pnl" in df.columns and len(df) > 0 else 0

        # 將 pr_ratio 轉換為百分比 (乘以 100) 但保持數字格式
        if "pr_ratio" in df.columns:
            df["pr_ratio"] = (df["pr_ratio"] * 100).round(2)
        # 輸出結果
        print(f"股票總已實現損益：{total_pnl}")
        return df
    except Exception as e:
        print(f"拉取股票已實現損益時發生錯誤: {str(e)}")
        return None


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


# === 拉取期權已實現損益 ====
def get_futopt_profit_loss(api, start_date, end_date):
    """拉取期權已實現損益"""
    try:
        print(f"查詢期權已實現損益期間: {start_date} 至 {end_date}")
        profitloss = api.list_profit_loss(api.futopt_account, start_date, end_date)
        if not profitloss:
            print("該期間沒有期權已實現損益資料")
            return None

        df = pd.DataFrame(pnl.__dict__ for pnl in profitloss)
        # 計算總已實現損益
        total_pnl = df["pnl"].sum() if "pnl" in df.columns and len(df) > 0 else 0
        # 輸出結果
        print(f"期權總已實現損益：{total_pnl}")
        return df
    except Exception as e:
        print(f"拉取期權已實現損益時發生錯誤: {str(e)}")
        return None


# === 產生Excel報表 ===
def generate_excel_report(stock_df, futopt_df, period_type, end_date):
    """產生Excel報表"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if period_type == "month":
            filename = f"monthly_profit_loss_report_{end_date}_{timestamp}.xlsx"
            period_desc = f"月報表 ({end_date})"
        else:  # quarter
            filename = f"quarterly_profit_loss_report_{end_date}_{timestamp}.xlsx"
            period_desc = f"季報表 ({end_date})"

        # 創建Excel檔案
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            # 寫入股票資料
            if stock_df is not None and not stock_df.empty:
                stock_df.to_excel(writer, sheet_name="證券已實現損益", index=False)

                # 設定欄位寬度
                worksheet = writer.sheets["證券已實現損益"]
                for idx, col in enumerate(stock_df.columns):
                    max_length = (
                        max(stock_df[col].astype(str).map(len).max(), len(col)) + 2
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length

                # 設定pr_ratio為百分比格式
                if "pr_ratio" in stock_df.columns:
                    col_idx = stock_df.columns.get_loc("pr_ratio")
                    col_letter = chr(65 + col_idx)
                    for row_idx in range(2, len(stock_df) + 2):
                        cell = f"{col_letter}{row_idx}"
                        worksheet[cell].number_format = "0.00"

            # 寫入期權資料
            if futopt_df is not None and not futopt_df.empty:
                futopt_df.to_excel(writer, sheet_name="期權已實現損益", index=False)

                # 設定欄位寬度
                worksheet = writer.sheets["期權已實現損益"]
                for idx, col in enumerate(futopt_df.columns):
                    max_length = (
                        max(futopt_df[col].astype(str).map(len).max(), len(col)) + 2
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length

        print(f"已生成{period_desc}報表: {filename}")
        return filename
    except Exception as e:
        print(f"生成Excel報表時發生錯誤: {str(e)}")
        return None


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


def generate_monthly_report(api, month_end_date):
    """生成月報表"""
    # 確認輸入的日期是否為月末
    if not is_last_day_of_month(month_end_date):
        print(f"警告: 輸入的日期 {month_end_date} 可能不是月末")

    # 取得月初日期
    month_start_date = get_first_day_of_month(month_end_date)

    # 獲取損益資料
    stock_pl_df = get_stock_profit_loss(api, month_start_date, month_end_date)
    futopt_pl_df = get_futopt_profit_loss(api, month_start_date, month_end_date)

    # 生成報表
    generate_excel_report(stock_pl_df, futopt_pl_df, "month", month_end_date)


def generate_quarterly_report(api, quarter_end_date):
    """生成季報表"""
    # 確認輸入的日期是否為季末
    if not is_last_day_of_quarter(quarter_end_date):
        print(f"警告: 輸入的日期 {quarter_end_date} 可能不是季末")

    # 取得季初日期
    quarter_start_date = get_first_day_of_quarter(quarter_end_date)

    # 獲取損益資料
    stock_pl_df = get_stock_profit_loss(api, quarter_start_date, quarter_end_date)
    futopt_pl_df = get_futopt_profit_loss(api, quarter_start_date, quarter_end_date)

    # 生成報表
    generate_excel_report(stock_pl_df, futopt_pl_df, "quarter", quarter_end_date)


if __name__ == "__main__":
    api = connect_shioaji()
    if api:
        try:
            # 您可以在此處修改日期來生成不同月份或季度的報表

            # 生成月報表 (假設2025-03-31是3月最後一天)
            monthly_end_date = "2025-03-25"
            generate_monthly_report(api, monthly_end_date)

            # 生成季報表 (假設2025-03-31是第一季最後一天)
            quarterly_end_date = "2025-03-25"
            generate_quarterly_report(api, quarterly_end_date)

        finally:
            # 確保即使發生異常，也會登出
            api.logout()
            print("已登出")
