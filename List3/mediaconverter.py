import argparse
import subprocess
import sys
from pathlib import Path
from utils import get_output_dir, generate_out_filename, detect_tool, log_conversion

def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Uniwersalny konwerter multimediów")
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Katalog z plikami do konwersji"
    )

    parser.add_argument(
        "-f", "--format",
        required=True,
        help="Docelowy format (np. webm, png, mp3)"
    )

    return parser.parse_args()

def convert_file(input_path: Path, output_dir: Path, target_format: str) -> None:
    tool = detect_tool(input_path)
    if not tool:
        print(f"'{input_path.name}' - nierozpoznany typ pliku.")
        return

    out_filename = generate_out_filename(input_path.name, target_format)
    out_path = output_dir / out_filename

    print(f"Konwertowanie '{input_path.name}' do .{target_format} używając {tool}...")

    if tool == "ffmpeg":
        command = ["ffmpeg", "-y", "-i", str(input_path), str(out_path)]
    elif tool == "magick":
        command = ["magick", str(input_path), str(out_path)]
    elif tool == "pandoc":
        command = ["pandoc", str(input_path), "-o", str(out_path)]


    try:
        result = subprocess.run(command,
                                capture_output=True,
                                text=True,
                                encoding="utf-8",
                                errors="replace",
                                check=False)
        
        if result.returncode == 0:
            print(f"Zapisano jako: {out_filename}")

            # zapis do csv
            log_file = output_dir / "history.csv"
            log_conversion(log_file, input_path, out_path, target_format, tool)
        else:
            print(f"Błąd: W programie {tool} wystąpił problem:\n{result.stderr}", file=sys.stderr)


    # jesli nie znajdzie programu
    except FileNotFoundError:
        print(f"\nBłąd: Nie znaleziono programu '{tool}' w systemie", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    args = setup_argparse()

    if not args.input_dir.is_dir():
        print(f"Błąd: '{args.input_dir}' nie jest katalogiem.", file=sys.stderr)
        sys.exit(1)

    out_dir = get_output_dir()
    print(f"Katalog źródłowy: {args.input_dir.absolute()}")
    print(f"Katalog docelowy: {out_dir.absolute()}\n")

    files_found = False
    for file_path in args.input_dir.iterdir():
        if file_path.is_file():
            files_found = True
            convert_file(file_path, out_dir, args.format)

    if not files_found:
        print(f"Nie znaleziono żadnych plików w katalogu '{args.input_dir}'.")

if __name__ == "__main__":
    main()