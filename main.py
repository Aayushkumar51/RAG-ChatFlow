# Ensure project root is on path so "server" package is found (e.g. on Render)
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from server.main import app

def main():
    print("Hello from medicalassistant!")


if __name__ == "__main__":
    main()
