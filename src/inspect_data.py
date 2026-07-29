"""Inspect raw NYC Green Taxi data before transformation."""

from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/green_tripdata_2025-01.parquet")


def inspect_dataset(path: Path) -> None:
    """Display basic information about a Parquet dataset."""

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Run the extraction script first."
        )

    dataframe = pd.read_parquet(path)

    print(f"Dataset: {path}")
    print(f"Rows: {len(dataframe):,}")
    print(f"Columns: {len(dataframe.columns)}")

    print("\nColumns and data types:")
    for column, data_type in dataframe.dtypes.items():
        print(f"- {column}: {data_type}")

    print("\nFirst 5 rows:")
    print(dataframe.head().to_string(index=False))

    print("\nMissing values:")
    missing_values = dataframe.isna().sum()
    missing_values = missing_values[missing_values > 0].sort_values(
        ascending=False
    )

    if missing_values.empty:
        print("No missing values found.")
    else:
        print(missing_values.to_string())


if __name__ == "__main__":
    inspect_dataset(DATA_PATH)