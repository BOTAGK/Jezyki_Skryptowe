from datetime import datetime, date
import statistics
from typing import List, Optional, Union


class TimeSeries:
    station_name: str
    station_code: str
    averaging_time: str
    dates: List[datetime]
    values: List[Optional[float]]
    unit: str 

    
    def __init__(
            self, 
            name: str, 
            station_code: str, 
            averaging_time: str,
            dates: List[datetime], 
            values: List[Optional[float]], 
            unit: str
        ) -> None:

        self.station_name = name
        self.station_code = station_code
        self.averaging_time = averaging_time
        self.dates = dates
        self.values = values
        self.unit = unit

    def __getitem__(
            self, key: Union[int, slice, date, datetime]
        ) -> (
            tuple[datetime, Optional[float]] 
            | list[tuple[datetime, Optional[float]]] 
            | Optional[float]
            | list[Optional[float]]
        ):

        if isinstance(key, int):
            return self.dates[key], self.values[key]

        if isinstance(key, slice):
            return list(zip(self.dates[key], self.values[key]))

        if isinstance(key, datetime):
            for date_obj, value in zip(self.dates, self.values):
                if date_obj == key:
                    return value

            raise KeyError(f"No data found for datetime: {key}")

        if isinstance(key, date):
            results: list[Optional[float]] = []

            for date_obj, value in zip(self.dates, self.values):
                if date_obj.date() == key:
                    results.append(value)

            if not results:
                raise KeyError(f"No data found for date: {key}")

            return results[0] if len(results) == 1 else results

        raise TypeError(
            f"Invalid key type: {type(key)}. Expected int, slice, date, or datetime."
        )  

    def __set_unit__(self, unit: str) -> None:
        if self.unit == "ug/m3" and unit == "ng/m3":
            self.unit = unit
            self.values = [v * 1000 if v is not None else None for v in self.values] 
        elif self.unit == "ng/m3" and unit == "ug/m3":
            self.unit = unit
            self.values = [v / 1000 if v is not None else None for v in self.values]
        else:
            raise ValueError(f"Invalid units: self - {self.unit} and unit - {unit}")   
            

    @property
    def mean(self) -> Optional[float]:
        valid_values: List[float] = [v for v in self.values if v is not None]
        return statistics.mean(valid_values) if valid_values else None
    
    @property
    def stddev(self) -> Optional[float]:
        valid_values: List[float] = [v for v in self.values if v is not None]
        return statistics.stdev(valid_values) if len(valid_values) > 1 else None

    @property
    def get_unit(self) -> str:
        return self.unit

    