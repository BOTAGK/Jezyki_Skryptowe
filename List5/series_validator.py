from abc import ABC, abstractmethod
from typing import List

from List5.time_series import TimeSeries

class SeriesValidator(ABC):

    @abstractmethod
    def anazlyze(self, series: 'TimeSeries') -> List[str]:
        pass

class OutlierDetector(SeriesValidator):
    k: float

    def __init__(self, k: float):
        self.k = k 

    def analyze(self, series: 'TimeSeries') -> List[str]:
        anomalies = []
        mean = series.mean
        stddev = series.stddev

        if mean is None or stddev is None:
            return [f"[{series.station_code}] Series {series.name} has insufficient data for analysis."]
        
        for data, value in zip(series.dates, series.values):
            if value is None:
                continue
            if abs(value - mean) > self.k * stddev:
                anomalies.append(
                    f"Outlier detected ({series.station_code}) on {data}: {value} (mean: {mean}, stddev: {stddev})"
                    f" - exceeds {self.k} standard deviations from the mean."
                )
        return anomalies
    
class ZeroSpikeDetector(SeriesValidator):
    consecutive_threshold: int = 3

    def analyze(self, series: 'TimeSeries') -> List[str]:
        anomalies = []
        consecutive_count = 0
        start_date = None

        for data, value in zip(series.dates, series.values):
            if value == 0 or value is None:
                if consecutive_count == 0:
                    start_date = data
                consecutive_count += 1
            else:
                if consecutive_count >= self.consecutive_threshold:
                    anomalies.append(
                        f"Zero spike detected ({series.station_code}) for {series.station_name} from {start_date} to {data} - "
                        f"{consecutive_count} consecutive zero values."
                    )
                consecutive_count = 0

        if consecutive_count >= self.consecutive_threshold:
            anomalies.append(
                f"Zero spike detected ({series.station_code}) for {series.station_name} from {start_date} to {series.dates[-1]} - "
                f"{consecutive_count} consecutive zero values."
            )
        return anomalies                    

class ThresholdDetector(SeriesValidator):
    threshold: float

    def __init__(self, threshold: float):
        self.threshold = threshold

    def analyze(self, series: 'TimeSeries') -> List[str]:
        anomalies = []

        for data, value in zip(series.dates, series.values):
            if value is None:
                continue
            if value > self.threshold:
                anomalies.append(
                    f"Threshold exceeded ({series.station_code}) for {series.station_name} on {data}: {value} (threshold: {self.threshold})"
                )
        return anomalies    