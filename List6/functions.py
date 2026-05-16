from functools import reduce
import math
import operator
from typing import Any
from collections.abc import Iterable, Callable, Iterator


def acronym(xs: list[str]) -> str:
    first_letters = map(lambda x: x[0], xs)

    return "".join(first_letters)

def acronym_2(xs: list[str]) -> str:
    first_letters = map(lambda x: x[0], xs)

    return reduce(operator.add, first_letters)

print(acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))
print(acronym_2(["Zakład", "Ubezpieczeń", "Społecznych"]))

def dumb_median(xs: list[int]) -> float:
    n = len(xs)
    mid = n // 2
    
    return xs[mid] if n % 2 != 0 else (xs[mid - 1] + xs[mid]) / 2.0

def median(xs: list[int]) -> float:
    sorted_xs = quicksort(xs)
    n = len(xs)

    mid = n // 2

    return sorted_xs[mid] if n % 2 != 0 else (sorted_xs[mid - 1] + sorted_xs[mid]) / 2.0
    
def  quicksort(xs: list[int]) -> list[int]:
    match xs:
        case []:
            return []
        
        case [pivot, *tail]:
            lesser = list(filter(lambda x: x <= pivot, tail))
            greater = list(filter(lambda x: x > pivot, tail))

            return quicksort(lesser) + [pivot] + quicksort(greater)   
        
print(median([1, 1, 19, 2, 3, 4, 4, 5, 1]))   
print(dumb_median([1, 1, 19, 2, 3, 4, 4, 5, 1]))     

def newton_sqrt(S: float, e: float) -> float:
    def iterate(guess: float) -> float:
        next_guess = (guess + S / guess) / 2.0
        return next_guess if abs(next_guess - guess) < e else iterate(next_guess)
    return iterate(S)

print(newton_sqrt(25, 0.0001))

def make_alpha_dict(text: str) -> dict[str, str]:
    words = text.split()
    #set was braking order by hash thats why we use dict.fromkeys
    return { char: [word for word in words if char in word ]
            for char in dict.fromkeys(text) if char.isalpha()
    }

print(make_alpha_dict("on i ona"))

def flatten(xs: Any) -> list[Any]:
    match xs:
        case []:
            return []
        case (head, *tail):
            return flatten(head) + flatten(tail)
        case _:
            return [xs]
        
print(flatten([1, [2, 3], [[4, 5], 6]]))        

def group_anagrams(xs: list[str]) -> dict[str, str]:
    return {
        canonical:
        [word for word in xs if "".join(sorted(word)) == canonical]
        for canonical in dict.fromkeys("".join(sorted(w)) for w in xs)
    }

print(group_anagrams(["kot", "tok", "pies", "kep", "pek"]))

def forall[T](pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return all(map(pred, iterable))

def exists[T](pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return any(map(pred, iterable))

def atleast[T](n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return sum(map(pred, iterable)) >= n

def atmost[T](n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return sum(map(pred, iterable)) <= n

is_even = lambda x: x % 2 == 0
liczby = [1, 2, 3, 4, 5, 6] 

print(f"Oczekiwane: False | Wynik: {forall(is_even, liczby)}")
print(f"Oczekiwane: True  | Wynik: {forall(is_even, [2, 4, 6])}\n")

print(f"Oczekiwane: True  | Wynik: {exists(is_even, liczby)}")
print(f"Oczekiwane: False | Wynik: {exists(is_even, [1, 3, 5])}\n")

print(f"atleast(3) -> Oczekiwane: True  | Wynik: {atleast(3, is_even, liczby)}")
print(f"atleast(4) -> Oczekiwane: False | Wynik: {atleast(4, is_even, liczby)}\n")

print(f"atmost(3) -> Oczekiwane: True  | Wynik: {atmost(3, is_even, liczby)}")
print(f"atmost(2) -> Oczekiwane: False | Wynik: {atmost(2, is_even, liczby)}")

def make_generator[T](f: Callable[[int], T]) -> Iterator[T]:
    n = 1
    while True:
        yield f(n)
        n += 1

def fibonacci(n: int) -> int:
    if n <= 2:
        return 1
    
    a, b = 1, 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b

def catalan(n: int) -> int:
    return math.comb(2 * n, n) // (n + 1)

gen_fib = make_generator(fibonacci)

print("Ciąg Fibonacciego (pierwsze 5 wyrazów):")
for _ in range(5):
    print(next(gen_fib))        

gen_catalan = make_generator(catalan)
print("Ciąg Catelana (pierwsze 5 wyrazów):")
for _ in range(5):
    print(next(gen_catalan))     