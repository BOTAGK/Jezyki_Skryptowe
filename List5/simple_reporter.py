from datetime import datetime

from series_validator import OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from time_series import TimeSeries


class SimpleReporter:
    def analyze(self, series: TimeSeries) -> list[str]:
        return [f'Info: {series.station_name} at {series.station_code} has mean = {series.mean} {series.unit}']

def build_example_series() -> TimeSeries:
    dates = [
        datetime(2026, 5, 1, 0, 0),
        datetime(2026, 5, 2, 0, 0),
        datetime(2026, 5, 3, 0, 0),
        datetime(2026, 5, 4, 0, 0),
        datetime(2026, 5, 5, 0, 0),
        datetime(2026, 5, 6, 0, 0),
    ]

    values = [10.0, 0.0, 0.0, 0.0, 12.0, 50.0]

    return TimeSeries(
        name="As(PM10)",
        station_code="TEST_01",
        averaging_time="24g",
        dates=dates,
        values=values,
        unit="ng/m3",
    )


def main() -> None:
    series = build_example_series()

    analyzers = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=20.0),
        SimpleReporter()
    ]

    for analyzer in analyzers:
        results = analyzer.analyze(series)
        print(f"== {analyzer.__class__.__name__} ==")
        if not results:
            print("(brak komunikatów)")
        else:
            for line in results:
                print(line)
        print()


if __name__ == "__main__":
    main()
