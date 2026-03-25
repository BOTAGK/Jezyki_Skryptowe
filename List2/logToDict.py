from List2.entryToDict import entry_to_dict
from List2.utils.validateLog import validate_log

# przyjmuje log jako liste krotek
def log_to_dict(log):
    validate_log(log)

    session_dict = {}

    if not log:
        return session_dict

    for entry in log:
        entry_uid = entry.uid

        if entry_uid not in session_dict:
            session_dict[entry_uid] = []

        session_dict[entry_uid].append(entry_to_dict(entry))

    return session_dict