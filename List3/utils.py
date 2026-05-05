import csv
from datetime import datetime
import mimetypes
import os
from pathlib import Path


def get_output_dir() -> Path:
    dir_path_str =  os.environ.get("CONVERTED_DIR", Path(__file__).with_name("converted"))
    out_dir = Path(dir_path_str)

    # jesli nie ma folderu w PATH
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def generate_out_filename(original_name: str, target_ext: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d")

    if not target_ext.startswith("."):
        target_ext = "." + target_ext

    # nazwa bez suffixu
    base_name = Path(original_name).stem

    return f"{timestamp}-{base_name}{target_ext}"

def detect_tool(file_path: Path) -> str | None:
    type, _ = mimetypes.guess_type(file_path)

    if not type:
        return None
    
    if type.startswith("image"):
        return "magick"
    elif type.startswith("video") or type.startswith("audio"):
        return "ffmpeg"
    elif type.startswith("text") or type.startswith("md"):
        return "pandoc"
    
    
    return None

def log_conversion(log_file: Path, original: Path, output: Path, fmt: str, tool: str) -> None:
    file_exists = log_file.exists()

    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "original_file", "output_format", "output_path", "tool_used"
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