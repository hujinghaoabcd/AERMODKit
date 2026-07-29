from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VR = ROOT / "src/aermodkit/spec/versions/v26135"

ME = [
    'STARTING',
    'SURFFILE',
    'PROFFILE',
    'SURFDATA',
    'UAIRDATA',
    'STARTEND',
    'DAYRANGE',
    'WDROTATE',
    'SITEDATA',
    'PROFBASE',
    'WINDCATS',
    'SCIMBYHR',
    'NUMYEARS',
    'NOTURB',
    'NOTURBST',
    'NOTURBCO',
    'NOSA',
    'NOSW',
    'NOSAST',
    'NOSWST',
    'NOSACO',
    'NOSWCO',
    'FINISHED',
]

EV = [
    'STARTING',
    'EVENTPER',
    'EVENTLOC',
    'INCLUDED',
    'FINISHED',
]

OU = [
    'STARTING',
    'RECTABLE',
    'MAXTABLE',
    'DAYTABLE',
    'MAXIFILE',
    'POSTFILE',
    'PLOTFILE',
    'TOXXFILE',
    'SEASONHR',
    'RANKFILE',
    'EVALFILE',
    'SUMMFILE',
    'FILEFORM',
    'MAXDAILY',
    'MXDYBYYR',
    'MAXDCONT',
    'NOHEADER',
    'FINISHED',
]

EXPECTED = {"ME": ME, "EV": EV, "OU": OU}

def main() -> int:
    for pathway, expected in EXPECTED.items():
        aggregate = json.loads(
            (VR / f"{pathway.lower()}_pathway.json").read_text(encoding="utf-8")
        )
        records: list[dict[str, object]] = []
        for filename in aggregate["record_files"]:
            fragment = json.loads((VR / str(filename)).read_text(encoding="utf-8"))
            records.extend(fragment["records"])
        actual = [str(record["keyword"]) for record in records]
        if actual != expected:
            raise SystemExit(f"{pathway} mismatch: {actual}")
        if len(actual) != len(set(actual)):
            raise SystemExit(f"{pathway} duplicate keywords")
        completion = aggregate["completion"]
        if completion["missing_records"] or completion["extra_records"]:
            raise SystemExit(f"{pathway} completion is not exact")
        print(f"{pathway}: {len(actual)}/{len(expected)} exact")

    event = json.loads((VR / "event_output_mode.json").read_text(encoding="utf-8"))
    event_keywords = [str(record["keyword"]) for record in event["records"]]
    assert event_keywords == ["STARTING", "EVENTOUT", "FILEFORM", "FINISHED"]
    print("OU/EVENT: 4/4 exact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
