#!/usr/bin/env bash
# ---------------------------------------------------------------
# run_all.sh — execute the full pipeline without Snakemake.
# Useful as a fallback for graders without snakemake installed.
# ---------------------------------------------------------------
set -euo pipefail

PROC=data/processed
ANA=results/analysis
FIG=results/figures
mkdir -p "$PROC" "$ANA" "$FIG" logs

START="2021-01-01"
END="2022-01-01"
YEAR="2021"
TICKERS=(CVS JNJ ABBV)

# Build the list of per-ticker stock CSV paths
STOCK_PATHS=()
for t in "${TICKERS[@]}"; do
    STOCK_PATHS+=("$PROC/stock_${t}.csv")
done

echo "[1/7] Loading raw COVID files..."
python scripts/01_load_covid.py \
    --input-folder csse_covid_19_daily_reports_us \
    --year "$YEAR" \
    --output "$PROC/covid_raw_combined.csv"

echo "[2/7] Cleaning COVID data..."
python scripts/02_clean_covid.py \
    --input "$PROC/covid_raw_combined.csv" \
    --output-state "$PROC/covid_state_daily.csv" \
    --output-us "$PROC/covid_us_daily.csv"

echo "[3/7] Fetching stock data..."
for t in "${TICKERS[@]}"; do
    python scripts/03_fetch_stocks.py \
        --ticker "$t" --start "$START" --end "$END" \
        --output "$PROC/stock_${t}.csv"
done

echo "[4/7] Integrating COVID + stocks..."
python scripts/04_integrate.py \
    --covid-us "$PROC/covid_us_daily.csv" \
    --stocks "${STOCK_PATHS[@]}" \
    --output "$PROC/integrated.csv"

echo "[5/7] Engineering features..."
python scripts/05_feature_engineering.py \
    --input "$PROC/integrated.csv" \
    --output "$PROC/features.csv" \
    --infection-window 7 --mortality-window 14 \
    --infection-weight 0.3 --mortality-weight 0.7 \
    --tickers "${TICKERS[@]}"

echo "[6/7] Running regressions..."
python scripts/06_analyze.py \
    --input "$PROC/features.csv" \
    --tickers "${TICKERS[@]}" \
    --output-dir "$ANA" \
    --output-csv "$ANA/regression_results.csv"

echo "[7/7] Generating figure..."
python scripts/07_visualize.py \
    --input "$PROC/features.csv" \
    --tickers "${TICKERS[@]}" \
    --output "$FIG/stocks_vs_cases.png"

echo "Done. Outputs in $PROC, $ANA, $FIG."
