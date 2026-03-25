from List2.utils.validateLog import validate_log


def get_top_uris(log, n=10):
    validate_log(log)

    if not isinstance(n, int):
        raise TypeError("n musi byc dodatnia liczba całkowita")

    counts = {}

    for entry in log:
        uri = entry.uri
        counts[uri] = counts.get(uri, 0) + 1

    # porownywanie po licznosci
    sorted_uris = sorted(counts.items(), key = lambda item: item[1], reverse = True)
    return sorted_uris[:n]