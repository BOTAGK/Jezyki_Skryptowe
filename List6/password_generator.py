import string
import random
from collections.abc import Iterator

class PasswrodGenerator:
    length: int
    count: int
    charset: str
    current: int

    def __init__(self, length: int, count: int, charset: str = string.ascii_letters + string.digits) -> None:
        self.length = length
        self.count = count
        self.charset = charset
        self.current = 0

    def __iter__(self) -> Iterator[str]:
        return self
    
    def __next__(self) -> str:
        if self.current >= self.count:
            raise StopIteration
        
        password = "".join(random.choices(self.charset, k=self.length))
        self.current += 1
        return password
    
gen = PasswrodGenerator(8, 3)
print("first password:", next(gen))

print("Next passwords:")
for pas in gen:
    print(pas)