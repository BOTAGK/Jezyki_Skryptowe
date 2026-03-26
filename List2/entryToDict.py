IDX_TS = 0
IDX_UID = 1
IDX_ORIG_H = 2
IDX_ORIG_P = 3
IDX_RESP_H = 4
IDX_RESP_P = 5
IDX_METHOD = 6
IDX_HOST = 7
IDX_URI = 8
IDX_STATUS_CODE = 9
IDX_STATUS_TEXT = 10

MIN_ENTRY_LENGTH = 9

def entry_to_dict(entry):

    if not isinstance(entry, tuple):
        raise TypeError(f"Argument musi być krotką, a otrzymano: {type(entry).__name__}")

    # potrzebujemy co najmniej 8 indeksow
    if len(entry) < MIN_ENTRY_LENGTH:
        raise ValueError(f"Krotka jest niekompletna (ma {len(entry)} elementow")

    result = {
        "ts": entry[IDX_TS],
        "uid": entry[IDX_UID],
        "id_orig_h": entry[IDX_ORIG_H],
        "id_orig_p": entry[IDX_ORIG_P],
        "id_resp_h": entry[IDX_RESP_H],
        "id_resp_p": entry[IDX_RESP_P],
        "method": entry[IDX_METHOD],
        "host": entry[IDX_HOST],
        "uri": entry[IDX_URI],
        # Bezpieczne sprawdzanie opcjonalnych pól przy pomocy stałych
        "status_code": entry[IDX_STATUS_CODE] if len(entry) > IDX_STATUS_CODE else None,
        "status_text": entry[IDX_STATUS_TEXT] if len(entry) > IDX_STATUS_TEXT else None
    }

    return result