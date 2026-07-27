"""Download raw NYC Green Taxi trip data."""

from pathlib import Path

import requests


DATA_URL = (
    "https://d37ci6vzurychx.cloudfront.net/"
    "trip-data/green_tripdata_2025-01.parquet"
)

OUTPUT_PATH = Path("data/raw/green_tripdata_2025-01.parquet")

CHUNK_SIZE = 1024 * 1024  # Download 1 MB at a time


def download_file(url: str, destination: Path) -> Path:
    """Download a file from a URL into the raw data directory."""

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        print(f"File already exists: {destination}")
        return destination

    temporary_path = destination.with_suffix(
        destination.suffix + ".part"
    )

    print(f"Downloading data from:\n{url}")

    try:
        with requests.get(
            url,
            stream=True,
            timeout=60,
        ) as response:
            response.raise_for_status()

            with temporary_path.open("wb") as file:
                for chunk in response.iter_content(
                    chunk_size=CHUNK_SIZE
                ):
                    if chunk:
                        file.write(chunk)

        temporary_path.replace(destination)

    except (requests.RequestException, OSError):
        temporary_path.unlink(missing_ok=True)
        raise

    size_mb = destination.stat().st_size / (1024 * 1024)

    print(f"Download complete: {destination}")
    print(f"File size: {size_mb:.2f} MB")

    return destination


if __name__ == "__main__":
    download_file(DATA_URL, OUTPUT_PATH)