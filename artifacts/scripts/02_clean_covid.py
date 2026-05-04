

import os
import argparse
import pandas as pd


KEEP_COLUMNS = ["Date", "Province_State", "Confirmed", "Deaths"]


def clean_covid(df: pd.DataFrame) -> pd.DataFrame:
    """Subset, parse dates, sort, and compute daily diffs per state."""
    missing = [c for c in KEEP_COLUMNS if c not in df.columns]
    if missing:
        raise KeyError(f"Expected columns missing from input: {missing}")

    out = df[KEEP_COLUMNS].copy()
    out["Date"] = pd.to_datetime(out["Date"])
    out = out.sort_values(["Province_State", "Date"]).reset_index(drop=True)

    out["New_Confirmed"] = out.groupby("Province_State")["Confirmed"].diff()
    out["New_Deaths"]    = out.groupby("Province_State")["Deaths"].diff()
    return out


def aggregate_national(df_state: pd.DataFrame) -> pd.DataFrame:
    """Sum daily New_Confirmed/New_Deaths across all states."""
    return (df_state
            .groupby("Date")[["New_Confirmed", "New_Deaths"]]
            .sum()
            .reset_index()
            .sort_values("Date")
            .reset_index(drop=True))


def main():
    parser = argparse.ArgumentParser(description="Clean and aggregate COVID data.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-state", required=True)
    parser.add_argument("--output-us", required=True)
    args = parser.parse_args()

    print(f"[02_clean_covid] Reading: {args.input}")
    df_raw = pd.read_csv(args.input)

    df_state = clean_covid(df_raw)
    df_us    = aggregate_national(df_state)

    os.makedirs(os.path.dirname(args.output_state), exist_ok=True)
    df_state.to_csv(args.output_state, index=False)
    df_us.to_csv(args.output_us, index=False)

    print(f"[02_clean_covid] State-level rows: {len(df_state)}")
    print(f"[02_clean_covid] National rows:    {len(df_us)}")
    print(f"[02_clean_covid] Wrote: {args.output_state}")
    print(f"[02_clean_covid] Wrote: {args.output_us}")


if __name__ == "__main__":
    main()
