#!/usr/bin/env node
/**
 * test_image_export.js
 * Automated verification for the image export fix.
 * Tests: variable name fix, CDN reachability, code structure.
 * Run: node test_image_export.js
 */

const fs = require('fs');
const https = require('https');
const http = require('http');
const path = require('path');

const HTML_PATH = path.join(__dirname, 'templates', 'index.html');
const CDN_URL = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
const FLASK_URL = 'http://127.0.0.1:5000';

let passed = 0, failed = 0;

function check(name, condition, detail = '') {
  if (condition) {
    console.log(`  ✅ ${name}`);
    passed++;
  } else {
    console.log(`  ❌ ${name}${detail ? ': ' + detail : ''}`);
    failed++;
  }
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    lib.get(url, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    }).on('error', reject);
  });
}

async function main() {
  console.log('='.repeat(55));
  console.log('  WallStreet AI — 圖片匯出修復驗證');
  console.log('='.repeat(55) + '\n');

  // === 1. 讀取 HTML 原始碼 ===
  console.log('【1】原始碼靜態檢查');
  let html;
  try {
    html = fs.readFileSync(HTML_PATH, 'utf8');
  } catch (e) {
    console.log(`  ❌ 無法讀取 ${HTML_PATH}`);
    process.exit(1);
  }

  // 1.1 確認 currentAnalysis 已移除
  check('不含 currentAnalysis（舊錯誤變數）',
    !html.includes('currentAnalysis'),
    '仍含 currentAnalysis，請修復');

  // 1.2 確認 currentData 正確使用
  check('exportReportAsImage 使用 currentData',
    html.includes('currentData && currentData.ticker'));

  // 1.3 確認 html2canvas CDN 存在
  check('html2canvas CDN script 標籤存在',
    html.includes('html2canvas'));

  // 1.4 確認 CDN 在 inline script 之前
  const cdnPos = html.indexOf('html2canvas.min.js"></script>');
  const inlinePos = html.indexOf('<script>');
  check('CDN 標籤在 inline script 之前（確保載入順序）',
    cdnPos !== -1 && cdnPos < inlinePos,
    `CDN at ${cdnPos}, inline script at ${inlinePos}`);

  // 1.5 確認 allowTaint: true 存在
  check('html2canvas 使用 allowTaint: true',
    html.includes('allowTaint: true'));

  // 1.6 確認 scale 為 1.5（不超過瀏覽器 canvas 限制）
  check('html2canvas scale <= 1.5',
    html.includes('scale: 1.5') || html.includes('scale: 1,') || html.includes('scale: 1 '));

  // 1.7 確認 try/catch/finally 結構完整
  check('exportReportAsImage 有 finally 恢復按鈕',
    html.includes('btn.disabled = false'));

  console.log('');

  // === 2. CDN 連線檢查 ===
  console.log('【2】CDN 連線檢查');
  try {
    const res = await fetchText(CDN_URL);
    check(`html2canvas CDN 可存取 (HTTP ${res.status})`, res.status === 200);
    check('CDN 回傳 JS 內容', res.body.length > 1000 && res.body.includes('html2canvas'));
  } catch (e) {
    check('html2canvas CDN 連線', false, e.message);
  }

  console.log('');

  // === 3. Flask 伺服器檢查 ===
  console.log('【3】Flask 伺服器檢查');
  try {
    const res = await fetchText(FLASK_URL);
    check('Flask 伺服器回應 200', res.status === 200);
    check('頁面含 btn-export-img', res.body.includes('btn-export-img'));
    check('頁面含 exportReportAsImage', res.body.includes('exportReportAsImage'));
    check('頁面含 html2canvas CDN', res.body.includes('html2canvas'));
    check('頁面不含 currentAnalysis', !res.body.includes('currentAnalysis'));
  } catch (e) {
    check('Flask 伺服器連線', false, e.message + '（請先執行 python3 app.py）');
  }

  console.log('');

  // === 結果 ===
  console.log('='.repeat(55));
  console.log(`  自動化測試結果：${passed} 通過 / ${failed} 失敗`);
  console.log('='.repeat(55));

  if (failed === 0) {
    console.log('\n✅ 所有自動化檢查通過！');
    console.log('\n📋 請在瀏覽器完成以下手動驗證：');
    console.log('   1. 開啟 http://127.0.0.1:5000，輸入 QCOM 完成分析');
    console.log('   2. 點擊 Navbar「📷 下載圖片」');
    console.log('   3. 確認按鈕顯示「⏳ 生成中...」');
    console.log('   4. 確認瀏覽器下載 QCOM_YYYYMMDD.png');
    console.log('   5. 開啟 PNG，確認圖表與內容完整');
  } else {
    console.log('\n❌ 有檢查項目失敗，請修復後重試。');
    process.exit(1);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
