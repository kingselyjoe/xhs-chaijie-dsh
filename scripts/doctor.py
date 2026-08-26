#!/usr/bin/env python3
"""Read-only installation and layout diagnostics for xhs-chaijie-dsh."""

from pathlib import Path
import os
import platform
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    dsh_home = Path(os.environ.get("DSH_HOME", Path.home() / ".dsh")).expanduser()
    expected = dsh_home / "skills" / "xhs-chaijie-dsh"
    print("xhs-chaijie-dsh doctor")
    print(f"Python: {platform.python_version()} ({sys.executable})")
    print(f"Current bundle: {root}")
    print(f"Expected user install: {expected}")
    print(f"Bundle SKILL.md: {'OK' if (root / 'SKILL.md').is_file() else 'MISSING'}")
    print(f"Installed at expected path: {'YES' if expected.resolve() == root.resolve() else 'NO'}")
    print("Runtime checks: browser login, Xiaohongshu access, vision/OCR, and HTML preview are negotiated by DSH per task.")
    return 0 if (root / "SKILL.md").is_file() else 1


if __name__ == "__main__":
    raise SystemExit(main())
