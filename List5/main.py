from measurements import Measurements
from series_validator import OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from simple_reporter import SimpleReporter


def main() -> None:
    measurements = Measurements('C:/Users/Piotrek/PycharmProjects/Jezyki_Skryptowe/List4/data/measurements')
    # measurements._load_data_if_needed(measurements._files_index[0])

    validators = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=20.0)
    ]

    print(measurements.detect_all_anomalies(validators, preload=True))


if __name__ == '__main__':
    main()