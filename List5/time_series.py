from datetime import datetime
from typing import List, Optional


class TimeSeries:
    station_name: str
    station_code: str
    averaging_time: str
    dates: List[datetime.datetime]
    values: List[Optional[float]]
    unit: str

    
