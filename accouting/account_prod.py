import shioaji as sj
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
import calendar
import math

# ======= config ============
# 將上一層目錄加入路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 現在可以直接引入
from config import API_KEY, SECRET_KEY

# ======= end config ============


# 日期處理函數
def get_previous_month_11th(current_date):
    """獲取上個月11號的日期"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 獲取上個月的年和月
    if current_date.month == 1:
        prev_year = current_date.year - 1
        prev_month = 12
    else:
        prev_year = current_date.year
        prev_month = current_date.month - 1

    # 生成上個月11號的日期
    prev_month_11th = datetime(prev_year, prev_month, 11)

    return prev_month_11th.strftime("%Y-%m-%d")


def get_current_month_11th(current_date):
    """獲取當前月11號的日期"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 生成當前月11號的日期
    current_month_11th = datetime(current_date.year, current_date.month, 11)

    return current_month_11th.strftime("%Y-%m-%d")


def get_quarter_end_next_month_11th(current_date):
    """獲取季度結束後的下個月11號日期"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 獲取當前季度的結束月
    month = current_date.month
    quarter_end_month = math.ceil(month / 3) * 3

    # 獲取下個月
    if quarter_end_month == 12:
        next_month_year = current_date.year + 1
        next_month = 1
    else:
        next_month_year = current_date.year
        next_month = quarter_end_month + 1

    # 生成下個月11號的日期
    next_month_11th = datetime(next_month_year, next_month, 11)

    return next_month_11th.strftime("%Y-%m-%d")


def get_quarter_start_previous_quarter_end_next_month_11th(current_date):
    """獲取上一季度結束後的下個月11號日期（季度開始日期）"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 獲取當前季度
    month = current_date.month
    current_quarter = math.ceil(month / 3)

    # 獲取上一季度的結束月
    if current_quarter == 1:
        prev_quarter_end_year = current_date.year - 1
        prev_quarter_end_month = 12
    else:
        prev_quarter_end_year = current_date.year
        prev_quarter_end_month = (current_quarter - 1) * 3

    # 獲取上一季度結束後的下個月
    if prev_quarter_end_month == 12:
        next_month_year = prev_quarter_end_year + 1
        next_month = 1
    else:
        next_month_year = prev_quarter_end_year
        next_month = prev_quarter_end_month + 1

    # 生成該月11號的日期
    next_month_11th = datetime(next_month_year, next_month, 11)

    return next_month_11th.strftime("%Y-%m-%d")


def get_third_wednesday_of_month(year, month):
    """獲取指定年月的第三週週三日期"""
    # 獲取該月第一天
    first_day = datetime(year, month, 1)

    # 計算第一個週三的日期
    # 週一為0，週日為6
    days_until_wednesday = (2 - first_day.weekday()) % 7
    first_wednesday = first_day + timedelta(days=days_until_wednesday)

    # 第三個週三 = 第一個週三 + 2週
    third_wednesday = first_wednesday + timedelta(days=14)

    return third_wednesday


def get_current_month_third_wednesday(current_date):
    """獲取當前月的第三週週三"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 獲取第三週週三
    third_wednesday = get_third_wednesday_of_month(
        current_date.year, current_date.month
    )

    return third_wednesday.strftime("%Y-%m-%d")


def get_previous_month_third_wednesday(current_date):
    """獲取上個月的第三週週三"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 獲取上個月的年和月
    if current_date.month == 1:
        prev_year = current_date.year - 1
        prev_month = 12
    else:
        prev_year = current_date.year
        prev_month = current_date.month - 1

    # 獲取上個月的第三週週三
    third_wednesday = get_third_wednesday_of_month(prev_year, prev_month)

    return third_wednesday.strftime("%Y-%m-%d")


