#!/usr/bin/env python3
"""
台灣郵遞區號查詢小幫手
使用 zip5.5432.tw API 查詢地址對應的 3+2 / 3+3 碼郵遞區號
API 來源: https://zip5.5432.tw
Created by Keith K.S Lee by Claude on 20260309
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


API_URL = "https://zip5.5432.tw/zip5json.py"


def query_zipcode(address: str) -> dict | None:
    """查詢地址對應的郵遞區號，回傳 API 的 JSON 結果。查詢失敗時回傳 None。"""
    params = urllib.parse.urlencode({"adrs": address})
    url = f"{API_URL}?{params}"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "PostalHelper/1.0",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"網路錯誤: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print("無法解析 API 回傳的資料", file=sys.stderr)
        return None

    return data


def display_result(data: dict) -> None:
    """將查詢結果以易讀的格式印出。"""
    print()
    print(f"  原輸入地址:       {data.get('adrs', '')}")
    print(f"  郵遞區號 (3+2):   {data.get('zipcode', '查無資料')}")
    print(f"  查詢結果 (3+2):   {data.get('new_adrs', '')}")
    print(f"  郵遞區號 (3+3):   {data.get('zipcode6', '查無資料')}")
    print(f"  查詢結果 (3+3):   {data.get('new_adrs6', '')}")
    print()

    zipcode6 = data.get("zipcode6", "")
    zipcode5 = data.get("zipcode", "")

    if zipcode6:
        print(f"  >>> 6 碼郵遞區號: {zipcode6}")
    elif zipcode5:
        print(f"  >>> 5 碼郵遞區號: {zipcode5}")
        print("  (無 3+3 碼資料，顯示 3+2 碼)")
    else:
        print("  >>> 查無郵遞區號，請確認地址是否正確")

    print()


def interactive_mode() -> None:
    """互動模式：持續接受使用者輸入地址進行查詢。"""
    print("台灣郵遞區號查詢小幫手 (輸入 q 或 Ctrl+C 離開)")
    print("=" * 50)

    while True:
        try:
            address = input("\n請輸入地址: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再見!")
            break

        if not address:
            continue
        if address.lower() == "q":
            print("再見!")
            break

        data = query_zipcode(address)
        if data is None:
            continue
        display_result(data)
        time.sleep(2)


def main() -> None:
    """解析命令列參數並執行查詢或進入互動模式。"""
    parser = argparse.ArgumentParser(
        description="台灣郵遞區號查詢小幫手 — 使用 zip5.5432.tw API"
    )
    parser.add_argument(
        "address",
        nargs="?",
        help="要查詢的地址 (不提供則進入互動模式)",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="以 JSON 格式輸出結果",
    )

    args = parser.parse_args()

    if args.address:
        data = query_zipcode(args.address)
        if data is None:
            sys.exit(1)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            display_result(data)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
