import sys


def set_up_Streams():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

def is_sentence(c):
    return c in ".?!"

def run_safely(main_func):
    try:
        main_func()

    except BrokenPipeError:
        sys.stdout.close()
        sys.stderr.close()
    except EOFError as e:
        print(f"Blad wejscia: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Blad: {e}", file=sys.stderr)
        sys.exit(1)