def get_quarter_end_month_third_wednesday(current_date):
    """獲取當前季度最後一個月的第三週週三"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 獲取當前季度的結束月
    month = current_date.month
    quarter_end_month = math.ceil(month / 3) * 3

    # 獲取該月的第三週週三
    third_wednesday = get_third_wednesday_of_month(current_date.year, quarter_end_month)

    return third_wednesday.strftime("%Y-%m-%d")


def get_previous_quarter_end_month_third_wednesday(current_date):
    """獲取上一季度最後一個月的第三週週三"""
    # 將當前日期轉換為datetime對象
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # 獲取當前季度
    month = current_date.month
    current_quarter = math.ceil(month / 3)

    # 獲取上一季度的結束月
    if current_quarter == 1:
        prev_quarter_end_year = current_date.year - 1
        prev_quarter_end_month = 12
    else:
        prev_quarter_end_year = current_date.year
        prev_quarter_end_month = (current_quarter - 1) * 3

    # 獲取該月的第三週週三
    third_wednesday = get_third_wednesday_of_month(
        prev_quarter_end_year, prev_quarter_end_month
    )

    return third_wednesday.strftime("%Y-%m-%d")


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
def generate_excel_report(
    stock_df, futopt_df, period_type, end_date, report_description=""
):
    """產生Excel報表"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if period_type == "month":
            filename = f"monthly_profit_loss_report_{end_date}_{timestamp}.xlsx"
            period_desc = f"月報表 ({report_description})"
        else:  # quarter
            filename = f"quarterly_profit_loss_report_{end_date}_{timestamp}.xlsx"
            period_desc = f"季報表 ({report_description})"

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


def generate_stock_monthly_report(api, report_date):
    """生成股票月報表 (從上個月11號到本月11號)"""
    # 將報表日期轉換為datetime對象以便操作
    if isinstance(report_date, str):
        report_date = datetime.strptime(report_date, "%Y-%m-%d")

    # 獲取本月11號和上個月11號
    current_month_11th = get_current_month_11th(report_date)
    previous_month_11th = get_previous_month_11th(report_date)

    # 確保開始日期早於結束日期
    start_date = previous_month_11th
    end_date = current_month_11th

    # 獲取股票損益資料
    stock_pl_df = get_stock_profit_loss(api, start_date, end_date)

    # 生成報表描述
    report_description = f"股票月報表 ({start_date} 至 {end_date})"

    # 生成報表
    generate_excel_report(stock_pl_df, None, "month", end_date, report_description)


def generate_stock_quarterly_report(api, report_date):
    """生成股票季報表 (按照每季結束後的下個月11號結算)"""
    # 將報表日期轉換為datetime對象以便操作
    if isinstance(report_date, str):
        report_date = datetime.strptime(report_date, "%Y-%m-%d")

    # 獲取當前季度結束後的下個月11號和上一季度結束後的下個月11號
    end_date = get_quarter_end_next_month_11th(report_date)
    start_date = get_quarter_start_previous_quarter_end_next_month_11th(report_date)

    # 獲取股票損益資料
    stock_pl_df = get_stock_profit_loss(api, start_date, end_date)

    # 生成報表描述
    report_description = f"股票季報表 ({start_date} 至 {end_date})"

    # 生成報表
    generate_excel_report(stock_pl_df, None, "quarter", end_date, report_description)


def generate_futures_monthly_report(api, report_date):
    """生成期貨月報表 (以每月第三週週三作為結算日)"""
    # 將報表日期轉換為datetime對象以便操作
    if isinstance(report_date, str):
        report_date = datetime.strptime(report_date, "%Y-%m-%d")

    # 獲取當前月和上個月的第三週週三
    current_month_third_wednesday = get_current_month_third_wednesday(report_date)
    previous_month_third_wednesday = get_previous_month_third_wednesday(report_date)

    # 確保開始日期早於結束日期
    start_date = previous_month_third_wednesday
    end_date = current_month_third_wednesday

    # 獲取期貨損益資料
    futopt_pl_df = get_futopt_profit_loss(api, start_date, end_date)

    # 生成報表描述
    report_description = f"期貨月報表 ({start_date} 至 {end_date})"

    # 生成報表
    generate_excel_report(None, futopt_pl_df, "month", end_date, report_description)


