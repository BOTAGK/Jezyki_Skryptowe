import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys


def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Menadżer zlecający analizę plików")
    parser.add_argument(
        "directory",
        type=Path,
        help="Ścieżka do katalogu z plikami"
    )

    return parser.parse_args()

def main():
    args = setup_argparse()
    
    if not args.directory.is_dir():
        print(f"Błąd: {args.directory} nie jest katalogiem.", file=sys.stderr)
        sys.exit(1)

    results = []

    # sprawdzenie czy ścieżka jest plikiem
    for file_path in args.directory.iterdir():
        if not file_path.is_file():
            continue
        
        process = subprocess.run(
            [sys.executable, Path(__file__).with_name("analyzer.py")],
            input=str(file_path),
            text=True,
            capture_output=True
        )

        # jeśli wszystko zadziałało
        if process.returncode == 0 and process.stdout.strip():
            file_stats = json.loads(process.stdout)
            results.append(file_stats)

    if not results:
        print("Nie znaleziono plików lub nie udało się ich przeanalizować.")
        return


    total_files = len(results)
    total_chars = sum(stat["total_chars"] for stat in results)
    total_words = sum(stat["total_words"] for stat in results)
    total_lines = sum(stat["total_lines"] for stat in results)

    global_chars = Counter(stat["most_freq_char"] for stat in results if stat["most_freq_char"])
    global_words = Counter(stat["most_freq_word"] for stat in results if stat["most_freq_word"])

    best_char = global_chars.most_common(1)[0][0] if global_chars else "Brak"
    best_word = global_words.most_common(1)[0][0] if global_words else "Brak"


    print("=== RAPORT ZBIORCZY ===")
    print(f"Przeanalizowane pliki: {total_files}")
    print(f"Całkowita liczba znaków: {total_chars}")
    print(f"Całkowita liczba słów: {total_words}")
    print(f"Całkowita liczba wierszy: {total_lines}")
    print(f"Najczęściej występujący znak w plikach: '{best_char}'")
    print(f"Najczęściej występujące słowo w plikach: '{best_word}'")

if __name__ == "__main__":
    main()