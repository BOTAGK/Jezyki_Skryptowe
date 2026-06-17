from datetime import datetime
from typing import List

from simple_reporter import SimpleReporter
from time_series import TimeSeries


def test_simple_reporter_returns_info_message_for_time_series() -> None:
    series: TimeSeries = TimeSeries(
        name="PM10",
        station_code="TEST_01",
        averaging_time="24g",
        dates=[
            datetime(2026, 5, 1, 0, 0),
            datetime(2026, 5, 2, 0, 0),
        ],
        values=[10.0, 20.0],
        unit="ng/m3",
    )
    reporter: SimpleReporter = SimpleReporter()

    messages: List[str] = reporter.analyze(series)

    assert messages == ["Info: PM10 at TEST_01 has mean = 15.0 ng/m3"]
