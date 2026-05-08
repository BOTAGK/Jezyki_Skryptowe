import re
from pathlib import Path
from typing import Dict, Tuple


def group_measurement_files_by_key(path: Path) -> Dict[Tuple[str, str, str], list[Path]]:
    result: Dict[Tuple[str, str, str], list[Path]] = {}

    pattern = re.compile(r"^(\d{4})_(.+?)_(\d+[a-zA-Z]+)(?:_\d+)?\.csv$")

    for file_path in path.iterdir():
        if not file_path.is_file():
            continue

        match = pattern.fullmatch(file_path.name)
        if match:
            rok, measurement, frequency = match.groups()
            key = (rok, measurement, frequency)
            result.setdefault(key, []).append(file_path)

    return result

if __name__ == '__main__':
    print(group_measurement_files_by_key(Path(__file__).parent.joinpath('data/measurements')))
