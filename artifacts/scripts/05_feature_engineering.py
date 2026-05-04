

import os
import argparse
import pandas as pd


def build_features(
    df: pd.DataFrame,
    tickers: list,
    inf_window: int,
    mor_window: int,
    inf_weight: float,
    mor_weight: float,
) -> pd.DataFrame:
    """Add rolling, Z-score, momentum, severity, and per-ticker return columns."""
    out = df.copy()

    inf_rolling = out["New_Confirmed"].rolling(window=inf_window).mean()
    mor_rolling = out["New_Deaths"].rolling(window=mor_window).mean()

    out["Infection_Z"] = (inf_rolling - inf_rolling.mean()) / inf_rolling.std()
    out["Mortality_Z"] = (mor_rolling - mor_rolling.mean()) / mor_rolling.std()

    out["Infection_Momentum"] = inf_rolling.pct_change(inf_window)
    out["Mortality_Momentum"] = mor_rolling.pct_change(mor_window)

    out["Severity_Index"] = (
        inf_weight * out["Infection_Z"] + mor_weight * out["Mortality_Z"]
    )

    for t in tickers:
        close_col  = f"{t}_Close"
        return_col = f"{t}_Return"
        if close_col not in out.columns:
            raise KeyError(f"Missing expected column {close_col} for ticker {t}.")
        out[return_col] = out[close_col].pct_change()

    return out


def main():
    parser = argparse.ArgumentParser(description="Build engineered features.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--infection-window", type=int, default=7)
    parser.add_argument("--mortality-window", type=int, default=14)
    parser.add_argument("--infection-weight", type=float, default=0.3)
    parser.add_argument("--mortality-weight", type=float, default=0.7)
    parser.add_argument("--tickers", required=True, nargs="+")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    out = build_features(
        df,
        tickers=args.tickers,
        inf_window=args.infection_window,
        mor_window=args.mortality_window,
        inf_weight=args.infection_weight,
        mor_weight=args.mortality_weight,
    )

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    out.to_csv(args.output, index=False)
    print(f"[05_feature_engineering] Output shape: {out.shape}")
    print(f"[05_feature_engineering] Added cols: "
          f"Infection_Z, Mortality_Z, Infection_Momentum, Mortality_Momentum, "
          f"Severity_Index, {', '.join(t + '_Return' for t in args.tickers)}")
    print(f"[05_feature_engineering] Wrote: {args.output}")


if __name__ == "__main__":
    main()
