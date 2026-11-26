"""Fetch optional third-party SAT Competition inputs from their original host.

The files are intentionally absent from the public repository. Verify every
download before moving it into the local benchmark directory.
"""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "benchmarks" / "instances" / "satcomp2025"
SOURCES = {
    "Break_12_50.xml.cnf.xz": (
        "0e1d562093d5f4fc9013cf4a14a03f70",
        "e56a8b6d9099fab4950ca38c9c759958d9d7c31ca8bc0ea78fad5238d7d67382",
    ),
    "s38417.cnf.xz": (
        "09cd83e233380d0ba1fc56cee88367b1",
        "03d81a900d1f6481daec12e2539de6139cc1579d7fab571ceac02ec68f8b6e99",
    ),
}


def digest(path: Path) -> str:
    hash_ = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hash_.update(block)
    return hash_.hexdigest()


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for name, (source_hash, expected_sha256) in SOURCES.items():
        destination = TARGET / name
        if destination.exists():
            if digest(destination) != expected_sha256:
                raise ValueError(f"existing benchmark checksum mismatch: {name}")
            print(f"verified existing {name}")
            continue
        url = f"https://benchmark-database.de/file/{source_hash}?context=cnf"
        with tempfile.NamedTemporaryFile(dir=TARGET, prefix="download-", delete=False) as temp:
            temporary = Path(temp.name)
            try:
                with urlopen(Request(url, headers={"User-Agent": "RCP-QI-reproducibility/1.0"}), timeout=120) as source:
                    for block in iter(lambda: source.read(1024 * 1024), b""):
                        temp.write(block)
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
        if digest(temporary) != expected_sha256:
            temporary.unlink(missing_ok=True)
            raise ValueError(f"downloaded benchmark checksum mismatch: {name}")
        temporary.replace(destination)
        print(f"downloaded and verified {name}")


if __name__ == "__main__":
    main()
