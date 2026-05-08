from station_manager import StationManager
import get_measurement_files_by_key
from pathlib import Path


def main() -> None:
    # test złej ścieżki
    # station_manager = StationManager(Path(__file__).parent.joinpath('./data/station/test.csv'))

    station_manager = StationManager(Path(__file__).parent.joinpath('./data/station/stacje.csv'))
    measurements = station_manager.parse_measurement_file(Path(__file__).parent.joinpath('./data/measurements/2023_As(PM10)_24g.csv'))
    print(get_measurement_files_by_key.group_measurement_files_by_key(Path(__file__).parent.joinpath('./data/measurements/')))

    # print(measurements)

if __name__ == "__main__":
    main()