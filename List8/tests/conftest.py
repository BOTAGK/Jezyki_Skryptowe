from datetime import datetime
from typing import List, Optional

import pytest

from time_series import TimeSeries


@pytest.fixture
def example_series() -> TimeSeries:
    dates: List[datetime] = [
        datetime(2026, 5, 1, 0, 0),
        datetime(2026, 5, 2, 0, 0),
        datetime(2026, 5, 3, 0, 0),
        datetime(2026, 5, 4, 0, 0),
        datetime(2026, 5, 5, 0, 0),
        datetime(2026, 5, 6, 0, 0),
    ]
    values: List[Optional[float]] = [10.0, 0.0, 0.0, 0.0, 12.0, 50.0]

    return TimeSeries(
        name="As(PM10)",
        station_code="TEST_01",
        averaging_time="24g",
        dates=dates,
        values=values,
        unit="ng/m3",
    )
