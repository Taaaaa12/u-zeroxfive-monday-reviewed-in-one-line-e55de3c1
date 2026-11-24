"""Monday, Reviewed in One Line.

Writes a single-line review of the entrant's own Monday to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

The line is fixed text: the grader runs the program twice and requires
byte-identical output, so there is no randomness, no clock, no network
and no input data. The program only validates the line against the
competition gate (UTF-8, 1 to 200 characters, not only whitespace,
exactly one line) and writes it.
"""

import os
import sys

# The review. Written as a one-star review: a concrete Monday (a meeting
# about the meeting, an inbox reply-all) with the joke landing on the
# last clause, and nothing else.
REVIEW = (
    "One star: Monday opened with a meeting about the meeting, "
    "my inbox hit reply-all, and by 9 a.m. even my coffee had "
    "filed for overtime."
)

MAX_CHARS = 200


def validate(text):
    """Check the line against the competition gate."""
    if not isinstance(text, str):
        raise ValueError("review must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "review must be 1 to 200 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("review must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("review must be exactly one line")
    text.encode("utf-8")  # must be valid UTF-8
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    line = validate(REVIEW)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    # Read back what was written and confirm it is exactly the line
    # the gate will see, so a partial write can never pass silently.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line + "\n":
        raise ValueError("read-back mismatch in %s" % path)
    print("wrote %s (%d characters)" % (path, len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
