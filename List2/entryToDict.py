def entry_to_dict(entry):

    if not isinstance(entry, tuple):
        raise TypeError(f"Argument musi być krotką, a otrzymano: {type(entry).__name__}")

    # potrzebujemy co najmniej 8 indeksow
    if len(entry) < 9:
        raise ValueError(f"Krotka jest niekompletna (ma {len(entry)} elementow")

    result = {"ts": entry[0], "uid": entry[1], "id_orig_h": entry[2], "id_orig_p": entry[3], "id_resp_h": entry[4],
              "id_resp_p": entry[5], "method": entry[6], "host": entry[7], "uri": entry[8],
              "stauts_code": entry[9] if len(entry) > 9 else None,
              "status_text": entry[10] if len(entry) > 10 else None}

    return result