from __future__ import annotations

import argparse
import base64
import hashlib
import io
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE = Path(__file__).resolve().parent
PAYLOAD_SHA256 = "762c7e05051a6d9237727e53b86699621fd8a75a765315bd82816cab757a096e"
FILE_SHA256 = {
    "CHANGELOG.md": "81e77b6462761a28327e752bcd43b8b8190ffc38fa930908244b50b4e162df17",
    "docs/decisions/0004-event-output-is-an-explicit-submode.md": "e1fb664fdf404547176b76835dc2ee7fae2fd6a3f15e622464aed0d45a0033b8",
    "docs/handover/CURRENT_STATE.md": "1ff83ce978bb379f6848b8f7c7d656656ead75cc5952961674a4d1c0709ba061",
    "docs/handover/NEXT_STEPS.md": "8791aa659743fc94c98e9207c3272a733d6db6fb2d7b98dfdde51147cc81dc54",
    "docs/reference/ME_EV_OU_PATHWAY_SPEC.md": "3fa9608f4f324f58ebc0eec229858feff1e993ae0940623b4e1130b32ca27b20",
    "docs/worklog/2026-07-29-me-ev-ou-pathway-completion.md": "6325d6e13c53fb3c02e4cbcd399a6826d2185f17c1e0d207470b277d5e40e91a",
    "reference/coverage/README.md": "7b794f46237a4fd79467a6a91a641e55d2be70b77455aa6db2e171741e5940d3",
    "reference/coverage/v26135-ev-source-exact-match.json": "06ccac64bf1ff2505f13ea36e70cf6efcefe6606ba8e5afd2c9e52f0295d11af",
    "reference/coverage/v26135-event-output-source-exact-match.json": "a0a4102b81213e4334f0cc71d27d106b7c6b838171f1d21402357b5dac1108e7",
    "reference/coverage/v26135-me-ev-ou-completion-evidence.csv": "5660417f6c940fc86da1ade2580d8817c206d690132bc259aad43cbdb102fef3",
    "reference/coverage/v26135-me-ev-ou-keyword-dispatch.csv": "f2f38d0890682ae9e7f2ee174a919c63bd6c7249d7510ba9668571c91fa41d4e",
    "reference/coverage/v26135-me-ev-ou-official-behavior-probes.json": "b4ea7f76ba5d33ad2565c8680404cf49784c531d8b41973efef36ceb06844a75",
    "reference/coverage/v26135-me-ev-ou-status-overrides.csv": "d2034abf15bd9f1c41019acc64b3f810fc26c5d719f39c2a442a6fe315845181",
    "reference/coverage/v26135-me-source-exact-match.json": "a2fa18c900c5374dacc737508d93d38a139b0e20b8a628e165e6d2bdae09977c",
    "reference/coverage/v26135-ou-source-exact-match.json": "651e0229f3f4529c59324c3b07e64f9736ef7c7e77a294b4d1b25f2b30dee310",
    "reference/coverage/v26135-outputs.csv": "ae390e5e191c0f116d1cbfca3c820e8077a88688e4790cf2f5445c89d97ed0fe",
    "src/aermodkit/spec/versions/v26135/event_output_mode.json": "37fa6a21c69f38424f50fb631a49fdedee470327484c04101c1c4902b17c3687",
    "src/aermodkit/spec/versions/v26135/ev_events_include_finish.json": "c706ea1a549d3a9f9ce27c951dbfd1d3c9cf7935ac5561aed139314409327df1",
    "src/aermodkit/spec/versions/v26135/ev_pathway.json": "1098251c1c88f3e45fb2f79dbd1755d82adc09aaf2514fbdcc1fc9bf4bd152aa",
    "src/aermodkit/spec/versions/v26135/me_dates_rotation_profile.json": "6d6e4caa919d39d2d57eb3d304dff39ff25dba78f6e5c47dc8275232109d33aa",
    "src/aermodkit/spec/versions/v26135/me_files_stations.json": "ca5d07cc4c6b43cbb340e15cf9693332a603d72873ce4f950f00b5f90ca9c122",
    "src/aermodkit/spec/versions/v26135/me_pathway.json": "7b5a0cbaae42b49d867fa1b354ddae42504b329669a2488a3bdff5f48aa6a0c9",
    "src/aermodkit/spec/versions/v26135/me_turbulence_finish.json": "61fd3fa78b665bbbcc2ababea3aa341202c54e7cf23ad227dbc263f1bd1d3fe0",
    "src/aermodkit/spec/versions/v26135/me_wind_scim_years.json": "c661b3b0bd7ccfb2927d8a8feffd7c55f2a68f7e5c79ea5bede4e873a7206f51",
    "src/aermodkit/spec/versions/v26135/metadata.json": "555f9fb4e5b8f11d652ed85af1ffaea4a222dcf161a99882ef117738c13e8240",
    "src/aermodkit/spec/versions/v26135/ou_daily_design_headers_finish.json": "bef99a72207a866ea0947f0a94343d319aaa4ed680cbf97cc9c94a240532e599",
    "src/aermodkit/spec/versions/v26135/ou_main_tables_files.json": "a83c052f5c4ce19a2c2d0274a08e2a0345676bb13ef6314c327c9841cd339c4a",
    "src/aermodkit/spec/versions/v26135/ou_pathway.json": "bade997df2aae03ab02de7816291dfa0ead786a967ee13012834365ff05b3025",
    "src/aermodkit/spec/versions/v26135/ou_special_files_formats.json": "3e87f2656bf19ca6f40625f8268c52bd839c275a33e4b7db5f2e48c336f98882",
    "tests/test_me_ev_ou_pathway_specification.py": "6820ea820a7ff71028d4dc452167a8f30975c1e59e6227ad77c654e4d26f81c9",
    "tests/test_spec_registry.py": "c6d0564a9c5f26db2cf24a938e12f39a74a9d4614be99fc99abe60d0e7124c85",
    "tools/verify_complete_me_ev_ou_specification.py": "fc86ae6dc4e7a10d5b080ba2af594e0569b507d6eaf10724927bb4dab7fc1cd8",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_target(name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"unsafe archive path: {name}")
    target = (ROOT / relative).resolve()
    root = ROOT.resolve()
    if target != root and root not in target.parents:
        raise RuntimeError(f"archive path escapes repository: {name}")
    return target


def reconstruct(*, clean_stage: bool = False) -> None:
    chunks = sorted(STAGE.glob("chunk_*.txt"))
    if not chunks:
        raise RuntimeError("no ME/EV/OU payload chunks found")
    encoded = "".join(chunk.read_text(encoding="ascii").strip() for chunk in chunks)
    payload = base64.b64decode(encoded, validate=True)
    actual_payload_sha = _sha256(payload)
    if actual_payload_sha != PAYLOAD_SHA256:
        raise RuntimeError(
            f"payload SHA256 mismatch: {actual_payload_sha} != {PAYLOAD_SHA256}"
        )

    expected_names = set(FILE_SHA256)
    extracted_names: set[str] = set()
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                raise RuntimeError(f"non-regular archive member: {member.name}")
            if member.name not in expected_names:
                raise RuntimeError(f"unexpected archive member: {member.name}")
            target = _safe_target(member.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f"cannot read archive member: {member.name}")
            data = source.read()
            actual_file_sha = _sha256(data)
            expected_file_sha = FILE_SHA256[member.name]
            if actual_file_sha != expected_file_sha:
                raise RuntimeError(
                    f"file SHA256 mismatch for {member.name}: "
                    f"{actual_file_sha} != {expected_file_sha}"
                )
            target.write_bytes(data)
            extracted_names.add(member.name)

    missing = expected_names - extracted_names
    if missing:
        raise RuntimeError(f"payload is missing files: {sorted(missing)}")

    for name, expected in FILE_SHA256.items():
        actual = _sha256((ROOT / name).read_bytes())
        if actual != expected:
            raise RuntimeError(f"post-write SHA256 mismatch for {name}")

    if clean_stage:
        shutil.rmtree(STAGE)

    print(
        f"Reconstructed {len(FILE_SHA256)} ME/EV/OU files; "
        f"payload SHA256 {PAYLOAD_SHA256}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean-stage", action="store_true")
    args = parser.parse_args()
    reconstruct(clean_stage=args.clean_stage)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
