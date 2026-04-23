import argparse
from collections import deque
import os
from pathlib import Path
import sys
import time

def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Własna implementacja programu 'tail'")
    # nargs="?" - nie wymaga nazwy flagi
    parser.add_argument(
       "file",
       nargs="?",
       type=Path,
       help="Ścieżka do pliku (opcjonalny)"
    )

    parser.add_argument(
        "-n", "--lines",
        type=int,
        default=10,
        help="Liczba linii do wypisania (domyślnie: 10)"
    )

    parser.add_argument(
        "-f", "--follow",
        action="store_true",
        help="Nie kończ działania, śledź zmiany w pliku i wypisuj dopisywane na bieżaco"
    )


    
    return parser.parse_args()

def print_last_lines(iterator, n: int, mode: str, is_reverse: bool) -> None:

    if mode == "chars":
        content = iterator.read()

        tail_content = content[-n:] if n > 0 else ""

        if is_reverse:
            lines = tail_content.splitlines(keepends=True)
            lines.reverse()
            for line in lines:
                sys.stdout.write(line)
        else:
            sys.stdout.write(tail_content)
    else:
        
        last_lines = list(deque(iterator, maxlen=n))

        if is_reverse:
            last_lines.reverse()
            
        for line in last_lines:
            sys.stdout.write(line)

def follow_file(file_path: Path) -> None:
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        # przewijamy wskaznik na sam koniec pliku
        file.seek(0, os.SEEK_END)

        while True:
            current_position = file.tell()
            line = file.readline()

            if not line:
                time.sleep(0.1)  
                # jesli plik zostal skasowany lub przeniesiony, przewijamy wskaznik na poczatek pliku
                if current_position > os.stat(file_path).st_size:
                    file.seek(0)
            else:
                sys.stdout.write(line)
                sys.stdout.flush()

def main() -> None:
    args = setup_argparse()

    env_reverse = os.environ.get("TAIL_REVERSE", "").lower()

    is_reverse = env_reverse in ["1", "true", "yes", "y"]

    env_mode = os.environ.get("TAIL_MODE", "lines").lower()
    mode = "chars" if env_mode == "chars" else "lines"


    if args.follow and not args.file:
        print("Błąd: Opcja -f/--follow wymaga podania ścieżki do pliku.", file=sys.stderr)
        sys.exit(1)

    
    if args.file:
        if not args.file.is_file():
            print(f"Błąd: Plik '{args.file}' nie istnieje lub nie jest plikiem.", file=sys.stderr)
            sys.exit(1)

        with open(args.file, 'r', encoding='utf-8', errors='replace') as file:
            print_last_lines(file, args.lines, mode, is_reverse)

        if args.follow:
            try:
                follow_file(args.file)
            except KeyboardInterrupt:
                print("\nZakończono śledzenie pliku.")
                sys.exit(0)
    # Jezeli uzytkownik nie podal sciezki do pliku, czytamy z wejscia standardowego
    else:
        print_last_lines(sys.stdin, args.lines, mode, is_reverse)

if __name__ == "__main__":
    main() 
