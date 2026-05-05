import argparse
import subprocess
import sys
from pathlib import Path


def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Program zwracający ścieżkę do plików komendy")
    parser.add_argument(
       "command",
       nargs="?",
       help="Nazwa komendy"
    )

    return parser.parse_args()

def main() -> None:
    args = setup_argparse()

    process = subprocess.run(
        ["where", args.command],
        shell=True,
        capture_output=True,
        text=True
    )

    # jeśli wszystko zadziałało
    if process.returncode == 0:
        print(process.stdout.strip())

if __name__ == "__main__":
    main()