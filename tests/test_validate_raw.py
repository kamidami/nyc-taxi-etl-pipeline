"""Tests for raw NYC taxi dataset validation."""

from datetime import datetime

import pandas as pd
import pytest

from src.validate_raw import validate_raw_dataset


def test_missing_dataset_raises_error(tmp_path):
    """Validation should fail when the dataset does not exist."""

    missing_file = tmp_path / "missing.parquet"

    with pytest.raises(FileNotFoundError, match="Dataset not found"):
        validate_raw_dataset(missing_file)


def test_valid_dataset_passes(tmp_path):
    """Validation should accept a valid Parquet dataset."""

    valid_file = tmp_path / "valid.parquet"

    dataframe = pd.DataFrame(
        {
            "lpep_pickup_datetime": [
                datetime(2025, 1, 1, 10, 0)
            ],
            "lpep_dropoff_datetime": [
                datetime(2025, 1, 1, 10, 15)
            ],
            "PULocationID": [1],
            "DOLocationID": [2],
            "trip_distance": [3.5],
            "fare_amount": [15.0],
            "total_amount": [18.5],
        }
    )

    dataframe.to_parquet(valid_file, index=False)

    validate_raw_dataset(valid_file)