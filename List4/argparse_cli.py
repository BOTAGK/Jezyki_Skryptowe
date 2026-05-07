import argparse
from get_measurement_files_by_key import group_measurement_files_by_key
from datetime import datetime
from pathlib import Path
from station_manager import StationManager
import random
import statistics
import sys
import logging

MEASUREMENTS_PATH = './data/measurements/'
STATIONS_PATH = './data/station/stacje.csv'

logger = logging.getLogger(__name__)

class StdoutFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= logging.WARNING

def setup_logging() -> None:
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(StdoutFilter())
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stdout_handler.setFormatter(formatter)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

def get_valid_measurement(dictionary: Path) -> tuple[set[str], set[str]]:
    grouped_measurements = group_measurement_files_by_key(dictionary)

    parameters: set[str] = set()
    frequencies: set[str] = set()
    for _, param, freq in grouped_measurements:
        parameters.add(param)
        frequencies.add(freq)

    return parameters, frequencies

def validate_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f'{value} nie jest poprawną datą'"")

def get_station_manager() -> StationManager:
    return StationManager(Path(__file__).parent.joinpath(STATIONS_PATH))

def print_random_station(parameter: str, frequency: str, start: datetime, end: datetime, valid_params: set, valid_freq: set):
    if parameter not in valid_params:
        logger.warning(f"Użytkownik podał mierzoną wielkość ({parameter}), która nie występuje na żadnej stacji.")
    if frequency not in valid_freq:
        logger.warning(f"Częstotliwość ({frequency}) nie jest wspierana w dostępnych plikach.")

    manager = get_station_manager()
    directory = Path(__file__).parent.joinpath(MEASUREMENTS_PATH)
    grouped = group_measurement_files_by_key(directory)

    valid_files = []
    for (rok, param, freq), paths in grouped.items():
        if param == parameter and freq == frequency:
            if start.year <= int(rok) <= end.year:
                valid_files.extend(paths)

    if not valid_files:
        logger.warning("Brak dostępnych plików pomiarowych dla podanego parametru i częstotliwości.")

    stations_with_measurements = set()
    for file_path in valid_files:
        manager.measurements_data.clear()
        manager.parse_measurement_file(file_path)
        for station_code, measurements in manager.measurements_data.items():
            for m in measurements:
                if start <= m.timestamp <= end:
                    stations_with_measurements.add(station_code)

    if not stations_with_measurements:
        logger.warning("Brak dostępnych pomiarów dla zadanych parametrów.")
        print("Brak stacji spełniających podane kryteria.")
        return

    random_station_code = random.choice(list(stations_with_measurements))
    station = manager.stations_data.get(random_station_code)
    if station:
        print(f"Nazwa: {station.name}, Adres: {station.address}, Kod: {station.code}")
    else:
        print(f"Stacja: {random_station_code} (Brak szczegółowych danych)")

def calculate_stats(parameter: str, frequency: str, start: datetime, end: datetime, station_id: str, valid_params: set, valid_freq: set):
    if parameter not in valid_params:
        logger.warning(f"Użytkownik podał mierzoną wielkość ({parameter}), która nie występuje na żadnej stacji.")
    if frequency not in valid_freq:
        logger.warning(f"Częstotliwość ({frequency}) nie jest wspierana w dostępnych plikach.")

    manager = get_station_manager()
    directory = Path(__file__).parent.joinpath(MEASUREMENTS_PATH)
    grouped = group_measurement_files_by_key(directory)

    valid_files = []
    for (rok, param, freq), paths in grouped.items():
        if param == parameter and freq == frequency:
            if start.year <= int(rok) <= end.year:
                valid_files.extend(paths)

    if not valid_files:
        logger.warning("Brak dostępnych plików pomiarowych dla podanego parametru i częstotliwości.")

    values = []
    for file_path in valid_files:
        manager.measurements_data.clear()
        manager.parse_measurement_file(file_path)
        if station_id in manager.measurements_data:
            for m in manager.measurements_data[station_id]:
                if start <= m.timestamp <= end:
                    values.append(m.value)

    if not values:
        logger.warning("Brak dostępnych pomiarów dla zadanych parametrów.")
        print("Brak danych pomiarowych dla podanej stacji w zadanym przedziale.")
        return

    avg = statistics.mean(values)
    std = statistics.pstdev(values) if len(values) > 1 else 0.0
    print(f"Średnia: {avg:.2f}")
    print(f"Odchylenie standardowe: {std:.2f}")

