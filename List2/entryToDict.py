def entry_to_dict(entry):

    if not isinstance(entry, tuple):
        raise TypeError("Argument musi być krotką")

    # potrzebujemy co najmniej 8 indeksow
    if len(entry) < 8:
        raise ValueError(f"Nieprawidłowy format wejscia (zbyt mało kolumn: {entry[:50]}...")

    return {
        "ts": entry[0],
        "uid": entry[1],
        "id_orig_h": entry[2],
        "id_orig_p": entry[3],
        "id_resp_h": entry[4],
        "id_resp_p": entry[5],
        "method": entry[6],
        "host": entry[7],
        "uri": entry[8],
        "status_code": entry[9],
        "status_text": entry[10]
    }