from datetime import datetime

from time_series import TimeSeries
from measurements import Measurements
from series_validator import OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from simple_reporter import SimpleReporter


def main() -> None:
    measurements = Measurements('C:/Users/Piotrek/PycharmProjects/Jezyki_Skryptowe/List4/data/measurements')

    validators = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=20.0)
    ]

    # print(measurements.detect_all_anomalies(validators, preload=True))

    dates = [
        datetime(2026, 5, 1, 0, 0),
        datetime(2026, 5, 2, 0, 0),
        datetime(2026, 5, 3, 0, 0),
        datetime(2026, 5, 4, 0, 0),
        datetime(2026, 5, 5, 0, 0),
        datetime(2026, 5, 6, 0, 0),
    ]

    values = [10.0, 0.0, 0.0, 0.0, 12.0, 50.0]

    series = TimeSeries(
        name="As(PM10)",
        station_code="TEST_01",
        averaging_time="24g",
        dates=dates,
        values=values,
        unit="ng/m3",
    )

    print(series.get_unit)
    for i in range(0, 5):
        print(series.values[i])
    series.__set_unit__("ug/m3")
    print(series.get_unit)
    for i in range(0, 5):
        print(series.values[i])

    series.__set_unit__("ng/m3")
    print(series.get_unit)
    for i in range(0, 5):
        print(series.values[i])    


if __name__ == '__main__':
    main()