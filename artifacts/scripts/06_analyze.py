

import os
import argparse
import pandas as pd
import statsmodels.api as sm


FEATURES = ["Severity_Index", "Infection_Momentum", "Mortality_Momentum"]


def run_ols(df: pd.DataFrame, target_col: str):
    """Fit an OLS model: target_col ~ FEATURES (with intercept)."""
    reg_df = df[FEATURES + [target_col]].dropna()
    X = sm.add_constant(reg_df[FEATURES])
    y = reg_df[target_col]
    return sm.OLS(y, X).fit(), len(reg_df)


def main():
    parser = argparse.ArgumentParser(description="OLS regressions per ticker.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--tickers", required=True, nargs="+")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--output-csv", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)

    df = pd.read_csv(args.input)

    summary_rows = []
    for t in args.tickers:
        target = f"{t}_Return"
        if target not in df.columns:
            raise KeyError(f"Missing return column: {target}")

        model, n_obs = run_ols(df, target)

        # Save full statsmodels summary as text
        txt_path = os.path.join(args.output_dir, f"ols_{t}.txt")
        with open(txt_path, "w") as f:
            f.write(f"OLS regression: {target} ~ {' + '.join(FEATURES)}\n")
            f.write(f"Observations used: {n_obs}\n\n")
            f.write(str(model.summary()))
        print(f"[06_analyze] Wrote: {txt_path}")

        # Collect tabular results
        for feat in ["const"] + FEATURES:
            summary_rows.append({
                "Ticker":      t,
                "Variable":    feat,
                "Coefficient": model.params[feat],
                "StdError":    model.bse[feat],
                "t":           model.tvalues[feat],
                "p_value":     model.pvalues[feat],
                "R_squared":   model.rsquared,
                "Adj_R_squared": model.rsquared_adj,
                "N_obs":       n_obs,
            })

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(args.output_csv, index=False)
    print(f"[06_analyze] Combined results: {args.output_csv}")


if __name__ == "__main__":
    main()
