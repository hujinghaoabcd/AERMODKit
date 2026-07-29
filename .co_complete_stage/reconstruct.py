"""Reconstruct and verify the temporary CO-completion payload."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import tarfile
from pathlib import Path

EXPECTED_TAR_SHA256 = "1a3ae9a7d6b62fb5550ef51829cecd79ad543c0e23e277700dc0d4260f13af89"


def reconstruct(*, clean: bool) -> None:
    stage = Path(".co_complete_stage")
    encoded = "".join(path.read_text() for path in sorted(stage.glob("chunk_*.txt")))
    payload = base64.b64decode(encoded, validate=True)
    actual_tar = hashlib.sha256(payload).hexdigest()
    if actual_tar != EXPECTED_TAR_SHA256:
        raise SystemExit(f"payload SHA256 mismatch: {actual_tar}")

    archive = stage / "payload.tar.gz"
    archive.write_bytes(payload)
    with tarfile.open(archive, "r:gz") as handle:
        for member in handle.getmembers():
            target = Path(member.name)
            if target.is_absolute() or ".." in target.parts:
                raise SystemExit(f"unsafe archive path: {member.name}")
        handle.extractall(".")

    manifest_path = Path("_co_complete_manifest.json")
    manifest: dict[str, str] = json.loads(manifest_path.read_text())
    for relative, expected in manifest.items():
        path = Path(relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"file SHA256 mismatch: {relative}: {actual}")
    manifest_path.unlink()

    if clean:
        shutil.rmtree(stage)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    reconstruct(clean=args.clean)


if __name__ == "__main__":
    main()
