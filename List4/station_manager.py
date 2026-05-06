import csv
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple



class StationColumn(str, Enum):
    ID = 'Nr'
    CODE = 'Kod stacji'
    INT_CODE = 'Kod międzynarodowy'
    NAME = 'Nazwa stacji'
    OLD_CODE = 'Stary Kod stacji \n(o ile inny od aktualnego)'
    START_DATE = 'Data uruchomienia'
    END_DATE = 'Data zamknięcia'
    STATION_TYPE = 'Typ stacji'
    AREA_TYPE = 'Typ obszaru'
    STATION_KIND = 'Rodzaj stacji'
    VOIVODESHIP = 'Województwo'
    CITY = 'Miejscowość'
    ADDRESS = 'Adres'
    WGS84_N = 'WGS84 φ N'
    WGS84_E = 'WGS84 λ E'

@dataclass
class Station:
    """Complete data class for station information."""
    id_number: str
    code: str
    international_code: str
    name: str
    old_code: str
    start_date: str
    end_date: str
    station_type: str
    area_type: str
    station_kind: str
    voivodeship: str
    city: str
    address: str
    lat: float
    lon: float

@dataclass
class Measurement:
    timestamp: datetime
    station_code: str
    value: float
    parameter: str
    unit: str
class StationManager:

    metadata_path: Path
    stations_data: Dict[str, Station]
    measurements_data: Dict[str, List[Measurement]]
    

    def __init__(self, metadata_path: Path):
        self.metadata_path = metadata_path
        self.stations_data = self._parse_metadata()
        self.measurements_data = {}

        self._setup_patterns()

    def _setup_patterns(self):
        self.address_regex = re.compile(r'^(.*?)(?:\s+(\d+[a-zA-Z\d/-]*))?$')    
        self.data_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        self.coords_latitude_regex = re.compile(r'^-?(?:[0-8]?\d(?:\.\d{6})|90(?:\.0{6}))$')
        self.coords_longitude_regex = re.compile(r'^-?(?:(?:1[0-7]\d|[1-9]?\d)(?:\.\d{6})|180(?:\.0{6}))$')
        self.two_part_name_regex = re.compile(r'^.+?\s+-\s+.+$')
        self.mob_code_regex = re.compile(r'^.*MOB$')
        self.three_part_name_regex = re.compile(r'^.+?\s+-\s+.+?\s+-\s+.+$')
        self.comma_street_regex = re.compile(r'^.+?,\s*(?:ul\.|al\.)\s+.+$')

    def _parse_metadata(self) -> Dict[str, Station]:
        """Parses the stations.csv file """
        station_dict = {}

        with open(self.metadata_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            for row in reader:

                code = row.get(StationColumn.CODE, '').strip()
                if not code:
                    continue
                
                lat_str = row.get(StationColumn.WGS84_N, '').strip().replace(',', '.')
                lon_str = row.get(StationColumn.WGS84_E, '').strip().replace(',', '.')

                station_dict[code] = Station(
                    id_number=row.get(StationColumn.ID, '').strip(),
                    code=code,
                    international_code=row.get(StationColumn.INT_CODE, '').strip(),
                    name=row.get(StationColumn.NAME, '').strip(),
                    old_code=row.get(StationColumn.OLD_CODE, '').strip(),
                    start_date=row.get(StationColumn.START_DATE, '').strip(),
                    end_date=row.get(StationColumn.END_DATE, '').strip(),
                    station_type=row.get(StationColumn.STATION_TYPE, '').strip(),
                    area_type=row.get(StationColumn.AREA_TYPE, '').strip(),
                    station_kind=row.get(StationColumn.STATION_KIND, '').strip(),
                    voivodeship=row.get(StationColumn.VOIVODESHIP, '').strip(),
                    city=row.get(StationColumn.CITY, '').strip(),
                    address=row.get(StationColumn.ADDRESS, '').strip(),
                    lat=float(lat_str) if lat_str else 0.0,
                    lon=float(lon_str) if lon_str else 0.0
                )
        return station_dict

    def parse_measurement_file(self, measurement_path: Path) -> Dict[str, List[Measurement]]:
        """Główny orkiestrator: Otwiera plik i deleguje parsowanie do metod pomocniczych."""
        with open(measurement_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            
            metadata = self._extract_headers_and_mapping(reader)
            if not metadata:
                return self.measurements_data   
                
            parameter, unit, column_map = metadata

            self._process_data_rows(reader, column_map, parameter, unit)
            return self.measurements_data

    def _extract_headers_and_mapping(self, reader) -> Optional[Tuple[str, str, Dict[int, str]]]:
        
        try:
            row_nr = next(reader)
            row_codes = next(reader)
            row_parameter = next(reader)
            row_time = next(reader)
            row_unit = next(reader)
            row_station_ids = next(reader)
        except StopIteration:
            return None
        
        parameter = row_parameter[1].strip() if len(row_parameter) > 1 else ""
        unit = row_unit[1].strip() if len(row_unit) > 1 else ""

        column_map = {}
        for i in range(1, len(row_codes)):
            code = row_codes[i].strip()
            if code:
                column_map[i] = code
                if code not in self.measurements_data:
                    self.measurements_data[code] = []
                    
        return parameter, unit, column_map

    def _process_data_rows(self, reader, column_map: Dict[int, str], parameter: str, unit: str) -> None:
        
        for row in reader:
            if not row or not row[0].strip():
                continue
            
            timestamp_dt = self._parse_measurement_datetime(row[0].strip())
            if not timestamp_dt:
                continue 

            for col_idx, station_code in column_map.items():
                if col_idx < len(row):
                    val_str = row[col_idx].strip()
                    if val_str:
                        try:
                            val_float = float(val_str.replace(',', '.'))
                            
                            measurement = Measurement(
                                timestamp=timestamp_dt,
                                station_code=station_code,
                                value=val_float,
                                parameter=parameter,
                                unit=unit
                            )
                            self.measurements_data[station_code].append(measurement)
                        except ValueError:
                            pass

    def _parse_measurement_datetime(self, timestamp_str: str) -> Optional[datetime]:
        
        try:
            if '/' in timestamp_str:
                try:
                    return datetime.strptime(timestamp_str, "%d/%m/%y %H:%M")
                except ValueError:
                    return datetime.strptime(timestamp_str, "%m/%d/%y %H:%M")
            else:
                return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    def store_measurements(self, station_id: str, measurements: List[Dict[str, str]]) -> None:
        """Stores the measurements for a given station ID."""
        self.measurements_data[station_id] = measurements

    def _extract_street_and_number(self, address: str) -> Tuple[str, Optional[str]]:
        """Extracts the street name and house number from an address string."""

        if not address:
            return '', None
        
        match = self.address_regex.match(address)
        if match:
            return match.group(1).strip(), match.group(2)
        return address.strip(), None
    
        
    def get_addresses(self, path: Optional[Path] = None, city: str = "") -> List[Tuple[str, str, str, Optional[str]]]:
        """Returns a list of 4-tuples containing the address information for the specified city."""
        addresses = []

        target_path = path if path else self.metadata_path

        with open(target_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader: 
                if row.get(StationColumn.CITY) == city:
                    voivodeship = row.get(StationColumn.VOIVODESHIP, '')
                    station_city = row.get(StationColumn.CITY, '')
                    address_raw = row.get(StationColumn.ADDRESS, '')

                    street, house_number = self._extract_street_and_number(address_raw)
                    addresses.append((voivodeship, station_city, street, house_number))
       
        return addresses    

    def get_all_dates(self) -> List[str]:
        """Returns a list of all start and end dates from the stations metadata."""
        dates = []
        for station in self.stations_data.values():
            
            for date_val in [station.start_date, station.end_date]:
                if self.data_regex.match(date_val):
                    dates.append(date_val)

        return dates

    def get_all_coordinates(self) -> List[Tuple[float, float]]:
        """Returns a list of all valid coordinates (latitude, longitude) from the stations metadata."""
        coords = []
        for station in self.stations_data.values():
            lat_match = self.coords_latitude_regex.match(str(station.lat))
            lon_match = self.coords_longitude_regex.match(str(station.lon))
            if lat_match and lon_match:
                coords.append((station.lat, station.lon))
        return coords
    
    def find_two_part_names(self) -> List[str]:
        """Returns a list of station names that consist of exactly two parts separated by ' - '."""
        two_part_names = []
        for station in self.stations_data.values():
            if self.two_part_name_regex.match(station.name):
                two_part_names.append(station.name)
        return two_part_names
    
    def find_three_part_names(self) -> List[str]:
        """Returns a list of station names that consist of exactly three parts separated by ' - '."""
        three_part_names = []
        for station in self.stations_data.values():
            if self.three_part_name_regex.match(station.name):
                three_part_names.append(station.name)
        return three_part_names
    
    def get_normalized_names(self) -> List[str]:
        """Returns a list of station names normalized by removing Polish diacritics."""

        polish_chars = str.maketrans(
            "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ",
            "acelnoszzACELNOSZZ"
        )
        normalized= []

        for station in self.stations_data.values():
            name = station.name.translate(polish_chars)
            name = name.replace(' ', '_')
            normalized.append(name)
        return normalized
    
    def verify_mob_stations(self) -> bool:
        """verifies that all station codes ending with 'MOB' are correctly identified."""
        for station in self.stations_data.values():
            if self.mob_code_regex.match(station.code):
                if station.station_kind.lower() != 'mobilna':
                    return False
        return True
    
    def find_comma_street_addresses(self) -> List[str]:
        """Returns a list of station addresses that contain a comma followed by 'ul.' or 'al.'."""
        comma_addresses = []
        for station in self.stations_data.values():
            if self.comma_street_regex.match(station.address):
                comma_addresses.append(station.address)
        return comma_addresses