from datetime import datetime
from pathlib import Path
from typing import Any, List

import pytest

from List8.measurements import Measurements
from List8.series_validator import OutlierDetector, ThresholdDetector, ZeroSpikeDetector
from List8.simple_reporter import SimpleReporter
from List8.time_series import TimeSeries


@pytest.fixture
def measurements_directory(tmp_path: Path) -> Path:
    csv_path: Path = tmp_path / "2026_PM10_1g.csv"
    csv_path.write_text(
        "\n".join(
            [
                "Metadane",
                "Czas pomiaru,TEST_01,TEST_02",
                "Jednostka,ng/m3,ng/m3",
                "Czas usredniania,1g,1g",
                "Zrodlo,test,test",
                "Komentarz,,",
                '05/01/26 00:00,10.0,"1,5"',
                "05/02/26 00:00,0.0,",
                "05/03/26 00:00,0.0,brak",
                "05/04/26 00:00,0.0,4.0",
                "05/05/26 00:00,12.0,5.0",
                "05/06/26 00:00,50.0,6.0",
            ]
        ),
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture
def measurements(measurements_directory: Path) -> Measurements:
    return Measurements(measurements_directory)


def test_measurements_builds_index_from_csv_metadata(
    measurements: Measurements,
) -> None:
    assert len(measurements) == 2
    assert "PM10" in measurements
    assert "NO2" not in measurements


def test_get_by_parameter_loads_matching_time_series(
    measurements: Measurements,
) -> None:
    series_list: List[TimeSeries] = measurements.get_by_parameter("PM10")

    assert len(series_list) == 2
    assert {series.station_code for series in series_list} == {"TEST_01", "TEST_02"}
    assert all(series.station_name == "PM10" for series in series_list)
    assert all(series.averaging_time == "1g" for series in series_list)


def test_get_by_station_returns_only_requested_station(
    measurements: Measurements,
) -> None:
    series_list: List[TimeSeries] = measurements.get_by_station("TEST_02")

    assert len(series_list) == 1
    assert series_list[0].station_code == "TEST_02"
    assert series_list[0].dates[0] == datetime(2026, 5, 1, 0, 0)
    assert series_list[0].values == [1.5, None, None, 4.0, 5.0, 6.0]
    assert measurements.get_by_station("UNKNOWN") == []


@pytest.mark.parametrize(
    ("analyzer", "expected_fragment"),
    [
        (OutlierDetector(k=1.5), "Outlier detected"),
        (ZeroSpikeDetector(), "Zero spike detected"),
        (ThresholdDetector(threshold=20.0), "Threshold exceeded"),
        (SimpleReporter(), "Info: PM10 at TEST_01"),
    ],
)
def test_detect_all_anomalies_returns_messages_for_duck_typed_analyzers(
    measurements_directory: Path,
    analyzer: Any,
    expected_fragment: str,
) -> None:
    measurements: Measurements = Measurements(measurements_directory)

    results: dict[str, List[str]] = measurements.detect_all_anomalies(
        [analyzer],
        preload=True,
    )
    messages: List[str] = results["PM10_1g"]

    assert len(messages) > 0
    assert messages + [] == messages
    assert expected_fragment in "\n".join(messages)
