"""Validate the raw NYC Green Taxi dataset before transformation."""

from pathlib import Path
import sys

import pyarrow.parquet as pq


DATA_PATH = Path("data/raw/green_tripdata_2025-01.parquet")

REQUIRED_COLUMNS = {
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "trip_distance",
    "fare_amount",
    "total_amount",
}


def validate_raw_dataset(path: Path) -> None:
    """Validate file existence, format, rows, and required columns."""

    print(f"Validating dataset: {path}")

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset does not exist: {path}\n"
            "Run the extraction script first."
        )

    file_size = path.stat().st_size

    if file_size == 0:
        raise ValueError("Dataset exists but is empty.")

    parquet_file = pq.ParquetFile(path)

    row_count = parquet_file.metadata.num_rows
    column_names = set(parquet_file.schema_arrow.names)

    if row_count == 0:
        raise ValueError("Parquet dataset contains zero rows.")

    missing_columns = REQUIRED_COLUMNS - column_names

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"Required columns are missing: {missing_text}")

    file_size_mb = file_size / (1024 * 1024)

    print(f"[PASS] File exists")
    print(f"[PASS] File size: {file_size_mb:.2f} MB")
    print(f"[PASS] Valid Parquet format")
    print(f"[PASS] Rows: {row_count:,}")
    print(f"[PASS] Columns: {len(column_names)}")
    print(f"[PASS] All required columns are present")


def main() -> None:
    """Run validation and return a useful terminal exit code."""

    try:
        validate_raw_dataset(DATA_PATH)
    except Exception as error:
        print(f"\nVALIDATION FAILED: {error}")
        sys.exit(1)

    print("\nRAW DATA VALIDATION PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()