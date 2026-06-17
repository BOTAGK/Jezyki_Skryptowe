import csv
from enum import Enum
from pathlib import Path
from typing import Dict, List

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
    
class Station:
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

    def __init__(self, row: Dict[str, str]) -> None:
        self._parse_data(row)

    def _parse_data(self, row: Dict[str, str]) -> None:
        self.id_number = row.get(StationColumn.ID, '')
        self.code = row.get(StationColumn.CODE, '')
        self.international_code = row.get(StationColumn.INT_CODE, '')
        self.name = row.get(StationColumn.NAME, '')
        self.old_code = row.get(StationColumn.OLD_CODE, '')
        self.start_date = row.get(StationColumn.START_DATE, '')
        self.end_date = row.get(StationColumn.END_DATE, '')
        self.station_type = row.get(StationColumn.STATION_TYPE, '')
        self.area_type = row.get(StationColumn.AREA_TYPE, '')
        self.station_kind = row.get(StationColumn.STATION_KIND, '')
        self.voivodeship = row.get(StationColumn.VOIVODESHIP, '')
        self.city = row.get(StationColumn.CITY, '')
        self.address = row.get(StationColumn.ADDRESS, '')

        lat_str: str = row.get(StationColumn.WGS84_N, '').replace(',', '.')
        lon_str: str = row.get(StationColumn.WGS84_E, '').replace(',', '.')
        self.lat = float(lat_str) if lat_str else 0.0
        self.lon = float(lon_str) if lon_str else 0.0

    @classmethod 
    def from_csv_by_code(cls, path: Path, target_code: str) -> 'Station':
        with open(path, 'r', encoding='utf-8') as file:
            reader: csv.DictReader = csv.DictReader(file)
            for row in reader:
                if row.get(StationColumn.CODE) == target_code:
                    return cls(row)
        raise ValueError(f"W pliku nie znaleziono stacji o kodzie: {target_code}")

    @classmethod
    def load_all_from_csv(cls, path: Path) -> List['Station']:
        stations: List['Station'] = []
        with open(path, 'r', encoding='utf-8') as file:
            reader: csv.DictReader = csv.DictReader(file)
            for row in reader:
                stations.append(cls(row))
        return stations                   

    def __str__(self) -> str:
        return f"Station {self.name} ({self.code}) in {self.city}, {self.voivodeship}"

    def __repr__(self) -> str:
        return f"Station(code='{self.code}', name='{self.name}', city='{self.city}', voivodeship='{self.voivodeship}')"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Station):
            return self.code == other.code
        return False