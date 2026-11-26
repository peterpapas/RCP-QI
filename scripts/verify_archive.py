"""Verify immutable experiment artifact bytes against the closeout inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "manifest.json"
INVENTORY = ROOT / "research" / "archive" / "artifact_integrity.json"
CATALOGUE = ROOT / "research" / "archive" / "RCPQI_THEOREM_CATALOGUE.md"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def artifact_paths() -> list[str]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    paths = set(manifest.get("processed", []))
    for experiment in manifest["experiments"]:
        for field in ("raw", "processed", "figures"):
            paths.update(experiment.get(field, []))
    for relative in paths:
        target = (ROOT / relative).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            raise ValueError(f"invalid or missing manifest artifact: {relative}")
    return sorted(paths)


def current_inventory() -> dict:
    return {
        "schema_version": 1,
        "scope": "Manifest-indexed historical raw, processed and figure artifacts; theory files are Git-versioned separately.",
        "manifest_sha256": digest(MANIFEST),
        "artifacts": {
            relative: {"bytes": (ROOT / relative).stat().st_size, "sha256": digest(ROOT / relative)}
            for relative in artifact_paths()
        },
    }


def verify_theorem_coverage() -> int:
    catalogue = CATALOGUE.read_text(encoding="utf-8")
    theorem_names = {
        match.group(1)
        for module in (ROOT / "formal" / "lean" / "RCPQI").glob("*.lean")
        for match in re.finditer(r"^theorem\s+([A-Za-z_][A-Za-z_0-9]*)", module.read_text(encoding="utf-8"), re.MULTILINE)
    }
    missing = sorted(name for name in theorem_names if f"RCPQI.{name}" not in catalogue)
    if missing:
        raise ValueError(f"Lean theorems absent from closeout catalogue: {missing}")
    return len(theorem_names)


def verify_local_links() -> int:
    documents = [ROOT / "README.md", *(ROOT / "research" / "archive").glob("*.md")]
    checked = 0
    for document in documents:
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if link.startswith(("https://", "http://", "#")):
                continue
            target = (document.parent / link.split("#", 1)[0]).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                raise ValueError(f"broken local link in {document.relative_to(ROOT)}: {link}")
            checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-inventory", action="store_true", help="Create the initial closeout index once")
    args = parser.parse_args()
    theorem_count = verify_theorem_coverage()
    current = current_inventory()
    local_link_count = verify_local_links()
    if args.write_inventory:
        if INVENTORY.exists():
            raise SystemExit(f"Refusing to overwrite immutable inventory: {INVENTORY}")
        INVENTORY.parent.mkdir(parents=True, exist_ok=True)
        INVENTORY.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Recorded {len(current['artifacts'])} artifact digests")
        return
    if not INVENTORY.is_file():
        raise SystemExit(f"Missing closeout inventory: {INVENTORY}")
    expected = json.loads(INVENTORY.read_text(encoding="utf-8"))
    if current != expected:
        missing = sorted(set(expected.get("artifacts", {})) - set(current["artifacts"]))
        added = sorted(set(current["artifacts"]) - set(expected.get("artifacts", {})))
        changed = sorted(
            key
            for key in set(current["artifacts"]) & set(expected.get("artifacts", {}))
            if current["artifacts"][key] != expected["artifacts"][key]
        )
        raise SystemExit(f"Archive integrity mismatch: missing={missing}, added={added}, changed={changed}, manifest_changed={current['manifest_sha256'] != expected.get('manifest_sha256')}")
    print(f"Verified {len(current['artifacts'])} immutable artifact digests, manifest SHA-256, {theorem_count} Lean theorem entries and {local_link_count} local links")


if __name__ == "__main__":
    main()
