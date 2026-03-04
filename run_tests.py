import sys
import pytest


def main():
    # Run pytest in the repository root
    return pytest.main(["-q", "tests"])


if __name__ == "__main__":
    sys.exit(main())
