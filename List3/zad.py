import argparse
import os
from pathlib import Path
import subprocess
import sys


def setup_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wyświetla ostatnie linie lub znaki z pliku")
    parser.add_argument(
        "komenda",
        type=str,
        help="Nazwa komendy (np notepad)"
    )
    return parser.parse_args()

def main() -> None:
    args = setup_argparse()
    cmd = args.komenda

    if sys.platform.startswith("win"):
        tool = "where"
    else:
        tool = "which"

    try:
        result = subprocess.run(
            [tool, cmd],
            capture_output=True,
            text=True,
            check=True
        )   

        found_path = result.stdout.strip().splitlines()[0]  # bierzemy pierwszą znalezioną ścieżkę

        print(found_path)
        sys.exit(0)    

    except subprocess.CalledProcessError:
        print(f"Błąd: Nie znaleziono komendy '{cmd}' w systemie.", file=sys.stderr)
        sys.exit(1)
        
             
    # path_env = os.environ.get("PATH", "")
    # folders = path_env.split(os.pathsep)

    # pathext_env = os.environ.get("PATHEXT", "")

    # if pathext_env:
    #     extensions = pathext_env.lower().split(os.pathsep)
    # else:
    #     extensions = [""]

    # if "" not in extensions:
    #     extensions.insert(0, "")

    # for folder_str in folders:
    #     if not folder_str:
    #         continue
            
    #     folder_path = Path(folder_str)

        
    #     for ext in extensions:
    #         possible_path = folder_path / f"{cmd}{ext}"
            
    #         if possible_path.is_file():
    #             print(possible_path.absolute())
    #             sys.exit(0)

    # print(f"Błąd: Nie znaleziono komendy '{cmd}' w żadnym z folderów w zmiennej PATH.", file=sys.stderr)
    # sys.exit(1)


if __name__ == "__main__":
    main()        