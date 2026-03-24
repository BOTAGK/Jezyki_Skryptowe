import os
import sys

def echo(s):
    return s

def run_safely(main_func):
    try:
        return main_func()
    except BrokenPipeError:
        os._exit(0)
    except EOFError as e:
        print(f"Blad wejscia: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Blad: {e}", file=sys.stderr)
        sys.exit(1)