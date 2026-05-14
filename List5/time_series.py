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

    
    def __init__(self, name: str, station_code: str, averaging_time: str, 
                 dates: List[datetime], values: List[Optional[float]], unit: str):
        self.station_name = name
        self.station_code = station_code
        self.averaging_time = averaging_time
        self.dates = dates
        self.values = values
        self.unit = unit

    def __getitem__(self, key: Union[int, slice, date, datetime]):
        if isinstance(key, int):
            return self.values[key]
        elif isinstance(key, slice):
            return list(zip(self.dates[key], self.values[key]))
        
        elif isinstance(key, (date, datetime)):
            results = []
            
            for i, date_obj in enumerate(self.dates):
                if type(key) in datetime.date:
                    if date_obj.date() == key:
                        results.append((date_obj, self.values[i]))

                elif date_obj.date() == key:
                    results.append((date_obj, self.values[i]))

            if not results:
                raise KeyError(f"No data found for date: {key}")
            
            return results[0] if len(results) == 1 else results

        raise TypeError(f"Invalid key type: {type(key)}. Expected int, slice, datetime.date, or datetime.datetime.")   

    @property
    def mean(self) -> Optional[float]:
        valid_values = [v for v in self.values if v is not None]
        return statistics.mean(valid_values) if valid_values else None
    
    @property
    def stddev(self) -> Optional[float]:
        valid_values = [v for v in self.values if v is not None]
        return statistics.stdev(valid_values) if len(valid_values) > 1 else None

    @property
    def get_unit(self) -> Optional[str]:
        return self.unit

    def set_unit(self, new_unit: str) -> None:
        if (self.unit == ('ug/m3' or 'ng/m3')) and (new_unit == ('ug/m3' or 'ng/m3')):
            self.unit = new_unit
        else:
            raise ValueError(f"Invalid unit conversion from {self.unit} to {new_unit}. Only 'ug/m3' and 'ng/m3' are supported.")

        if self.unit == 'ng/m3' and new_unit == 'ug/m3':
            new_values = [v * 1000 for v in self.values if v is not None]
            self.values = new_values
            # for i, value in enumerate(self.values):
            #     if value is not None:
            #         self.values[i] = value/1000
        elif self.unit == 'ug/m3' and new_unit == 'ng/m3':
            new_values = [v * 1000 for v in self.values if v is not None]
            self.values = new_values
            # for i, value in enumerate(self.values):
            #     if value is not None:
            #         self.values[i] = value*1000