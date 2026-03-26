from List2.utils.validateLog import validate_log
from collections import Counter

def count_status_classes(log):
    validate_log(log)

    #zwracamy slownic jako counter z licznosciami
    return Counter(
        f"{entry.status_code // 100}xx"
        for entry in log
        if entry.status_code is not None
    )