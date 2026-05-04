

import os
import argparse
import pandas as pd


def load_covid_files(folder_path: str, year_filter: str) -> pd.DataFrame:
    """Concatenate every CSV in folder_path whose filename contains year_filter."""
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"COVID data folder not found: {folder_path}")

    files = [f for f in os.listdir(folder_path)
             if year_filter in f and f.endswith(".csv")]
    if not files:
        raise ValueError(
            f"No CSV files matching year '{year_filter}' found in {folder_path}"
        )

    print(f"[01_load_covid] Found {len(files)} CSV files for year {year_filter}.")

    df_list = []
    for fname in files:
        df_list.append(pd.read_csv(os.path.join(folder_path, fname)))

    combined = pd.concat(df_list, ignore_index=True)
    print(f"[01_load_covid] Combined dataframe shape: {combined.shape}")
    return combined


def main():
    parser = argparse.ArgumentParser(description="Load and combine raw COVID CSVs.")
    parser.add_argument("--input-folder", required=True)
    parser.add_argument("--year", default="2021")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = load_covid_files(args.input_folder, args.year)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"[01_load_covid] Wrote: {args.output}")


if __name__ == "__main__":
    main()
