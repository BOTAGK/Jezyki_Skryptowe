PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS stops (
    stop_id TEXT PRIMARY KEY,
    stop_code TEXT,
    stop_name TEXT NOT NULL,
    stop_lat REAL,
    stop_lon REAL
);

CREATE TABLE IF NOT EXISTS routes (
    route_id TEXT PRIMARY KEY,
    agency_id TEXT,
    route_short_name TEXT,
    route_long_name TEXT,
    route_desc TEXT,
    route_type INTEGER
);

CREATE TABLE IF NOT EXISTS service_calendar (
    service_id TEXT PRIMARY KEY,
    monday INTEGER NOT NULL DEFAULT 0,
    tuesday INTEGER NOT NULL DEFAULT 0,
    wednesday INTEGER NOT NULL DEFAULT 0,
    thursday INTEGER NOT NULL DEFAULT 0,
    friday INTEGER NOT NULL DEFAULT 0,
    saturday INTEGER NOT NULL DEFAULT 0,
    sunday INTEGER NOT NULL DEFAULT 0,
    start_date DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS trips (
    trip_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    service_id TEXT,
    trip_headsign TEXT,
    direction_id INTEGER,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (service_id) REFERENCES service_calendar(service_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS stop_times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id TEXT NOT NULL,
    arrival_time TEXT,
    departure_time TEXT,
    arrival_seconds INTEGER,
    departure_seconds INTEGER,
    stop_id TEXT NOT NULL,
    stop_sequence INTEGER NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE (trip_id, stop_sequence)
);

CREATE INDEX IF NOT EXISTS ix_stops_stop_name ON stops(stop_name);
CREATE INDEX IF NOT EXISTS ix_trips_route_id ON trips(route_id);
CREATE INDEX IF NOT EXISTS ix_trips_service_id ON trips(service_id);
CREATE INDEX IF NOT EXISTS ix_stop_times_trip_sequence ON stop_times(trip_id, stop_sequence);
CREATE INDEX IF NOT EXISTS ix_stop_times_stop_departure ON stop_times(stop_id, departure_seconds);
