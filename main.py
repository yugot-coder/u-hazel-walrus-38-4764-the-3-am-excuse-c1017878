"""The 3 AM Excuse — make.fun entry (program/v1).

Writes one fixed excuse line to /output/entry.txt: a hardware wallet
refusing to sign a transaction at 3 AM. Pure Python 3 standard
library, no network, fully deterministic — the same bytes on every
run. The gate needs 1-200 UTF-8 characters, one line, not blank.
"""

import hashlib
import os
import sys

ENTRY = (
    "Every 3 AM signature in my memory ends with 'why did I do that' "
    "by 9 AM. I'm breaking the cycle \u2014 ask the sun, not me."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def check(text):
    """Return an error string if text breaks the gate, else None."""
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        return "entry must be %d-%d characters, got %d" % (
            MIN_CHARS,
            MAX_CHARS,
            len(text),
        )
    if not text.strip():
        return "entry must not be whitespace only"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    text.encode("utf-8")
    return None


def main():
    problem = check(ENTRY)
    if problem is not None:
        raise SystemExit(problem)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)

    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != ENTRY.encode("utf-8"):
        raise SystemExit("read-back mismatch: bytes on disk differ")

    print(
        "wrote %s (%d chars, sha256 %s)"
        % (OUTPUT_PATH, len(ENTRY), hashlib.sha256(written).hexdigest())
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
