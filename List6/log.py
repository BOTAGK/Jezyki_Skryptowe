from __future__ import annotations

from functools import wraps
import logging
from datetime import datetime, timezone
from typing import Any, Callable, cast


def log(level: int = logging.INFO) -> Callable[[Any], Any]:
    def decorator(obj: Any) -> Any:
        if isinstance(obj, type):
            return _decorate_class(obj, level)
        return _decorate_function(obj, level)

    return decorator


def _decorate_function(func: Callable[..., Any], level: int) -> Callable[..., Any]:
    logger = logging.getLogger(func.__module__)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        started_at = datetime.now(timezone.utc)

        logger.log(
            level,
            "Wywołanie funkcji %s args=%s kwargs=%s time=%s",
            func.__qualname__, args, kwargs, started_at.isoformat(),
        )

        try:
            result = func(*args, **kwargs)
        except Exception:
            duration = (datetime.now(timezone.utc) - started_at).total_seconds()
            logger.exception(
                "Funkcja %s zakończyła się wyjątkiem po %.6f s",
                func.__qualname__, duration,
            )
            raise

        duration = (datetime.now(timezone.utc) - started_at).total_seconds()
        logger.log(
            level,
            "Funkcja %s zakończona po %.6f s, wynik=%r",
            func.__qualname__, duration, result,
        )
        return result

    return wrapper


def _decorate_class(cls: type[Any], level: int) -> type[Any]:
    logger = logging.getLogger(cls.__module__)
    original_init = cls.__init__

    @wraps(original_init)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        logger.log(
            level,
            "Tworzenie instancji klasy %s args=%s kwargs=%s",
            cls.__qualname__, args, kwargs,
        )

        original_init(self, *args, **kwargs)

    cls.__init__ = __init__
    return cls


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(name)s:%(message)s",
    )

    @log(logging.INFO)
    def add(a: int, b: int) -> int:
        return a + b

    @log(logging.DEBUG)
    class Point:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    print(add(2, 3))
    point = Point(10, 20)
    print(point.x, point.y)
