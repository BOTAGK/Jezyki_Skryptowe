import argparse
import os
from pathlib import Path


def get_path_dirs() -> list[Path]:
    path_value = os.environ.get("PATH", "")
    return [Path(entry) for entry in path_value.split(os.pathsep) if entry]

def get_windows_pathext() -> tuple[str, ...]:
    pathext_value = os.environ.get("PATHEXT", "")
    return tuple(ext.lower() for ext in pathext_value.split(";") if ext)

def is_executable(file_path: Path, pathext: tuple[str, ...]) -> bool:
    if not file_path.is_file():
        return False

    if os.name == "nt":
        return file_path.suffix.lower() in pathext
    
    #for unix-like systems, check if the file has execute permissions    
    return os.access(file_path, os.X_OK)

def get_executables(directory: Path, pathext: tuple[str, ...]) -> list[Path]:
    if not directory.exists() or not directory.is_dir():
        return []

    executables: list[Path] = []

    try:
        for entry in directory.iterdir():
            if is_executable(entry, pathext):
                executables.append(entry)
    except PermissionError:
        pass            

    return sorted(executables, key=lambda path: path.name.lower())

def setup_argparse() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser(description="Eksplorator zmiennej PATH")
    parser.add_argument(
        "-e", "--with-executables",
        action="store_true",
        help="Wypisz również pliki wykonywalne znajdujace sie w katalogach"
    )
    return parser.parse_args()


def main() -> None:
    args = setup_argparse()
    path_dirs = get_path_dirs()
    pathext = get_windows_pathext() if os.name == "nt" else ()

    for directory in path_dirs:
        print(directory)

        if not args.with_executables:
            continue

        executables = get_executables(directory, pathext)

        if not executables:
            print("  (brak plików wykonywalnych)")
        else:
            for exe in executables:
                print(f"  {exe.name}")    

if __name__ == "__main__":
    main()
