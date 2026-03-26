from typing import Final, NamedTuple, Optional
from datetime import datetime


class EntryDictKey:
    TS: Final = "ts"
    UID: Final = "uid"
    ORIG_H: Final = "orig_h"
    ORIG_P: Final = "orig_p"
    RESP_H: Final = "resp_h"
    RESP_P: Final = "resp_p"
    METHOD: Final = "method"
    HOST: Final = "host"
    URI: Final = "uri"
    STATUS_CODE: Final = "status_code"

class LogEntry(NamedTuple):
    ts: datetime
    uid: str
    id_orig_h: str
    id_orig_p: int
    id_resp_h: str
    id_resp_p: int
    method: str
    host: str
    uri: str
    status_code: Optional[int]
    status_text: Optional[str]


