from List2.entryToDict import entry_to_dict
from List2.utils.validateLog import validate_log

UID_INDEX = 1

def log_to_dict(log):
    validate_log(log)

    session_dict = {}

    if not log:
        return session_dict

    for entry in log:
        entry_uid = entry[UID_INDEX]
        session_dict[entry_uid] = session_dict.get(entry_uid, []).append(entry_to_dict(entry))

    return session_dict