def generate_futures_quarterly_report(api, report_date):
    """生成期貨季報表 (從上一季最後一月的第三週週三到本季最後一月的第三週週三)"""
    # 將報表日期轉換為datetime對象以便操作
    if isinstance(report_date, str):
        report_date = datetime.strptime(report_date, "%Y-%m-%d")

    # 獲取當前季度最後一個月和上一季度最後一個月的第三週週三
    current_quarter_third_wednesday = get_quarter_end_month_third_wednesday(report_date)
    previous_quarter_third_wednesday = get_previous_quarter_end_month_third_wednesday(
        report_date
    )

    # 確保開始日期早於結束日期
    start_date = previous_quarter_third_wednesday
    end_date = current_quarter_third_wednesday

    # 獲取期貨損益資料
    futopt_pl_df = get_futopt_profit_loss(api, start_date, end_date)

    # 生成報表描述
    report_description = f"期貨季報表 ({start_date} 至 {end_date})"

    # 生成報表
    generate_excel_report(None, futopt_pl_df, "quarter", end_date, report_description)


def generate_combined_monthly_report(api, report_date):
    """生成綜合月報表 (股票+期貨)"""
    # 將報表日期轉換為datetime對象以便操作
    if isinstance(report_date, str):
        report_date = datetime.strptime(report_date, "%Y-%m-%d")

    # 股票時間範圍: 從上個月11號到本月11號
    stock_start_date = get_previous_month_11th(report_date)
    stock_end_date = get_current_month_11th(report_date)

    # 期貨時間範圍: 從上個月第三週週三到本月第三週週三
    futures_start_date = get_previous_month_third_wednesday(report_date)
    futures_end_date = get_current_month_third_wednesday(report_date)

    # 獲取損益資料
    stock_pl_df = get_stock_profit_loss(api, stock_start_date, stock_end_date)
    futopt_pl_df = get_futopt_profit_loss(api, futures_start_date, futures_end_date)

    # 生成報表描述
    report_description = (
        f"綜合月報表 (股票: {stock_start_date} 至 {stock_end_date}, "
        f"期貨: {futures_start_date} 至 {futures_end_date})"
    )

    # 生成報表
    generate_excel_report(
        stock_pl_df,
        futopt_pl_df,
        "month",
        report_date.strftime("%Y-%m-%d"),
        report_description,
    )


def generate_combined_quarterly_report(api, report_date):
    """生成綜合季報表 (股票+期貨)"""
    # 將報表日期轉換為datetime對象以便操作
    if isinstance(report_date, str):
        report_date = datetime.strptime(report_date, "%Y-%m-%d")

    # 股票時間範圍: 按照每季結束後的下個月11號結算
    stock_end_date = get_quarter_end_next_month_11th(report_date)
    stock_start_date = get_quarter_start_previous_quarter_end_next_month_11th(
        report_date
    )

    # 期貨時間範圍: 從上一季最後一月的第三週週三到本季最後一月的第三週週三
    futures_end_date = get_quarter_end_month_third_wednesday(report_date)
    futures_start_date = get_previous_quarter_end_month_third_wednesday(report_date)

    # 獲取損益資料
    stock_pl_df = get_stock_profit_loss(api, stock_start_date, stock_end_date)
    futopt_pl_df = get_futopt_profit_loss(api, futures_start_date, futures_end_date)

    # 生成報表描述
    report_description = (
        f"綜合季報表 (股票: {stock_start_date} 至 {stock_end_date}, "
        f"期貨: {futures_start_date} 至 {futures_end_date})"
    )

    # 生成報表
    generate_excel_report(
        stock_pl_df,
        futopt_pl_df,
        "quarter",
        report_date.strftime("%Y-%m-%d"),
        report_description,
    )


if __name__ == "__main__":
    api = connect_shioaji()
    if api:
        try:
            # 使用當前日期作為報表日期
            report_date = datetime.now()

            # 生成不同類型的報表
            print("\n===== 生成股票月報表 =====")
            generate_stock_monthly_report(api, report_date)

            print("\n===== 生成期貨月報表 =====")
            generate_futures_monthly_report(api, report_date)

            print("\n===== 生成綜合月報表 =====")
            generate_combined_monthly_report(api, report_date)

            print("\n===== 生成股票季報表 =====")
            generate_stock_quarterly_report(api, report_date)

            print("\n===== 生成期貨季報表 =====")
            generate_futures_quarterly_report(api, report_date)

            print("\n===== 生成綜合季報表 =====")
            generate_combined_quarterly_report(api, report_date)

        finally:
            # 確保即使發生異常，也會登出
            api.logout()
            print("已登出")
