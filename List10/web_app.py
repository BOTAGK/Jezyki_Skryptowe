from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from timetable.constants import (
    CliArgument,
    ContentType,
    HttpHeader,
    QueryParam,
    TextEncoding,
    WebDefault,
    WebPath,
)
from timetable.services.analytics_service import AnalyticsService
from timetable.services.database_service import DatabaseService
from timetable.web.templates import render_stop_list_page, render_stop_report_page


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small timetable web UI.")
    parser.add_argument(
        CliArgument.DATABASE.value,
        help="Database name or path. Missing .sqlite3 suffix is added automatically.",
    )
    parser.add_argument(CliArgument.HOST.value, default=WebDefault.HOST.value)
    parser.add_argument(CliArgument.PORT.value, type=int, default=8000)
    return parser.parse_args()


def build_handler(database: DatabaseService) -> type[BaseHTTPRequestHandler]:
    class TimetableHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            if parsed.path in (WebPath.HOME.value, WebPath.STOPS.value):
                query = params.get(QueryParam.SEARCH.value, [""])[0].strip()
                self.render_stop_list(query)
                return

            if parsed.path == WebPath.STOP.value:
                stop_id = params.get(QueryParam.STOP_ID.value, [""])[0].strip()
                self.render_stop_report(stop_id)
                return

            self.send_error(404, "Page not found")

        def render_stop_list(self, query: str) -> None:
            with database.session() as session:
                service = AnalyticsService(session)
                stops = service.list_stops(search=query or None, limit=1000)

            self.write_html(render_stop_list_page(query, stops))

        def render_stop_report(self, stop_id: str) -> None:
            if not stop_id:
                self.redirect(WebPath.HOME.value)
                return

            try:
                with database.session() as session:
                    service = AnalyticsService(session)
                    analytics = service.analyze_stop(stop_id)
            except LookupError:
                self.send_error(404, "Stop not found")
                return

            self.write_html(render_stop_report_page(analytics))

        def redirect(self, location: str) -> None:
            self.send_response(302)
            self.send_header(HttpHeader.LOCATION.value, location)
            self.end_headers()

        def write_html(self, html: str) -> None:
            data = html.encode(TextEncoding.UTF_8.value)
            self.send_response(200)
            self.send_header(HttpHeader.CONTENT_TYPE.value, ContentType.HTML_UTF_8.value)
            self.send_header(HttpHeader.CONTENT_LENGTH.value, str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args: object) -> None:
            return

    return TimetableHandler


def main() -> None:
    args = parse_args()
    database = DatabaseService(args.database)
    handler = build_handler(database)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Web UI: http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
