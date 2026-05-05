import sys
from os import environ


def main():
    def print_env(name, value):
        print(f"{name} = {value}")

    process_env(print_env)


def process_env(callback) -> None:
    filters = [arg.lower() for arg in sys.argv[1:]]

    entries = sorted(environ.items(), key=lambda item: item[0].lower())

    for name, value in entries:
        if not filters or any(fragment in name.lower() for fragment in filters):
            callback(name, value)


if __name__ == "__main__":
    main()