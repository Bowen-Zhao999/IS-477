

import os
import argparse
from functools import reduce
import pandas as pd


def assign_trading_day(d: pd.Timestamp, trading_dates: list) -> pd.Timestamp:
    """Return the first trading_date >= d, or NaT if none exists."""
    for td in trading_dates:
        if td >= d:
            return td
    return pd.NaT


def integrate(covid_us: pd.DataFrame, stock_dfs: dict) -> pd.DataFrame:
    """Roll COVID dates forward to next trading day, then inner-merge all stocks."""
    if not stock_dfs:
        raise ValueError("At least one stock dataframe is required.")

    # Reference trading calendar = first ticker's Date list
    first_ticker = next(iter(stock_dfs))
    trading_dates = (pd.to_datetime(stock_dfs[first_ticker]["Date"])
                     .sort_values()
                     .tolist())

    covid = covid_us.copy()
    covid["Date"] = pd.to_datetime(covid["Date"])
    covid["Trading_Day"] = covid["Date"].apply(
        lambda d: assign_trading_day(d, trading_dates)
    )

    covid_by_td = (covid
                   .groupby("Trading_Day")[["New_Confirmed", "New_Deaths"]]
                   .sum()
                   .reset_index()
                   .rename(columns={"Trading_Day": "Date"}))
    covid_by_td["Date"] = covid_by_td["Date"].dt.strftime("%Y-%m-%d")

    # Inner-join with every ticker's data on Date
    merged = reduce(
        lambda left, right: left.merge(right, on="Date", how="inner"),
        stock_dfs.values(),
        covid_by_td,
    )

    # Clip retroactive-correction negatives
    n_neg_conf = (merged["New_Confirmed"] < 0).sum()
    n_neg_dth  = (merged["New_Deaths"]    < 0).sum()
    print(f"[04_integrate] Negatives clipped — New_Confirmed: {n_neg_conf}, "
          f"New_Deaths: {n_neg_dth}")
    merged["New_Confirmed"] = merged["New_Confirmed"].clip(lower=0)
    merged["New_Deaths"]    = merged["New_Deaths"].clip(lower=0)

    return merged


def infer_ticker_from_columns(df: pd.DataFrame) -> str:
    """Recover the ticker symbol from a cleaned stock CSV's column names."""
    for col in df.columns:
        if col.endswith("_Close"):
            return col[:-len("_Close")]
    raise ValueError(f"Could not infer ticker from columns: {list(df.columns)}")


def main():
    parser = argparse.ArgumentParser(description="Integrate COVID and stock data.")
    parser.add_argument("--covid-us", required=True)
    parser.add_argument("--stocks", required=True, nargs="+",
                        help="Paths to cleaned per-ticker stock CSVs.")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    covid_us = pd.read_csv(args.covid_us)

    stock_dfs = {}
    for path in args.stocks:
        df = pd.read_csv(path)
        ticker = infer_ticker_from_columns(df)
        stock_dfs[ticker] = df
        print(f"[04_integrate] Loaded {ticker} ({len(df)} rows) from {path}")

    merged = integrate(covid_us, stock_dfs)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(f"[04_integrate] Final shape: {merged.shape}")
    print(f"[04_integrate] Wrote: {args.output}")


if __name__ == "__main__":
    main()
