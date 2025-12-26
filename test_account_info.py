#!/usr/bin/env python3
"""
測試 get_account_info 函數
從 .env 讀取 API Key 和 Secret Key
"""

import os
import json
from dotenv import load_dotenv
from lambda_function import get_account_info

# 載入 .env 檔案
load_dotenv()


def test_get_account_info():
    """測試取得帳務資訊"""

    # 從環境變數取得 API Key 和 Secret Key
    api_key = os.getenv("SHIOAJI_APIKEY")
    secret_key = os.getenv("SHIOAJI_SECRETKEY")

    if not api_key or not secret_key:
        print("錯誤: 請在 .env 檔案中設定 API_KEY 和 SECRET_KEY")
        print("格式範例:")
        print("API_KEY=your_api_key_here")
        print("SECRET_KEY=your_secret_key_here")
        return

    # 建立測試 event
    event = {"apiKey": api_key, "secretKey": secret_key}

    print("=" * 80)
    print("開始測試 get_account_info 函數")
    print("=" * 80)

    try:
        # 呼叫函數
        result = get_account_info(event)

        if result is None:
            print("錯誤: 無法取得帳戶資訊（可能沒有登入成功）")
            return

        # 解析 JSON 結果
        account_info = json.loads(result)

        # 美化輸出
        print("\n" + "=" * 80)
        print("期貨部位曝險分析")
        print("=" * 80 + "\n")

        # 顯示每個合約的詳細資訊
        if "contracts" in account_info and len(account_info["contracts"]) > 0:
            print("持倉明細:")
            print("-" * 80)
            for i, contract in enumerate(account_info["contracts"], 1):
                print(f"\n合約 {i}:")
                print(f"  名稱: {contract['contract_name']}")
                print(f"  數量: {contract['quantity']}")
                print(f"  價格: {contract['price']:,.2f}")
                print(f"  曝險金額: {contract['exposure']:,.0f} 元")
                print(f"  未實現損益: {contract['pnl']:,.0f} 元")
            print("\n" + "-" * 80)
        else:
            print("目前沒有期貨部位\n")

        # 顯示總計資訊
        print("\n總計資訊:")
        print("-" * 80)
        print(f"總曝險金額: {account_info.get('總曝險金額', 'N/A')}")
        print(f"未實現損益: {account_info.get('未實現損益', 'N/A')}")

        if "權益數" in account_info:
            print(f"\n保證金資訊:")
            print("-" * 80)
            print(f"權益數: {account_info.get('權益數', 'N/A')}")
            print(f"槓桿倍數: {account_info.get('槓桿倍數', 'N/A')}")
            print(f"原始保證金: {account_info.get('原始保證金', 'N/A')}")
            print(f"保證金使用率: {account_info.get('保證金使用率', 'N/A')}")

            # 風險評估
            leverage_str = account_info.get("槓桿倍數", "0x")
            leverage = float(leverage_str.replace("x", ""))

            print(f"\n風險評估:")
            print("-" * 80)
            if leverage > 3:
                print(f"  ⚠️  警告: 槓桿倍數 {leverage:.2f}x 較高，請注意風險控管")
            elif leverage > 2:
                print(f"  ⚡ 提醒: 槓桿倍數 {leverage:.2f}x 中等，建議留意部位")
            else:
                print(f"  ✓ 槓桿倍數 {leverage:.2f}x 相對安全")

        print("\n" + "=" * 80)

        # 顯示完整 JSON（選擇性）
        print("\n完整 JSON 回應:")
        print("-" * 80)
        print(json.dumps(account_info, indent=2, ensure_ascii=False))
        print("=" * 80)

    except Exception as e:
        print(f"\n錯誤: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_get_account_info()
