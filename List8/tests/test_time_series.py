from typing import List, Optional

import pytest
from datetime import datetime, date
from time_series import TimeSeries

def test_getitem_with_int(example_series: TimeSeries) -> None:
    date_obj: datetime
    value: Optional[float]

    date_obj, value = example_series[0]
    assert date_obj == datetime(2026, 5, 1, 0, 0)
    assert value == 10.0

def test_getitem_with_slice(example_series: TimeSeries) -> None:
    result: List[tuple[datetime, Optional[float]]] = example_series[1:3]

    assert len(result) == 2
    assert result[0] == (datetime(2026, 5, 2, 0, 0), 0.0)
    assert result[1] == (datetime(2026, 5, 3, 0, 0), 0.0)

def test_getitem_with_date(example_series: TimeSeries) -> None:
    value: Optional[float] = example_series[date(2026, 5, 5)]  
    assert value == 12.0

def test_getitem_missing_date(example_series: TimeSeries) -> None:
    missing_date: date = date(2026, 5, 10)

    with pytest.raises(KeyError):
        _ = example_series[missing_date]

def test_getitem_with_datetime(example_series: TimeSeries) -> None:
    value: Optional[float] = example_series[datetime(2026, 5, 6, 0, 0)]
    assert value == 50.0

def test_mean_with_valid_data(example_series: TimeSeries) -> None:
    mean_value: float = example_series.mean
    assert mean_value == pytest.approx(12.0)

def test_mean_with_none_values() -> None:
    series_with_none: TimeSeries = TimeSeries(
        name="As(PM10)",
        station_code="TEST_02",
        averaging_time="24g",
        dates=[
            datetime(2026, 5, 1, 0, 0),
            datetime(2026, 5, 2, 0, 0),
            datetime(2026, 5, 3, 0, 0),
        ],
        values=[10, None, None],
        unit="ng/m3",
    )

    mean_value: float = series_with_none.mean
    assert mean_value == pytest.approx(10.0)

def test_mean_with_all_none_values() -> None:
    series_all_none: TimeSeries = TimeSeries(
        name="As(PM10)",
        station_code="TEST_03",
        averaging_time="24g",
        dates=[
            datetime(2026, 5, 1, 0, 0),
            datetime(2026, 5, 2, 0, 0),
            datetime(2026, 5, 3, 0, 0),
        ],
        values=[None, None, None],
        unit="ng/m3",
    )

    mean_value: Optional[float] = series_all_none.mean
    assert mean_value is None

def test_stddev_with_valid_data(example_series: TimeSeries) -> None:
    stddev_value: Optional[float] = example_series.stddev
    assert stddev_value == pytest.approx(19.39, abs=0.01)

def test_stddev_with_none_values() -> None:
    series_with_none: TimeSeries = TimeSeries(
        name="As(PM10)",
        station_code="TEST_04",
        averaging_time="24g",
        dates=[
            datetime(2026, 5, 1, 0, 0),
            datetime(2026, 5, 2, 0, 0),
            datetime(2026, 5, 3, 0, 0),
        ],
        values=[10, 20, None],
        unit="ng/m3",
    )

    stddev_value: Optional[float] = series_with_none.stddev
    assert stddev_value == pytest.approx(7.07, abs=0.01)

def test_stddev_with_all_none_values() -> None:
    series_all_none: TimeSeries = TimeSeries(
        name="As(PM10)",
        station_code="TEST_05",
        averaging_time="24g",
        dates=[
            datetime(2026, 5, 1, 0, 0),
            datetime(2026, 5, 2, 0, 0),
            datetime(2026, 5, 3, 0, 0),
        ],
        values=[None, None, None],
        unit="ng/m3",
    )

    stddev_value: Optional[float] = series_all_none.stddev
    assert stddev_value is None
    
     
