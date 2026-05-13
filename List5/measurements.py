import csv
import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass, field

from time_series import TimeSeries
from series_validator import SeriesValidator


class Config:
    """Config class to centralize all constants and magic values related to file handling and parsing."""
    CSV_GLOB = "*.csv"
    ENCODING = "utf-8"
    DATE_FORMAT = "%d/%m/%y %H:%M"
    DEFAULT_UNIT = "ng/m3"
    UNKNOWN_VALUE = "unknown"
    HEADER_LINES_TO_SKIP_FOR_DATA = 6


@dataclass
class FileMetadata:
    """Structure to hold metadata about each CSV file and its loading state."""
    file_path: Path
    parameter: str
    frequency: str
    year: str
    stations: List[str]
    loaded_series: Dict[str, 'TimeSeries'] = field(default_factory=dict)

    @property
    def is_fully_loaded(self) -> bool:
        """Checks if all expected TimeSeries for the stations in this file have been loaded."""
        return len(self.loaded_series) == len(self.stations)


class Measurements:
    """Class for aggregating measurement data. Uses lazy loading."""

    def __init__(self, directory_path: str | Path):
        self.directory = Path(directory_path)
        self._files_index: List[FileMetadata] = []
        self._build_index()

    def __len__(self) -> int:
        return sum(len(metadata.stations) for metadata in self._files_index)

    def __contains__(self, parameter_name: str) -> bool:
        return any(metadata.parameter == parameter_name for metadata in self._files_index)

    def get_by_parameter(self, param_name: str) -> List['TimeSeries']:
        results = []
        for metadata in self._files_index:
            if metadata.parameter == param_name:
                self._load_data_if_needed(metadata)
                results.extend(metadata.loaded_series.values())
        return results

    def get_by_station(self, station_code: str) -> List['TimeSeries']:
        results = []
        for metadata in self._files_index:
            if station_code in metadata.stations:
                self._load_data_if_needed(metadata)
                if station_code in metadata.loaded_series:
                    results.append(metadata.loaded_series[station_code])
        return results

    def _build_index(self) -> None:
        """Function to build the index of files and their metadata without loading actual measurement data."""
        for file_path in self.directory.glob(Config.CSV_GLOB):
            metadata = self._process_single_file_metadata(file_path)
            self._files_index.append(metadata)

    def _process_single_file_metadata(self, file_path: Path) -> FileMetadata:
        """Function to process metadata for a single CSV file."""
        year, parameter, frequency = self._parse_filename(file_path)
        stations = self._extract_stations_from_header(file_path)
        return FileMetadata(file_path, parameter, frequency, year, stations)

    def _parse_filename(self, file_path: Path) -> Tuple[str, str, str]:
        """Function to parse the filename and extract year, parameter, and frequency. Assumes a specific naming convention."""
        parts = file_path.stem.split('_')
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        return Config.UNKNOWN_VALUE, file_path.stem, Config.UNKNOWN_VALUE

    def _extract_stations_from_header(self, file_path: Path) -> List[str]:
        """Function to extract station codes from the header of a CSV file."""
        with open(file_path, mode='r', encoding=Config.ENCODING) as f:
            reader = csv.reader(f)
            try:
                next(reader)
                header = next(reader)
                return header[1:]
            except StopIteration:
                return []


    def _load_data_if_needed(self, metadata: FileMetadata) -> None:
        """Function to decide whether to load a measurement file from disk."""
        if metadata.is_fully_loaded:
            return

        dates, values_dict = self._parse_measurements_file(metadata)
        self._instantiate_time_series(metadata, dates, values_dict)

    def _parse_measurements_file(self, metadata: FileMetadata) -> Tuple[List, Dict[str, list]]:
        """Function responsible for opening and reading the actual measurement rows."""
        dates = []
        values_dict = {st_code: [] for st_code in metadata.stations}

        with open(metadata.file_path, mode='r', encoding=Config.ENCODING) as f:
            reader = csv.reader(f)
            self._skip_header_lines(reader, Config.HEADER_LINES_TO_SKIP_FOR_DATA)

            for row in reader:
                if not row:
                    continue
                self._process_measurement_row(row, metadata.stations, dates, values_dict)

        return dates, values_dict

    def _skip_header_lines(self, reader, count: int) -> None:
        """Function to skip header lines in the CSV reader."""
        for _ in range(count):
            next(reader, None)

    def _process_measurement_row(self, row: List[str], stations: List[str],
                                 dates: List, values_dict: Dict[str, list]) -> None:
        """Function to process a single measurement row."""
        date_obj = self._parse_date(row[0])
        dates.append(date_obj)

        for i, st_code in enumerate(stations):
            val = self._parse_value(row, index=i+1)
            values_dict[st_code].append(val)

    def _parse_date(self, date_str: str):
        """Function to parse a date string."""
        try:
            return datetime.datetime.strptime(date_str, Config.DATE_FORMAT)
        except ValueError:
            return date_str

    def _parse_value(self, row: List[str], index: int) -> Optional[float]:
        """Function to parse a value from a CSV row."""
        val_str = row[index].strip() if index < len(row) else ""
        if not val_str:
            return None
        try:
            return float(val_str.replace(',', '.'))
        except ValueError:
            return None


    def _instantiate_time_series(self, metadata: FileMetadata, dates: List, values_dict: Dict[str, list]) -> None:
        """Function to instantiate TimeSeries objects from loaded data."""
        for st_code in metadata.stations:
            ts = TimeSeries(
                name=metadata.parameter,
                station_code=st_code,
                averaging_time=metadata.frequency,
                dates=dates.copy(),
                values=values_dict[st_code],
                unit=Config.DEFAULT_UNIT
            )
            metadata.loaded_series[st_code] = ts

    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False) -> dict[str, list[str]]:
        results: dict[str, list[str]] = {}

        for metadata in self._files_index:
            if preload:
                self._load_data_if_needed(metadata)

            for series in metadata.loaded_series.values():
                dict_key = f'{series.station_name}_{metadata.frequency}'
                if dict_key not in results:
                    results[dict_key] = []

                for validator in validators:
                    results[dict_key].extend(validator.analyze(series))

        return results

