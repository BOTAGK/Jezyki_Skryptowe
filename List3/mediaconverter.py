import argparse
import subprocess
import sys
from pathlib import Path
from utils import get_output_dir, generate_out_filename, detect_tool, log_conversion

def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Uniwersalny konwerter multimediów (FFmpeg / ImageMagick)")
    parser.add_argument("input_dir", type=Path, help="Katalog z plikami do konwersji")
    # Argument wymagany określający docelowy format
    parser.add_argument("-f", "--format", required=True, help="Docelowy format (np. webm, png, mp3)")
    return parser.parse_args()

def convert_file(input_path: Path, output_dir: Path, target_format: str) -> None:
    """Zarządza konwersją pojedynczego pliku."""
    tool = detect_tool(input_path)
    if not tool:
        print(f"  [Pomijam] '{input_path.name}' - nierozpoznany typ pliku.")
        return

    out_filename = generate_out_filename(input_path.name, target_format)
    out_path = output_dir / out_filename

    print(f"  [Proces] Konwertuję '{input_path.name}' do .{target_format} używając {tool}...")
    
    # Budujemy komendę dla subprocessa w zależności od narzędzia
    if tool == "ffmpeg":
        # -loglevel error : wyłącza setki wierszy technicznego "bełkotu" ffmpeg z konsoli
        command = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(input_path), str(out_path)]
    else: 
        # ImageMagick używa nowej komendy 'magick' 
        command = ["magick", str(input_path), str(out_path)]

    try:
        # Odpalamy zewnętrzny program
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"  [Sukces] Zapisano jako: {out_filename}")
            
            # Rejestrujemy operację w logu CSV
            log_file = output_dir / "history.csv"
            log_conversion(log_file, input_path, out_path, target_format, tool)
        else:
            print(f"  [Błąd] Program {tool} zgłosił problem:\n{result.stderr}", file=sys.stderr)
            
    #  Gdy system nie znajdzie programu 'ffmpeg' lub 'magick'
    except FileNotFoundError:
        print(f"\n[Błąd Krytyczny] Nie znaleziono programu '{tool}' w systemie!", file=sys.stderr)
        print("Upewnij się, że jest zainstalowany i dodany do zmiennej środowiskowej PATH.", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    args = setup_argparse()

    if not args.input_dir.is_dir():
        print(f"[Błąd] '{args.input_dir}' nie jest katalogiem.", file=sys.stderr)
        sys.exit(1)

    out_dir = get_output_dir()
    print("=== Rozpoczęcie pracy ===")
    print(f"Katalog źródłowy: {args.input_dir.absolute()}")
    print(f"Katalog docelowy: {out_dir.absolute()}\n")

    files_found = False
    for file_path in args.input_dir.iterdir():
        if file_path.is_file():
            files_found = True
            convert_file(file_path, out_dir, args.format)

    if not files_found:
        print(f"Nie znaleziono żadnych plików w katalogu '{args.input_dir}'.")
        
    print("\n=== Koniec pracy ===")

if __name__ == "__main__":
    main()