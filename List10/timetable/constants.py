from enum import Enum


class GtfsFile(str, Enum):
    STOPS = "stops.txt"
    ROUTES = "routes.txt"
    CALENDAR = "calendar.txt"
    TRIPS = "trips.txt"
    STOP_TIMES = "stop_times.txt"


class GtfsColumn(str, Enum):
    STOP_ID = "stop_id"
    STOP_CODE = "stop_code"
    STOP_NAME = "stop_name"
    STOP_LAT = "stop_lat"
    STOP_LON = "stop_lon"

    ROUTE_ID = "route_id"
    AGENCY_ID = "agency_id"
    ROUTE_SHORT_NAME = "route_short_name"
    ROUTE_LONG_NAME = "route_long_name"
    ROUTE_DESC = "route_desc"
    ROUTE_TYPE = "route_type"

    SERVICE_ID = "service_id"
    TRIP_ID = "trip_id"
    TRIP_HEADSIGN = "trip_headsign"
    DIRECTION_ID = "direction_id"

    ARRIVAL_TIME = "arrival_time"
    DEPARTURE_TIME = "departure_time"
    STOP_SEQUENCE = "stop_sequence"

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    START_DATE = "start_date"
    END_DATE = "end_date"


class DatabaseColumn(str, Enum):
    ID = "id"
    STOP_ID = GtfsColumn.STOP_ID.value
    STOP_CODE = GtfsColumn.STOP_CODE.value
    STOP_NAME = GtfsColumn.STOP_NAME.value
    STOP_LAT = GtfsColumn.STOP_LAT.value
    STOP_LON = GtfsColumn.STOP_LON.value

    ROUTE_ID = GtfsColumn.ROUTE_ID.value
    AGENCY_ID = GtfsColumn.AGENCY_ID.value
    ROUTE_SHORT_NAME = GtfsColumn.ROUTE_SHORT_NAME.value
    ROUTE_LONG_NAME = GtfsColumn.ROUTE_LONG_NAME.value
    ROUTE_DESC = GtfsColumn.ROUTE_DESC.value
    ROUTE_TYPE = GtfsColumn.ROUTE_TYPE.value

    SERVICE_ID = GtfsColumn.SERVICE_ID.value
    TRIP_ID = GtfsColumn.TRIP_ID.value
    TRIP_HEADSIGN = GtfsColumn.TRIP_HEADSIGN.value
    DIRECTION_ID = GtfsColumn.DIRECTION_ID.value

    ARRIVAL_TIME = GtfsColumn.ARRIVAL_TIME.value
    DEPARTURE_TIME = GtfsColumn.DEPARTURE_TIME.value
    ARRIVAL_SECONDS = "arrival_seconds"
    DEPARTURE_SECONDS = "departure_seconds"
    STOP_SEQUENCE = GtfsColumn.STOP_SEQUENCE.value

    MONDAY = GtfsColumn.MONDAY.value
    TUESDAY = GtfsColumn.TUESDAY.value
    WEDNESDAY = GtfsColumn.WEDNESDAY.value
    THURSDAY = GtfsColumn.THURSDAY.value
    FRIDAY = GtfsColumn.FRIDAY.value
    SATURDAY = GtfsColumn.SATURDAY.value
    SUNDAY = GtfsColumn.SUNDAY.value
    START_DATE = GtfsColumn.START_DATE.value
    END_DATE = GtfsColumn.END_DATE.value


class TableName(str, Enum):
    STOPS = "stops"
    ROUTES = "routes"
    SERVICE_CALENDAR = "service_calendar"
    TRIPS = "trips"
    STOP_TIMES = "stop_times"


class ForeignKeyAction(str, Enum):
    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"


class RelationshipName(str, Enum):
    CALENDAR = "calendar"
    ROUTE = "route"
    STOP = "stop"
    STOP_TIMES = "stop_times"
    TRIP = "trip"
    TRIPS = "trips"


class CascadeOption(str, Enum):
    ALL_DELETE_ORPHAN = "all, delete-orphan"


class ConstraintName(str, Enum):
    STOP_TIMES_TRIP_SEQUENCE = "uq_stop_times_trip_sequence"


class IndexName(str, Enum):
    STOP_TIMES_STOP_DEPARTURE = "ix_stop_times_stop_departure"
    STOP_TIMES_TRIP_SEQUENCE = "ix_stop_times_trip_sequence"


class NamingConventionKey(str, Enum):
    CHECK = "ck"
    FOREIGN_KEY = "fk"
    INDEX = "ix"
    PRIMARY_KEY = "pk"
    UNIQUE = "uq"


class NamingConventionPattern(str, Enum):
    CHECK = "ck_%(table_name)s_%(constraint_name)s"
    FOREIGN_KEY = "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    INDEX = "ix_%(column_0_label)s"
    PRIMARY_KEY = "pk_%(table_name)s"
    UNIQUE = "uq_%(table_name)s_%(column_0_name)s"


class DatabaseSetting(str, Enum):
    SQLITE_SUFFIX = ".sqlite3"
    SQLITE_URL_PREFIX = "sqlite:///"


class SqliteOption(str, Enum):
    CHECK_SAME_THREAD = "check_same_thread"
    CONNECT_EVENT = "connect"
    FOREIGN_KEYS_ON = "PRAGMA foreign_keys=ON"


class GtfsValue(str, Enum):
    TRUE = "1"


class TextEncoding(str, Enum):
    UTF_8 = "utf-8"
    UTF_8_SIG = "utf-8-sig"


class GtfsDateFormat(str, Enum):
    BASIC_DATE = "%Y%m%d"


class TimeToken(str, Enum):
    SEPARATOR = ":"


class AnalyticsLabel(str, Enum):
    DIRECTION = "direction"
    DEPARTURES = "departures"
    DISTINCT_ROUTES = "distinct_routes"
    HOUR = "hour"


class AnalyticsDefault(str, Enum):
    UNKNOWN_DIRECTION = "unknown"


class WebPath(str, Enum):
    HOME = "/"
    STOPS = "/stops"
    STOP = "/stop"


class WebDefault(str, Enum):
    HOST = "127.0.0.1"


class HttpHeader(str, Enum):
    CONTENT_LENGTH = "Content-Length"
    CONTENT_TYPE = "Content-Type"
    LOCATION = "Location"


class ContentType(str, Enum):
    HTML_UTF_8 = "text/html; charset=utf-8"


class QueryParam(str, Enum):
    SEARCH = "q"
    STOP_ID = "stop_id"


class CliArgument(str, Enum):
    BATCH_SIZE = "--batch-size"
    DATABASE = "database"
    DROP_EXISTING = "--drop-existing"
    ECHO_SQL = "--echo-sql"
    GTFS_ZIP = "gtfs_zip"
    HOST = "--host"
    LIMIT = "--limit"
    PORT = "--port"
    REPLACE = "--replace"
    SEARCH = "--search"
    STOP_ID = "--stop-id"


class CliAction(str, Enum):
    STORE_TRUE = "store_true"


def foreign_key_target(table: TableName, column: DatabaseColumn) -> str:
    return f"{table.value}.{column.value}"
