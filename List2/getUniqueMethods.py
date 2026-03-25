from List2.utils.validateLog import validate_log


def get_unique_methods(log) -> list[str]:
    validate_log(log)

    if not log:
        return []

    #set odrzuca duplikaty
    methods = {entry.method for entry in log}

    return list(methods)