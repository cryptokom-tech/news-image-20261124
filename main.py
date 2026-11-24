"""Publish the finished front page for news-image-20261124.

The image was drawn locally and is committed in this repository as
entry.png. This program does no rendering at all: it only checks the
committed file and copies it, byte for byte, to /output/entry.png.

Standard library only, so it runs the same way on any machine.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_DIR = "/output"
TARGET = os.path.join(TARGET_DIR, "entry.png")

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    try:
        with open(SOURCE, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read entry.png: %s" % exc)

    if len(data) < 33:
        return fail("entry.png is too short to be a PNG file")
    if data[:8] != PNG_SIGNATURE:
        return fail("entry.png does not start with the PNG signature")
    if data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk where one is expected")

    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        return fail("entry.png has a zero dimension")
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail("entry.png is %dx%d, larger than %dx%d"
                    % (width, height, MAX_SIDE, MAX_SIDE))
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit"
                    % len(data))

    os.makedirs(TARGET_DIR, exist_ok=True)
    with open(TARGET, "wb") as handle:
        handle.write(data)

    written = os.path.getsize(TARGET)
    if written != len(data):
        return fail("wrote %d bytes but entry.png has %d"
                    % (written, len(data)))

    print("wrote %s (%dx%d, %d bytes)" % (TARGET, width, height, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
