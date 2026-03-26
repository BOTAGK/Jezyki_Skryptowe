from collections import defaultdict

from List2.utils.validateLog import validate_log

# przyjmuje log jako liste krotek
def get_session_paths(log):
    validate_log(log)

    if not log:
        return {}

    session_paths = defaultdict(list)

    for entry in log:
        session_paths[entry.uid].append(entry.uri)

    #zwracamy jako zwykly slownik
    return dict(session_paths)