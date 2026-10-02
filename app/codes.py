# app/main.py
from app.codes import make_code      # absolute import (preferred)
from . import codes                  # relative import, only inside a package

def main() -> None:
    print(make_code())

if __name__ == "__main__":           # true only when run directly, not on import
    main()  