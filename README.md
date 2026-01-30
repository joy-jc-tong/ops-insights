# Ops Insights

Ops Insights 是一個製造業設備營運分析的示範專案，  
模擬設備事件資料的產生，透過 Python 執行 ETL，將資料載入 SQLite 資料倉儲，並產出可供分析與 BI 使用的 KPI marts。

---

## 本專案模擬的情境（What this project simulates）

- 製造設備事件資料（Manufacturing equipment events）
  - 狀態包含：Run / Down / Idle
- 資料流程：
  - Raw events → ETL → KPI marts → SQL analysis / Power BI dashboard
- 常見營運指標（Operational KPIs）：
  - Daily downtime
  - Daily throughput (wafer out)
  - Downtime by tool type / site

---

## 如何執行（How to run）

一行指令即可產生資料並完成整個 pipeline：

```bash
py -m src.main --generate-data --run-etl