def calculate_worst_station(parameter: str, frequency: str, start: datetime, end: datetime, valid_params: set, valid_freq: set):
    """Finds and writes info about the station with the worst average value in the given time range."""
    
    worst_code = None
    worst_avg = float('-inf')

    manager = get_station_manager()
    directory = Path(__file__).parent.joinpath(MEASUREMENTS_PATH)
    grouped = group_measurement_files_by_key(directory)

    valid_files = []
    for (rok, param, freq), paths in grouped.items():
        if param == parameter and freq == frequency:
            if start.year <= int(rok) <= end.year:
                valid_files.extend(paths)

    if not valid_files:
        logger.warning("Brak dostępnych plików pomiarowych dla podanego parametru i częstotliwości.")

    for file_path in valid_files:
        manager.measurements_data.clear()
        manager.parse_measurement_file(file_path)

        for code, pomiary in manager.measurements_data.items():

            values = [p.value for p in pomiary if start <= p.timestamp <= end]
            if values:
                avg = statistics.mean(values)
                if avg > worst_avg:
                    worst_avg = avg
                    worst_code = code
                
    if worst_code is None:
        logger.warning("Brak pomiarów dla tych parametrów w danym czasie.")
        return
        
    stacja = manager.stations_data.get(worst_code)
    
    if stacja:
        logger.warning("\n--- NAJGORSZA STACJA ---")
        print(f"Nazwa: {stacja.name}")
        print(f"Adres: {stacja.city}, {stacja.address}")
        print(f"Kod:   {stacja.code}")
        print(f"Średnia wartość: {worst_avg:.4f}\n")


def run_cli():
    setup_logging()

    valid_params, valid_freq = get_valid_measurement(Path(__file__).parent.joinpath(MEASUREMENTS_PATH))

    parser = argparse.ArgumentParser(description="Zaktualizowany interfejs linii komend z podkomendami")
    parser.add_argument("parameter", help="Mierzona wielkość np. PM2.5, PM10, NO")
    parser.add_argument("frequency", help="Częstotliwość pomiaru np. 1g, 24g")
    parser.add_argument("start", type=validate_date, help="Początek przedziału czasowego w formacie rrrr-mm-dd")
    parser.add_argument("end", type=validate_date, help="Koniec przedziału czasowego w formacie rrrr-mm-dd")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("random", help="Wypisanie nazwy i adresu losowej stacji")

    stats_parser = subparsers.add_parser("stats", help="Obliczenie średniej i odchylenia standardowego")
    stats_parser.add_argument("station", help="Kod stacji pomiarowej")

    worst_parser = subparsers.add_parser("worst-station", help="Wyswietla stacje ktora ma największą średnią wartość zadanej wielkości w zadanym przedziale czasowym")
    stats_parser.add_argument("worst-station", help="Wyswietla najgorsza stacje")

    args = parser.parse_args()

    if args.start > args.end:
        print("Błąd: Początek zakresu dat jest większy od końca")
        return

    if args.command == "random":
        print_random_station(args.parameter, args.frequency, args.start, args.end, valid_params, valid_freq)
    elif args.command == "stats":
        calculate_stats(args.parameter, args.frequency, args.start, args.end, args.station, valid_params, valid_freq)
    elif args.command == "worst-station":
        calculate_worst_station(args.parameter, args.frequency, args.start, args.end, valid_params, valid_freq)    
    elif args.command is None:
        parser.print_help()

if __name__ == "__main__":
    run_cli()
