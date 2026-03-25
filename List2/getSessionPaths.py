from List2.entryToDict import entry_to_dict
from List2.utils.validateLog import validate_log

# przyjmuje log jako liste krotek
def get_session_paths(log):
    validate_log(log)

    session_paths = {}

    if not log:
        return session_paths

    for entry in log:
        entry_uid = entry.uid

        if entry_uid not in session_paths:
            session_paths[entry_uid] = []

        session_paths[entry_uid].append(entry.uri)

    return session_paths