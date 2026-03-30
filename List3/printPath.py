import os
import sys
from pathlib import Path


def get_path_dirs() -> list[Path]:
    path_value = os.environ.get("PATH", "")
    return [Path(entry) for entry in path_value.split(os.pathsep) if entry]

def get_windows_pathext() -> tuple[str, ...]:
    pathext_value = os.environ.get("PATHEXT", "")
    return tuple(ext.lower() for ext in pathext_value.split(";") if ext)

def parse_cli_args(argv: list[str]) -> bool:
    with_executables = False
    for arg in argv:
        if arg in ("-e", "--with-executables"):
            with_executables = True

        elif arg in ("-h", "--help"):
            print("Uzycie: python printPath.py [-e|--with-executables]")
            sys.exit(0)

        else:
            raise ValueError(f"Nieznany parametr: {arg}")

    return with_executables

def is_executable(file_path: Path, pathext: tuple[str, ...]) -> bool:
    if not file_path.is_file():
        return False

    if os.name == "nt":
        return file_path.suffix.lower() in pathext

    return os.access(file_path, os.X_OK)

def get_executables(directory: Path, pathext: tuple[str, ...]) -> list[Path]:
    if not directory.exists() or not directory.is_dir():
        return []

    executables: list[Path] = []
    for entry in directory.iterdir():
        if is_executable(entry, pathext):
            executables.append(entry)

    return sorted(executables, key=lambda path: path.name.lower())

def main() -> None:
    with_executables = parse_cli_args(sys.argv[1:])
    path_dirs = get_path_dirs()

    pathext = get_windows_pathext() if os.name == "nt" else ()

    if not with_executables:
        for directory in path_dirs:
            print(directory)
        return

    for directory in path_dirs:
        print(directory)
        executables = get_executables(directory, pathext)
        if not executables:
            print("  (brak plikow wykonywalnych)")
            continue

        for executable in executables:
            print(f"  {executable.name}")

if __name__ == "__main__":
    main()
