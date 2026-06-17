from __future__ import annotations

import argparse

from timetable.schemas.analytics import StopAnalytics, StopOption
from timetable.services.analytics_service import AnalyticsService
from timetable.services.database_service import DatabaseService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze departures for one stop.")
    parser.add_argument(
        "database",
        help="Database name or path. Missing .sqlite3 suffix is added automatically.",
    )
    parser.add_argument("--stop-id", help="Skip prompt and analyze this stop id.")
    parser.add_argument("--search", help="Initial stop-name filter for the prompt.")
    parser.add_argument("--limit", type=int, default=50, help="Stop list size.")
    return parser.parse_args()


def choose_stop(service: AnalyticsService, search: str | None, limit: int) -> str:
    query = search
    while True:
        if query is None:
            query = input("Stop name filter (empty = first stops): ").strip() or None

        stops = service.list_stops(search=query, limit=limit)
        if not stops:
            print("No stops found.")
            query = None
            continue

        print()
        for index, stop in enumerate(stops, start=1):
            print(f"{index:>3}. {format_stop_option(stop)}")

        selected = input("\nChoose stop number, or type new filter: ").strip()
        if selected.isdigit():
            number = int(selected)
            if 1 <= number <= len(stops):
                return stops[number - 1].stop_id
            print("Number outside the list.")
        else:
            query = selected or None


def format_stop_option(stop: StopOption) -> str:
    code = f" [{stop.stop_code}]" if stop.stop_code else ""
    return f"{stop.stop_name}{code} (id={stop.stop_id})"


def print_report(analytics: StopAnalytics) -> None:
    print()
    print(f"Stop: {format_stop_option(analytics.stop)}")
    print(f"Distinct routes: {analytics.route_count}")
    print(f"Departures: {analytics.departure_count}")
    print(f"First departure: {analytics.first_departure or '-'}")
    print(f"Last departure: {analytics.last_departure or '-'}")

    print("\nMost frequent directions:")
    if analytics.popular_directions:
        for item in analytics.popular_directions:
            print(f"  {item.direction}: {item.departures}")
    else:
        print("  No departure data.")

    print("\nBusiest hours by departures:")
    if analytics.busiest_hours:
        for item in analytics.busiest_hours:
            print(
                f"  {item.hour_label}: {item.departures} departures, "
                f"{item.distinct_routes} distinct routes"
            )
    else:
        print("  No hourly data.")


def main() -> None:
    args = parse_args()
    database = DatabaseService(args.database)

    with database.session() as session:
        service = AnalyticsService(session)
        stop_id = args.stop_id or choose_stop(service, args.search, args.limit)
        analytics = service.analyze_stop(stop_id)

    print_report(analytics)


if __name__ == "__main__":
    main()
