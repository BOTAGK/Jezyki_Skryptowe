import csv
from datetime import datetime
import mimetypes
import os
from pathlib import Path


def get_output_dir() -> Path:
    """Odczytuje zmienna srodowiskowa i towrzy folder docelowy"""
    dir_path_str =  os.environ.get("CONVERTED_DIR", "converted")
    out_dir = Path(dir_path_str)
    # Tworzymy katalog docelowy, jeśli nie istnieje
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def generate_out_filename(original_name: str, target_ext: str) -> str:
    """Generuje nazwe z timestampel"""

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Dodaje kropke do rozszerzenia, jesli jej brak
    if not target_ext.startswith("."):
        target_ext = "." + target_ext

    base_name = Path(original_name).stem
    return f"{timestamp}-{base_name}{target_ext}"

def detect_tool(file_path: Path) -> str | None:
    """Używa moduły mimetypes do wykrycia typu pliku i zwraca odpowiednie narzędzie"""

    mine_type, _ = mimetypes.guess_type(file_path)

    if not mine_type:
        return None
    
    if mine_type.startswith("image"):
        return "magick"
    elif mine_type.startswith("video") or mine_type.startswith("audio"):
        return "ffmpeg"
    
    return None

def log_conversion(log_file: Path, original: Path, output: Path, fmt: str, tool: str) -> None:
    """Dopisuje rekord o konwersji do pliku CSV"""
    file_exists = log_file.exists()

    with open(log_file, "a", newline="", encoding="utf-8") as f:
        # Wykorzystujemy csv.writer aby łatwo zapisywać nazwane kolumny
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "original_file", "output_format","output_path", "tool_used"
            ])
        
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(sep =" ", timespec="seconds"),
            "original_file": str(original.absolute()),
            "output_format": fmt,
            "output_path": str(output.absolute()),
            "tool_used": tool
        })    