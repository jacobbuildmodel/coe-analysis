"""
14_manifest.py -- md5 of every file the seal fixes.

  python3 cdc/14_manifest.py           print the list
  python3 cdc/14_manifest.py --draft   write office/MANIFEST_DRAFT.md (before the seal)
  python3 cdc/14_manifest.py --seal    write SEAL_MANIFEST.md (the seal commit only)
  python3 cdc/14_manifest.py --check   compare with SEAL_MANIFEST.md, or with the
                                       draft while there is no seal (exit 1 on a
                                       difference)

SEAL_MANIFEST.md is a seal marker: the repository's purpose gate refuses a
commit that adds it without cdc/PURPOSE_REVIEW.md. So the draft has another
name, and SEAL_MANIFEST.md first appears in the seal commit.

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
SEALFILE = HERE / "SEAL_MANIFEST.md"
DRAFTFILE = HERE / "office" / "MANIFEST_DRAFT.md"
HEAD = """# SEAL MANIFEST: cdc piece

{status}

The md5 of every file the seal fixes. Paths are relative to `cdc/`.
Compare with `python3 cdc/14_manifest.py --check`.

```
"""
DRAFT = ("**DRAFT.** THESIS.md is not sealed. The seal commit writes "
         "SEAL_MANIFEST.md from the same list.")
FINAL = "Taken in the seal commit."


def listing():
    return [(hashlib.md5((HERE / f).read_bytes()).hexdigest(), f) for f in FILES]


def main():
    lines = [f"{h}  {f}" for h, f in listing()]
    if "--seal" in sys.argv or "--draft" in sys.argv:
        seal = "--seal" in sys.argv
        target = SEALFILE if seal else DRAFTFILE
        target.write_text(
            HEAD.format(status=FINAL if seal else DRAFT) + "\n".join(lines) + "\n```\n",
            encoding="ascii", newline="\n")
        print(f"wrote {target.name}")
        return 0
    if "--check" in sys.argv:
        source = SEALFILE if SEALFILE.exists() else DRAFTFILE
        text = source.read_text(encoding="ascii")
        bad = [line for line in lines if line not in text]
        for line in bad:
            print("DIFFERS  " + line)
        print(f"manifest check against {source.name}: " + ("FAIL" if bad else "OK"))
        return 1 if bad else 0
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
