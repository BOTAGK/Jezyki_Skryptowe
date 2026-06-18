from __future__ import annotations

from html import escape
from textwrap import dedent

from timetable.constants import QueryParam, WebPath
from timetable.schemas.analytics import StopAnalytics, StopOption


def render_stop_list_page(query: str, stops: list[StopOption]) -> str:
    options = "\n".join(render_stop_option(stop) for stop in stops)
    body = f"""
        <h1>Timetable stops</h1>
        <form action="{WebPath.STOPS.value}" method="get">
            <input name="{QueryParam.SEARCH.value}" value="{escape(query)}" placeholder="Filter stops" autofocus>
            <button type="submit">Search</button>
        </form>
        <form action="{WebPath.STOP.value}" method="get">
            <p><label for="{QueryParam.STOP_ID.value}">Stop</label></p>
            <select id="{QueryParam.STOP_ID.value}" name="{QueryParam.STOP_ID.value}" size="18" required>
                {options}
            </select>
            <p><button type="submit">Show analysis</button></p>
        </form>
    """
    return render_page("Timetable stops", body)


def render_stop_report_page(analytics: StopAnalytics) -> str:
    body = f"""
        <p><a href="{WebPath.HOME.value}">Back to stops</a></p>
        <h1>{escape(analytics.stop.stop_name)}</h1>
        <p>Stop id: {escape(analytics.stop.stop_id)}</p>
        <ul>
            <li>Distinct routes: {analytics.route_count}</li>
            <li>Departures: {analytics.departure_count}</li>
            <li>First departure: {escape(analytics.first_departure or "-")}</li>
            <li>Last departure: {escape(analytics.last_departure or "-")}</li>
        </ul>
        <h2>Most frequent directions</h2>
        {render_direction_table(analytics)}
        <h2>Busiest hours</h2>
        {render_hour_table(analytics)}
    """
    return render_page("Stop analysis", body)


def render_stop_option(stop: StopOption) -> str:
    label = stop.stop_name
    if stop.stop_code:
        label = f"{label} [{stop.stop_code}]"
    label = f"{label} - {stop.stop_id}"
    return f'<option value="{escape(stop.stop_id)}">{escape(label)}</option>'


def render_direction_table(analytics: StopAnalytics) -> str:
    rows = "".join(
        f"<tr><td>{escape(item.direction)}</td><td>{item.departures}</td></tr>"
        for item in analytics.popular_directions
    )
    return render_table(
        "<tr><th>Direction</th><th>Departures</th></tr>",
        rows or '<tr><td colspan="2">No data</td></tr>',
    )


def render_hour_table(analytics: StopAnalytics) -> str:
    rows = "".join(
        "<tr>"
        f"<td>{escape(item.hour_label)}</td>"
        f"<td>{item.departures}</td>"
        f"<td>{item.distinct_routes}</td>"
        "</tr>"
        for item in analytics.busiest_hours
    )
    return render_table(
        "<tr><th>Hour</th><th>Departures</th><th>Routes</th></tr>",
        rows or '<tr><td colspan="3">No data</td></tr>',
    )


def render_table(header: str, rows: str) -> str:
    return f"""
        <table>
            <thead>{header}</thead>
            <tbody>{rows}</tbody>
        </table>
    """


def render_page(title: str, body: str) -> str:
    return dedent(
        f"""\
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{escape(title)}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 32px; max-width: 960px; }}
                input, select, button {{ font: inherit; margin: 4px 0; }}
                input, select {{ width: 100%; padding: 6px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 24px; }}
                th, td {{ border: 1px solid #ccc; padding: 6px; text-align: left; }}
            </style>
        </head>
        <body>
        {dedent(body).strip()}
        </body>
        </html>
        """
    )
