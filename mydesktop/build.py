import sys
from PyInstaller.__main__ import run


def main() -> None:
    """Build a standalone executable using PyInstaller."""
    args = ["--onefile", "-m", "mydesktop"] + sys.argv[1:]
    run(args)


if __name__ == "__main__":
    main()
