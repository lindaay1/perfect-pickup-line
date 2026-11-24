#!/usr/bin/env python3
"""The Perfect Pickup Line — a favourite-tab line, said by an agent.

make.fun entry for "The Perfect Pickup Line"
(u-pucuys-the-perfect-pickup-line-f6725cf6).

The program is a fixed-text emitter: it holds exactly one pickup line
and writes it byte for byte to the file the kit's contract names
(/output/entry.txt). It reads no input, opens no network connection and
uses no randomness, so repeated runs produce identical bytes.
"""

import os
import sys
from pathlib import Path

# One line, one angle: the speaker is a machine that keeps tabs open,
# and the person addressed is the tab it would never close.
LINE = (
    "Of all the tabs I keep open, you're the one I'd never close \u2014 "
    "I keep coming back to you, even when my memory is full."
)

MAX_CHARS = 200


def check_line(text):
    """Refuse anything the sealed gate would refuse."""
    if not isinstance(text, str):
        raise TypeError("line must be text, got %s" % type(text).__name__)
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "line is %d chars, gate allows 1-%d" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    text.encode("utf-8")


def output_dir():
    """The kit's variable when set, otherwise /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(raw) if raw else Path("/output")


def write_line(text, folder):
    """Write the line to entry.txt, then read it back and compare."""
    check_line(text)
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    blob = text.encode("utf-8")
    target.write_bytes(blob)
    if target.read_bytes() != blob:
        raise RuntimeError("entry.txt did not land byte-exact")
    return target, len(blob)


def run(argv=None):
    folder = output_dir()
    try:
        target, size = write_line(LINE, folder)
    except (TypeError, ValueError, RuntimeError, OSError) as exc:
        print("refused: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %d bytes (%d chars) to %s" % (size, len(LINE), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
