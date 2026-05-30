#!/usr/bin/env python3
"""
End-to-end test: analyze QCOM via WallStreet AI.
Usage: python3 test_qcom.py
Requires: Flask server running at localhost:5000 + ANTHROPIC_API_KEY in env or .env
"""
import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "http://127.0.0.1:5000"
TICKER = "QCOM"

REQUIRED_FIELDS = [
    "company_name", "ticker", "market", "currency",
    "current_price", "overall_rating", "target_price_12m",
    "section1", "section2", "section3", "section4",
    "section5", "section6", "section7", "sandbox",
]
REQUIRED_SECTION2 = ["moat_score", "radar_scores", "competitors"]
REQUIRED_SECTION3 = ["health_verdict", "annual_data"]
REQUIRED_SECTION4 = ["valuation_verdict", "pe_band_data"]
VALID_RATINGS = {"BUY", "HOLD", "AVOID"}
VALID_HEALTH = {"STRONG", "WEAKENING", "CONCERNING"}
VALID_VALUATION = {"UNDERVALUED", "OVERVALUED", "FAIR"}


def check_server():
    try:
        r = requests.get(BASE + "/", timeout=5)
        r.raise_for_status()
        print("✅ Flask 伺服器連線正常")
    except Exception:
        print(f"❌ 無法連線到 {BASE}，請先執行：python3 app.py")
        sys.exit(1)


def get_api_key():
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        print("❌ 請設定 ANTHROPIC_API_KEY（環境變數或 .env 文件）")
        sys.exit(1)
    print(f"✅ API Key 已讀取（{key[:12]}...）")
    return key


def analyze_qcom(api_key):
    print(f"\n🔍 開始分析 {TICKER}，預計需要 30–90 秒...")
    t0 = time.time()
    try:
        resp = requests.post(
            BASE + "/api/analyze",
            json={"ticker": TICKER, "api_key": api_key},
            timeout=180,
        )
    except requests.Timeout:
        print("❌ 請求超時（180秒），請重試")
        sys.exit(1)

    elapsed = time.time() - t0
    print(f"   API 回傳，耗時 {elapsed:.1f} 秒")

    if resp.status_code != 200:
        err = resp.json().get("error", resp.text[:200])
        print(f"❌ API 回傳錯誤 (HTTP {resp.status_code}): {err}")
        sys.exit(1)

    body = resp.json()
    if not body.get("success"):
        print(f"❌ 分析失敗: {body.get('error', '未知錯誤')}")
        sys.exit(1)

    return body["data"]


def validate(data):
    errors = []

    # Required top-level fields
    for f in REQUIRED_FIELDS:
        if f not in data:
            errors.append(f"缺少頂層欄位: {f}")

    # Rating
    rating = data.get("overall_rating", "")
    if rating not in VALID_RATINGS:
        errors.append(f"overall_rating 無效: {rating!r}（應為 BUY/HOLD/AVOID）")

    # Ticker
    if data.get("ticker", "").upper() != TICKER:
        errors.append(f"ticker 不符: {data.get('ticker')!r}（應為 {TICKER}）")

    # Section 2
    s2 = data.get("section2", {})
    for f in REQUIRED_SECTION2:
        if f not in s2:
            errors.append(f"section2 缺少: {f}")
    score = s2.get("moat_score")
    if score is not None and not (1 <= float(score) <= 10):
        errors.append(f"section2.moat_score 超出範圍: {score}")

    # Section 3
    s3 = data.get("section3", {})
    for f in REQUIRED_SECTION3:
        if f not in s3:
            errors.append(f"section3 缺少: {f}")
    hv = s3.get("health_verdict", "")
    if hv not in VALID_HEALTH:
        errors.append(f"section3.health_verdict 無效: {hv!r}")

    # Section 4
    s4 = data.get("section4", {})
    for f in REQUIRED_SECTION4:
        if f not in s4:
            errors.append(f"section4 缺少: {f}")
    vv = s4.get("valuation_verdict", "")
    if vv not in VALID_VALUATION:
        errors.append(f"section4.valuation_verdict 無效: {vv!r}")

    # Section 7
    s7 = data.get("section7", {})
    r7 = s7.get("rating", "")
    if r7 not in VALID_RATINGS:
        errors.append(f"section7.rating 無效: {r7!r}")

    # Sandbox
    sb = data.get("sandbox", {})
    for sc in ["scenario1", "scenario2", "scenario3"]:
        if sc not in sb:
            errors.append(f"sandbox 缺少: {sc}")

    return errors


def print_summary(data):
    s2 = data.get("section2", {})
    s3 = data.get("section3", {})
    s4 = data.get("section4", {})
    s7 = data.get("section7", {})
    cur = data.get("current_price", 0)
    tgt = data.get("target_price_12m", 0)
    upside = ((tgt - cur) / cur * 100) if cur and tgt else 0
    curr_sym = "NT$" if data.get("currency") == "TWD" else "$"

    print("\n" + "=" * 55)
    print(f"  公司名稱   : {data.get('company_name', '--')}")
    print(f"  股票代碼   : {data.get('ticker')} ({data.get('market')})")
    print(f"  現價       : {curr_sym}{cur}")
    print(f"  12M目標價  : {curr_sym}{tgt}  ({upside:+.1f}%)")
    print(f"  分析師評等 : {data.get('overall_rating')}")
    print(f"  護城河評分 : {s2.get('moat_score')} / 10")
    print(f"  財務體質   : {s3.get('health_verdict')}")
    print(f"  估值狀態   : {s4.get('valuation_verdict')}")
    print(f"  核心金句   : 「{s7.get('key_sentence', '--')}」")
    print("=" * 55)


def main():
    print("=" * 55)
    print("  WallStreet AI — QCOM 端對端測試")
    print("=" * 55 + "\n")

    check_server()
    api_key = get_api_key()
    data = analyze_qcom(api_key)
    errors = validate(data)

    if errors:
        print("\n❌ JSON 結構驗證失敗，缺少以下欄位：")
        for e in errors:
            print(f"   • {e}")
        sys.exit(1)

    print_summary(data)
    rating = data.get("section7", {}).get("rating") or data.get("overall_rating")
    tgt = data.get("target_price_12m", "--")
    curr_sym = "NT$" if data.get("currency") == "TWD" else "$"
    print(f"\n✅ QCOM 分析成功！評等: {rating}，目標價: {curr_sym}{tgt}")


if __name__ == "__main__":
    main()
