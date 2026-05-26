from __future__ import annotations

from pathlib import Path
import sys


# potrzebne żeby metody z list2 działały
def _ensure_repo_on_path() -> None:
    if __package__:
        return
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def main() -> None:
    _ensure_repo_on_path()
    from List7.log_browser_pyside import run_app

    ui_path = Path(__file__).with_name("ui") / "log_browser.ui"
    # run_app(ui_path)
    run_app()

if __name__ == "__main__":
    main()
