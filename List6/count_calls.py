from functools import wraps
from typing import Callable, Any


def count_calls(func):

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func(*args, **kwargs)
        wrapper.called += 1

    wrapper.called = 0
    return wrapper


if __name__ == '__main__':
    @count_calls
    def x(y: int) -> int:
        return y

    x(2)
    x(3)
    print(x.called)

