from __future__ import annotations

import argparse
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from timetable.schemas.analytics import StopAnalytics, StopOption
from timetable.services.analytics_service import AnalyticsService
from timetable.services.database_service import DatabaseService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small timetable web UI.")
    parser.add_argument(
        "database",
        help="Database name or path. Missing .sqlite3 suffix is added automatically.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def build_handler(database: DatabaseService) -> type[BaseHTTPRequestHandler]:
    class TimetableHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            if parsed.path in ("/", "/stops"):
                query = params.get("q", [""])[0].strip()
                self.render_stop_list(query)
                return

            if parsed.path == "/stop":
                stop_id = params.get("stop_id", [""])[0].strip()
                self.render_stop_report(stop_id)
                return

            self.send_error(404, "Page not found")

        def render_stop_list(self, query: str) -> None:
            with database.session() as session:
                service = AnalyticsService(session)
                stops = service.list_stops(search=query or None, limit=200)

            options = "\n".join(render_stop_option(stop) for stop in stops)
            body = f"""
            <section class="toolbar">
                <form action="/stops" method="get" class="search">
                    <input name="q" value="{escape(query)}" placeholder="Filter stops" autofocus>
                    <button type="submit">Search</button>
                </form>
            </section>
            <form action="/stop" method="get" class="panel">
                <label for="stop_id">Stop</label>
                <select id="stop_id" name="stop_id" size="18" required>
                    {options}
                </select>
                <button type="submit">Show analysis</button>
            </form>
            """
            self.write_html(render_page("Timetable stops", body))

        def render_stop_report(self, stop_id: str) -> None:
            if not stop_id:
                self.redirect("/")
                return

            try:
                with database.session() as session:
                    service = AnalyticsService(session)
                    analytics = service.analyze_stop(stop_id)
            except LookupError:
                self.send_error(404, "Stop not found")
                return

            self.write_html(render_page("Stop analysis", render_report(analytics)))

        def redirect(self, location: str) -> None:
            self.send_response(302)
            self.send_header("Location", location)
            self.end_headers()

        def write_html(self, html: str) -> None:
            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args: object) -> None:
            return

    return TimetableHandler


def render_stop_option(stop: StopOption) -> str:
    label = stop.stop_name
    if stop.stop_code:
        label = f"{label} [{stop.stop_code}]"
    label = f"{label} - {stop.stop_id}"
    return f'<option value="{escape(stop.stop_id)}">{escape(label)}</option>'


def render_report(analytics: StopAnalytics) -> str:
    direction_rows = "".join(
        f"<tr><td>{escape(item.direction)}</td><td>{item.departures}</td></tr>"
        for item in analytics.popular_directions
    )
    hour_rows = "".join(
        "<tr>"
        f"<td>{escape(item.hour_label)}</td>"
        f"<td>{item.departures}</td>"
        f"<td>{item.distinct_routes}</td>"
        "</tr>"
        for item in analytics.busiest_hours
    )

    return f"""
    <nav><a href="/">Back to stops</a></nav>
    <header>
        <h1>{escape(analytics.stop.stop_name)}</h1>
        <p class="muted">Stop id: {escape(analytics.stop.stop_id)}</p>
    </header>
    <section class="metrics">
        <article><span>Distinct routes</span><strong>{analytics.route_count}</strong></article>
        <article><span>Departures</span><strong>{analytics.departure_count}</strong></article>
        <article><span>First departure</span><strong>{escape(analytics.first_departure or "-")}</strong></article>
        <article><span>Last departure</span><strong>{escape(analytics.last_departure or "-")}</strong></article>
    </section>
    <section class="grid">
        <article class="panel">
            <h2>Most frequent directions</h2>
            <table>
                <thead><tr><th>Direction</th><th>Departures</th></tr></thead>
                <tbody>{direction_rows or '<tr><td colspan="2">No data</td></tr>'}</tbody>
            </table>
        </article>
        <article class="panel">
            <h2>Busiest hours</h2>
            <table>
                <thead><tr><th>Hour</th><th>Departures</th><th>Routes</th></tr></thead>
                <tbody>{hour_rows or '<tr><td colspan="3">No data</td></tr>'}</tbody>
            </table>
        </article>
    </section>
    """


def render_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
        :root {{
            color-scheme: light;
            --bg: #f6f8fb;
            --ink: #16202a;
            --muted: #617080;
            --line: #d9e0e8;
            --panel: #ffffff;
            --accent: #2457a6;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            min-height: 100vh;
            font-family: Arial, Helvetica, sans-serif;
            background: var(--bg);
            color: var(--ink);
        }}
        main {{
            width: min(1120px, calc(100% - 32px));
            margin: 32px auto;
        }}
        h1, h2 {{ margin: 0 0 12px; }}
        h1 {{ font-size: 30px; }}
        h2 {{ font-size: 18px; }}
        a {{ color: var(--accent); }}
        .muted {{ color: var(--muted); margin-top: -6px; }}
        .toolbar {{ margin-bottom: 16px; }}
        .search {{
            display: flex;
            gap: 8px;
            max-width: 620px;
        }}
        input, select, button {{
            font: inherit;
            border: 1px solid var(--line);
            border-radius: 6px;
        }}
        input {{
            flex: 1;
            min-width: 0;
            padding: 10px 12px;
            background: white;
        }}
        button {{
            padding: 10px 14px;
            background: var(--accent);
            color: white;
            border-color: var(--accent);
            cursor: pointer;
        }}
        select {{
            width: 100%;
            min-height: 420px;
            padding: 8px;
            background: white;
        }}
        .panel {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 16px;
        }}
        .panel label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        .panel button {{ margin-top: 12px; }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin: 20px 0;
        }}
        .metrics article {{
            background: white;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px;
        }}
        .metrics span {{
            display: block;
            color: var(--muted);
            font-size: 13px;
        }}
        .metrics strong {{
            display: block;
            margin-top: 6px;
            font-size: 24px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px 8px;
            border-bottom: 1px solid var(--line);
            text-align: left;
            vertical-align: top;
        }}
        th {{ color: var(--muted); font-size: 13px; }}
        @media (max-width: 760px) {{
            main {{ width: min(100% - 20px, 1120px); margin: 16px auto; }}
            .search, .grid {{ display: block; }}
            .search button {{ margin-top: 8px; width: 100%; }}
            .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .grid .panel + .panel {{ margin-top: 16px; }}
        }}
    </style>
</head>
<body>
    <main>{body}</main>
</body>
</html>"""


def main() -> None:
    args = parse_args()
    database = DatabaseService(args.database)
    handler = build_handler(database)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Web UI: http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
