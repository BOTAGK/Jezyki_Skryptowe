from collections import Counter
from List2.utils.validateLog import validate_log

def get_extension_stats(log):
    validate_log(log)

    if not log:
        return {}

    extensions_count = Counter()

    for entry in log:
        # bierzemy tylko dane bez query
        based_uri = entry.uri.split('?')[0]

        if '.' in based_uri:
            extension = based_uri.split('.')[-1]

            if '/' not in extension and extension:
                extension = extension.lower()

                extensions_count[extension] += 1

    return dict(extensions_count)