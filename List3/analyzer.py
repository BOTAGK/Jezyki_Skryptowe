import json
from pathlib import Path
from collections import Counter
import sys


def analyze_path(file_path: Path) -> dict:

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    lines = content.splitlines()
    words = content.split()

    char_counts = Counter(content)   
    word_counts = Counter(words)

    most_freq_char = char_counts.most_common(1)[0][0] if char_counts else ""
    most_freq_word = word_counts.most_common(1)[0][0] if word_counts else ""

    return {
        "file_path": str(file_path),
        "total_chars": len(content),
        "total_words": len(words),
        "total_lines": len(lines),
        "most_freq_char": most_freq_char,
        "most_freq_word": most_freq_word
    }

def main():
    input_path = sys.stdin.read().strip()

    if not input_path:
        sys.exit(1)

    file_path = Path(input_path)
    if file_path.is_file():
        stats = analyze_path(file_path)
        print(json.dumps(stats))

if __name__ == "__main__":
    main()           