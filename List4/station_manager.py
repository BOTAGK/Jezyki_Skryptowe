import csv
from enum import Enum
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple

class StationColumn(str, Enum):
    REGION = 'Województwo'
    CITY = 'Miejscowość'
    ADDRESS = 'Adres'
class StationManager:

    metadata_path: Path
    stations_data: List[Dict[str, str]]
    measurements_data: Dict[str, List[Dict[str, str]]]
    address_regex: re.Pattern

    def __init__(self, metadata_path: Path):
        self.metadata_path = metadata_path
        self.stations_data = self._parse_metadata()
        self.measurements_data = {}

        self._setup_patterns()

    def _setup_patterns(self):
        self.address_regex = re.compile(r"""
            ^ # Start of the string
            (.*?) #Non-greedy match for the street name
            (?: # Optional non-capturing group for the house number
                \s+ # One or more whitespace characters before the house number
                (
                    \d+ # Match the house number (one or more digits)
                    [a-zA-Z\d/]* # Optional match for any letters, digits, or slashes following the house number
                )
            )? # Optional group ends here
            $ # End of the string
        """, re.VERBOSE)    

    def _parse_metadata(self) -> List[Dict[str, str]]:
        """Parses the stations.csv file """
        parsed_data = []

        with open(self.metdata_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                parsed_data.append(row)
        return parsed_data
    
    def parse_measurement_file(self, measurement_path: Path) -> List[Dict[str, str]]:
        """Parses a measurement file and returns the data as a list of dictionaries."""
        
        parsed_measurements = []

        with open(measurement_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                parsed_measurements.append(row)
        return parsed_measurements
    
    def store_measurements(self, station_id: str, measurements: List[Dict[str, str]]) -> None:
        """Stores the measurements for a given station ID."""
        self.measurements_data[station_id] = measurements


        
    def get_addresses(self, path: Optional[Path] = None, city: str = "") -> List[Tuple[str, str, str, Optional[str]]]:
        """Returns a list of 4-tuples containing the address information for the specified city."""
        addresses = []

        target_path = path if path else self.metadata_path

        with open(target_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader: 
                if row.get(StationColumn.CITY) == city:
                    province = row.get(StationColumn.REGION, '')
                    station_city = row.get(StationColumn.CITY, '')
                    address_raw = row.get(StationColumn.ADDRESS, '')

                    street, house_number = self._extract_street_and_number(address_raw)
                    addresses.append((province, station_city, street, house_number))
       
        return addresses    

    def _extract_street_and_number(self, address: str) -> Tuple[str, Optional[str]]:
        """Extracts the street name and house number from an address string."""

        if not address:
            return '', None
        
        match = self.address_regex.match(address)
        if match:
            return match.group(1).strip(), match.group(2)
        return address.strip(), None