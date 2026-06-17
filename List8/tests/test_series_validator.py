from datetime import datetime
from typing import Any, List

import pytest

from series_validator import OutlierDetector, ThresholdDetector, ZeroSpikeDetector
from simple_reporter import SimpleReporter
from time_series import TimeSeries


def test_outlier_detector_finds_value_more_than_k_stddev_from_mean(
    example_series: TimeSeries,
) -> None:
    detector: OutlierDetector = OutlierDetector(k=1.5)

    messages: List[str] = detector.analyze(example_series)

    assert len(messages) == 1
    assert "Outlier detected (TEST_01)" in messages[0]
    assert "50.0" in messages[0]
    assert "exceeds 1.5 standard deviations" in messages[0]


def test_zero_spike_detector_finds_three_consecutive_zero_or_none_values() -> None:
    series: TimeSeries = TimeSeries(
        name="PM10",
        station_code="TEST_02",
        averaging_time="24g",
        dates=[
            datetime(2026, 5, 1, 0, 0),
            datetime(2026, 5, 2, 0, 0),
            datetime(2026, 5, 3, 0, 0),
            datetime(2026, 5, 4, 0, 0),
        ],
        values=[8.0, 0.0, None, 0.0],
        unit="ng/m3",
    )
    detector: ZeroSpikeDetector = ZeroSpikeDetector()

    messages: List[str] = detector.analyze(series)

    assert len(messages) == 1
    assert "Zero spike detected (TEST_02)" in messages[0]
    assert "3 consecutive zero values" in messages[0]


def test_threshold_detector_finds_values_exceeding_defined_threshold() -> None:
    series: TimeSeries = TimeSeries(
        name="PM10",
        station_code="TEST_03",
        averaging_time="24g",
        dates=[
            datetime(2026, 5, 1, 0, 0),
            datetime(2026, 5, 2, 0, 0),
            datetime(2026, 5, 3, 0, 0),
            datetime(2026, 5, 4, 0, 0),
            datetime(2026, 5, 5, 0, 0),
        ],
        values=[5.0, 21.0, 20.0, 30.0, None],
        unit="ng/m3",
    )
    detector: ThresholdDetector = ThresholdDetector(threshold=20.0)

    messages: List[str] = detector.analyze(series)

    assert len(messages) == 2
    assert "21.0" in messages[0]
    assert "30.0" in messages[1]
    assert all("threshold: 20.0" in message for message in messages)


@pytest.mark.parametrize(
    "analyzer",
    [
        OutlierDetector(k=1.5),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=20.0),
        SimpleReporter(),
    ],
)
def test_detect_all_anomalies_analyzers_duck_typing(
    analyzer: Any,
    example_series: TimeSeries,
) -> None:
    messages: List[str] = analyzer.analyze(example_series)

    assert len(messages) > 0
    assert messages + [] == messages
    assert "\n".join(messages)
