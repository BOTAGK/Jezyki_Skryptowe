from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, cast

from measurements import Measurements
from series_validator import OutlierDetector, SeriesValidator, ThresholdDetector, ZeroSpikeDetector
from simple_reporter import SimpleReporter
from station import Station
from time_series import TimeSeries

#cd List8
#python.exe -m pip install mypy
#python -m mypy

def build_example_series() -> TimeSeries:
    dates: List[datetime] = [
        datetime(2026, 5, 1, 0, 0),
        datetime(2026, 5, 1, 1, 0),
        datetime(2026, 5, 1, 2, 0),
        datetime(2026, 5, 2, 0, 0),
        datetime(2026, 5, 2, 1, 0),
        datetime(2026, 5, 2, 2, 0),
    ]
    values: List[Optional[float]] = [10.0, 0.0, 0.0, 0.0, 12.0, 50.0]

    return TimeSeries(
        name="PM10",
        station_code="TEST_01",
        averaging_time="1g",
        dates=dates,
        values=values,
        unit="ng/m3",
    )


def check_time_series(series: TimeSeries) -> None:
    first_item: tuple[datetime, Optional[float]] = cast(
        tuple[datetime, Optional[float]],
        series[0],
    )
    first_slice: List[tuple[datetime, Optional[float]]] = cast(
        List[tuple[datetime, Optional[float]]],
        series[1:3],
    )
    value_at_datetime: Optional[float] = cast(
        Optional[float],
        series[datetime(2026, 5, 2, 2, 0)],
    )
    values_at_date: List[Optional[float]] = cast(
        List[Optional[float]],
        series[date(2026, 5, 1)],
    )

    assert first_item == (datetime(2026, 5, 1, 0, 0), 10.0)
    assert first_slice == [
        (datetime(2026, 5, 1, 1, 0), 0.0),
        (datetime(2026, 5, 1, 2, 0), 0.0),
    ]
    assert value_at_datetime == 50.0
    assert values_at_date == [10.0, 0.0, 0.0]
    assert series.mean is not None
    assert series.stddev is not None

    series.__set_unit__("ug/m3")
    assert series.get_unit == "ug/m3"
    assert series.values[0] == 0.01

    series.__set_unit__("ng/m3")
    assert series.get_unit == "ng/m3"
    assert series.values[0] == 10.0


def check_analyzers(series: TimeSeries) -> None:
    analyzers: List[SeriesValidator | SimpleReporter] = [
        OutlierDetector(k=1.5),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=20.0),
        SimpleReporter(),
    ]

    for analyzer in analyzers:
        messages: List[str] = analyzer.analyze(series)
        print(f"== {analyzer.__class__.__name__} ==")
        print("\n".join(messages) if messages else "(no messages)")
        print()


def check_station(path: Path) -> None:
    station: Station = Station.from_csv_by_code(path, "DsBialka")
    stations: List[Station] = Station.load_all_from_csv(path)

    assert station.code == "DsBialka"
    assert station.name
    assert station.lat != 0.0
    assert station.lon != 0.0
    assert len(stations) > 0
    assert stations[0] == station


def check_measurements(directory: Path) -> None:
    measurements: Measurements = Measurements(directory)
    validators: List[SeriesValidator] = [
        ThresholdDetector(threshold=0.0),
    ]

    assert len(measurements) > 0
    assert "C6H6" in measurements

    series_by_parameter: List[TimeSeries] = measurements.get_by_parameter("C6H6")
    first_series: TimeSeries = series_by_parameter[0]
    series_by_station: List[TimeSeries] = measurements.get_by_station(first_series.station_code)
    anomalies: dict[str, list[str]] = measurements.detect_all_anomalies(validators)

    assert len(series_by_parameter) > 0
    assert len(series_by_station) > 0
    assert "C6H6_1g" in anomalies
    assert len(anomalies["C6H6_1g"]) > 0


def main() -> None:
    project_root: Path = Path(__file__).resolve().parent.parent
    station_path: Path = project_root / "List4" / "data" / "station" / "stacje.csv"
    measurements_path: Path = project_root / "List4" / "data" / "measurements"

    series: TimeSeries = build_example_series()
    check_time_series(series)
    check_analyzers(series)
    check_station(station_path)
    check_measurements(measurements_path)

    print("All List8 checks passed.")


if __name__ == "__main__":
    main()
