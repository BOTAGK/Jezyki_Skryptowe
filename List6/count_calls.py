from functools import wraps
from typing import Any, Callable

def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.calls += 1
        return func(*args, **kwargs)
   
    wrapper.calls = 0
    return wrapper

@count_calls
def example_function() -> None:
    print("Function")

if __name__ == "__main__":
    example_function()
    example_function()
    example_function()
    print(f"function was called {example_function.calls} times")    