import pickle
from pathlib import Path
from typing import Any, Dict


def save_pickle(
    directory: Path,
    data: Any,
    filename: str | None = None
) -> None:
    """
    Save data as a pickle file.

    - If filename is provided, saves to that file.
    - If filename is None, raises an error (explicit is better than implicit).
    """
    directory.mkdir(parents=True, exist_ok=True)

    if filename is None:
        raise ValueError("filename must be provided when saving data")

    file_path = directory / filename

    with open(file_path, "wb") as f:
        pickle.dump(data, f)


def load_pickle(
    directory: Path,
    filename: str | None = None
) -> Any:
    """
    Load pickled data.

    - If filename is provided, loads that file.
    - If filename is None, loads *all* pickle files in the directory
      and returns a dict: {filename: data}
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if filename:
        file_path = directory / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            return pickle.load(f)

    # Load everything in directory
    all_data: Dict[str, Any] = {}

    for file_path in directory.glob("*.pkl"):
        with open(file_path, "rb") as f:
            all_data[file_path.name] = pickle.load(f)

    if not all_data:
        raise FileNotFoundError(f"No pickle files found in {directory}")

    return all_data
