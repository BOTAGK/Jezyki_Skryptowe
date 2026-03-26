from List2.readLog import LogEntry
from List2.utils.validateLog import validate_log

def get_entries_by_extension(log, ext) -> list[LogEntry]:
    validate_log(log)

    if not log:
        return []

    #upewniamy sie ze ext jest z malej  i ma kropke
    clean_ext = ext.lower()
    ext_with_dot = clean_ext if clean_ext.startswith('.') else f".{clean_ext}"

    #bierzemy tylko pierwsza czesc bez znaku zapytania
    return [ entry for entry in log
             if entry.uri.split('?')[0].lower().endswith(ext_with_dot)
    ]