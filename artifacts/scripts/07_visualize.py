

import os
import argparse
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DEFAULT_COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c",
                  "#d62728", "#9467bd", "#8c564b"]


def plot_stocks_vs_cases(df: pd.DataFrame, tickers: list, output_path: str):
    """Multi-panel figure: per-ticker close price overlaid with new cases."""
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    n = len(tickers)
    fig, axes = plt.subplots(n, 1, figsize=(12, 3.5 * n), sharex=True)
    if n == 1:
        axes = [axes]

    colors = (DEFAULT_COLORS * ((n // len(DEFAULT_COLORS)) + 1))[:n]

    for ax, ticker, color in zip(axes, tickers, colors):
        close_col = f"{ticker}_Close"
        if close_col not in df.columns:
            raise KeyError(f"Missing column {close_col} in input data.")

        ax.plot(df["Date"], df[close_col], color=color, label=f"{ticker} Close")
        ax.set_ylabel(f"{ticker} Close Price ($)", color=color)
        ax.tick_params(axis="y", labelcolor=color)
        ax.set_title(f"{ticker} Stock Price vs. COVID-19 New Cases (2021)")

        ax2 = ax.twinx()
        ax2.fill_between(df["Date"], df["New_Confirmed"],
                         color="gray", alpha=0.2, label="New Confirmed")
        ax2.set_ylabel("New Confirmed Cases", color="gray")
        ax2.tick_params(axis="y", labelcolor="gray")

    axes[-1].set_xlabel("Date")
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"[07_visualize] Wrote: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot stock price vs COVID cases.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--tickers", required=True, nargs="+")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    plot_stocks_vs_cases(df, args.tickers, args.output)


if __name__ == "__main__":
    main()
