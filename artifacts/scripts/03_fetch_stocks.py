

import os
import argparse
import pandas as pd
import yfinance as yf


def fetch_ticker(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download Close + Volume for a ticker, prefix columns with ticker name."""
    print(f"[03_fetch_stocks] Downloading {ticker} ({start} to {end})...")
    raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if raw.empty:
        raise RuntimeError(f"No data returned for ticker {ticker}.")

    # Flatten yfinance MultiIndex columns if present
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = [c[0] for c in raw.columns]

    raw = raw[["Close", "Volume"]].copy()
    raw.columns = [f"{ticker}_Close", f"{ticker}_Volume"]
    raw.reset_index(inplace=True)
    raw["Date"] = raw["Date"].dt.strftime("%Y-%m-%d")
    raw = raw[["Date", f"{ticker}_Close", f"{ticker}_Volume"]]

    print(f"[03_fetch_stocks] {ticker}: {len(raw)} trading-day rows")
    return raw


def main():
    parser = argparse.ArgumentParser(description="Fetch stock data via yfinance.")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = fetch_ticker(args.ticker, args.start, args.end)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"[03_fetch_stocks] Wrote: {args.output}")


if __name__ == "__main__":
    main()
