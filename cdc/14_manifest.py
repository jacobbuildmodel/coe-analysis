"""
14_manifest.py -- md5 of every file the seal fixes.

  python3 cdc/14_manifest.py                  print the list
  python3 cdc/14_manifest.py --seal           write SEAL_MANIFEST.md (draft header)
  python3 cdc/14_manifest.py --seal --final   the same, with the seal header
  python3 cdc/14_manifest.py --check          compare with SEAL_MANIFEST.md
                                              (exit 1 on a difference)

Hashes are of the bytes in the working tree; the repository forces LF on .py,
.md, .txt and .sh, so they equal the committed blobs. Standard library only.
"""
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
FILES = ["THESIS.md", "ALTERNATIVES.md", "events.csv", "office/COVERAGE.txt",
         "00_coverage.py", "01_download.py", "10_load.py", "11_tests.py",
         "12_alternatives.py", "14_manifest.py", "cdclib.py", "requirements.txt",
         "run_all.sh", "tests/make_fixtures.py", "tests/test_pipeline.py"]
HEAD = """# SEAL MANIFEST: cdc piece

{status}

The md5 of every file the seal fixes. Paths are relative to `cdc/`.
Regenerate with `python3 cdc/14_manifest.py --seal` and compare with
`python3 cdc/14_manifest.py --check`.

```
"""
DRAFT = ("**DRAFT.** THESIS.md is not sealed. This file is rewritten in the seal "
         "commit, which then adds only it.")
FINAL = "Taken in the seal commit, which changes this file and nothing else."


def listing():
    return [(hashlib.md5((HERE / f).read_bytes()).hexdigest(), f) for f in FILES]


def main():
    lines = [f"{h}  {f}" for h, f in listing()]
    if "--seal" in sys.argv:
        status = FINAL if "--final" in sys.argv else DRAFT
        (HERE / "SEAL_MANIFEST.md").write_text(
            HEAD.format(status=status) + "\n".join(lines) + "\n```\n",
            encoding="ascii", newline="\n")
        print("wrote SEAL_MANIFEST.md")
        return 0
    if "--check" in sys.argv:
        text = (HERE / "SEAL_MANIFEST.md").read_text(encoding="ascii")
        bad = [line for line in lines if line not in text]
        for line in bad:
            print("DIFFERS  " + line)
        print("manifest check: " + ("FAIL" if bad else "OK"))
        return 1 if bad else 0
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
