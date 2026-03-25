from utils.validateLog import validate_log


def count_by_method(log) -> dict[str, int]:

    validate_log(log)

    methods_count = {}

    for entry in log:

        method = entry.method

        methods_count[method] = methods_count.get(method, 0) + 1

    return methods_count
