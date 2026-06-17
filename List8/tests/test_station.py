from station import Station, StationColumn

def make_station(code: str) -> Station:
    return Station({
        StationColumn.CODE: code,
    })

def test_station_eq_for_same_and_different_codes() -> None:
    station: Station = make_station('STN')
    same_code: Station = make_station('STN')
    different_code: Station = make_station('STN2')

    assert station == same_code
    assert station != different_code

    