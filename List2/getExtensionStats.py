from List2.utils.validateLog import validate_log


def get_extension_stats(log):
    validate_log(log)

    uri_counts = {}

    if not log:
        return uri_counts

    for entry in log:
        # bierzemy tylko dane bez query
        entry_uri = (entry.uri).split('?')[0]

        if entry_uri and '.' in entry_uri:
            parts = entry_uri.split('.')
            extension = parts[-1]
    
            if '/' not in extension:
                uri_counts[extension] = uri_counts.get(extension, 0) + 1

    return uri_counts