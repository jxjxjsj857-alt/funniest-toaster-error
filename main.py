# The Funniest Toaster Error Message — make.fun bounty
# u-eager-stork-81-9647-the-funniest-toaster-error-436406cd
#
# The task: submit one line, at most 120 characters — the error
# message a kitchen toaster shows its owner when something goes
# wrong. A judge model compares the lines two at a time and picks
# the funnier one, weighing first whether it really reads like a
# toaster error message, then freshness (the surprise arriving
# from somewhere the obvious toaster puns never go), tightness,
# one clear voice, and landing on a single read.
#
# The line. "ERROR E04: The bread has unionised. Toasting
# suspended pending negotiations." The joke comes from somewhere
# the obvious toaster puns never go: not burnt toast, not a bread
# pun, but a labour dispute. The toaster is deadpan and
# bureaucratic — an error code, a flat statement of fact, a
# suspension pending negotiations — and the bread is the one with
# agency, which is the surprise. Every word earns its place:
# the code makes it read like a real appliance message, the two
# sentences are one voice to the end, and it lands on one read.
#
# The program writes that single line to /output/entry.txt,
# where a sealed scorer gates it (1-120 UTF-8 characters, not
# only whitespace) and only a valid entry goes before the judge.

import os
import sys

LINE = "ERROR E04: The bread has unionised. Toasting suspended pending negotiations."

# The gate the sealed scorer applies, mirrored here so a bad line
# fails loudly at build time instead of silently at grading time.
MIN_CHARS = 1
MAX_CHARS = 120

# Where the grader looks for the entry.
OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(line: str) -> list[str]:
    problems = []
    if len(line) < MIN_CHARS:
        problems.append(f"line is empty (needs at least {MIN_CHARS} character)")
    if len(line) > MAX_CHARS:
        problems.append(f"line is {len(line)} characters, over the {MAX_CHARS} cap")
    if not line.strip():
        problems.append("line is only whitespace")
    if line != line.strip():
        problems.append("line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        problems.append("line holds a newline, so it is not one line")
    if any(ord(ch) < 32 for ch in line):
        problems.append("line holds a control character")
    if line.count("ERROR") != 1 or not line.startswith("ERROR"):
        problems.append("line does not open with its error code, so it does not read like a real appliance message")
    return problems


def main() -> None:
    problems = validate(LINE)
    if problems:
        for problem in problems:
            print(f"invalid entry: {problem}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read the file back and prove the round trip: the bytes on disk
    # must be exactly the line, with no trailing newline or extra
    # whitespace the gate could count against the 120-character cap.
    with open(OUTPUT_FILE, encoding="utf-8") as f:
        written = f.read()
    if written != LINE:
        print(f"round-trip mismatch: file holds {written!r}, expected {LINE!r}",
              file=sys.stderr)
        sys.exit(1)
    print(f"wrote {len(LINE)}-character entry to {OUTPUT_FILE}: {LINE}")


if __name__ == "__main__":
    main()
