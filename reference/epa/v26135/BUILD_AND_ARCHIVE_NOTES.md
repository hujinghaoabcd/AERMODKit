# AERMOD v26135 official source archive and build notes

## Provenance

- Authority: U.S. EPA Support Center for Regulatory Atmospheric Modeling (SCRAM)
- Canonical asset: `aermod_source.zip`
- Canonical URL: `https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_source.zip`
- HTTP last-modified: `Thu, 09 Jul 2026 19:44:32 GMT`
- HTTP ETag: `"a4ac7-65632da69ce02"`
- Downloaded by GitHub Actions run: `30391161469`
- Artifact ID: `8700977820`
- Artifact digest: `sha256:1bcdb91ccec3572126da48dff67f3924628ff394530270094d16b8a2278201ca`
- Official ZIP size: `674503` bytes
- Official ZIP SHA256: `5092c1d68b77d9407c9f67d497b440a79d2ee746f9ed6515a63ad4a5b11cd8ed`
- ZIP entries: `32` total: one directory, 29 Fortran source files, and two Windows batch build scripts.

The ZIP SHA256 was computed on the GitHub-hosted runner and independently recomputed after downloading the artifact into the working container. The values matched.

## Archive layout

The archive root is `aermod_source_v26135/`. A complete entry-level inventory with sizes, CRC32 values, ZIP timestamps, and compression metadata is stored in `archive-index/aermod-source.csv`.

The source contains:

- one main program;
- 11 modules;
- 528 subroutines;
- 26 functions;
- 566 program units in total, based on declaration-level indexing.

A per-file summary is stored in `reference/coverage/v26135-source-unit-summary.csv`. The full declaration index is stored as `reference/coverage/v26135-source-units.csv.gz` to keep the Git repository compact. It decompresses to a normal UTF-8 CSV. Its line ranges end immediately before the next program-unit declaration and are intended as traceability locations, not as a replacement for Fortran-aware parsing.

## Official GNU Fortran build

The official `gfortran-aermod.bat` defines:

```text
COMPILE_FLAGS = -fbounds-check -Wuninitialized -O2 -static
LINK_FLAGS    = -static -O2
```

Compilation order:

```text
modules.f grsm.f aermod.f setup.f coset.f soset.f reset.f meset.f
ouset.f inpsum.f metext.f iblval.f siggrid.f tempgrid.f windgrid.f
calc1.f calc2.f prise.f arise.f prime.f sigmas.f pitarea.f uninam.f
output.f evset.f evcalc.f evoutput.f rline.f bline.f
```

The object files are linked in the same order to produce `aermod.exe`.

The supplied script is a Windows batch file. The same compiler flags and unit order can be translated to a POSIX shell command, but that translation is an AERMODKit reproducibility aid rather than an EPA-distributed script.

## Official Intel oneAPI build

The official `intel_ifx_aermod.bat` defines:

```text
COMPILE_FLAGS = /O2 /Qipo /Qprec-div
LINK_FLAGS    = /O2 /Qipo /Qprec-div
```

It compiles the same 29 source units with `ifx /compile-only` and links them with `/exe:aermod.exe`.

## Pathway dispatch confirmed from source

| Pathway | Dispatcher | File | Source lines |
|---|---|---|---:|
| CO | `COCARD` | `coset.f` | 1–1447 |
| SO | `SOCARD` | `soset.f` | 1–1008 |
| RE | `RECARD` | `reset.f` | 1–207 |
| ME | `MECARD` | `meset.f` | 1–307 |
| OU | `OUCARD` | `ouset.f` | 1–210 |
| EV | `EVCARD` | `evset.f` | 1–175 |
| OU in event mode | `EV_OUCARD` | `evset.f` | 776–848 |

All 120 currently inventoried primary records were located in these dispatchers. Exact branch lines and called handler candidates are stored in `reference/coverage/v26135-keyword-dispatch.csv`.

## Distribution policy

The EPA source archive is not committed to this Git repository. The repository stores its canonical URL, metadata, cryptographic hash, archive index, source-unit index, and derived traceability maps. A short-lived GitHub Actions artifact retains the source snapshot for audit and handoff.

The large sample-run and test-case ZIPs are handled similarly: download, hash, index, extract a bounded set of text fixtures, and discard the original large archive before artifact upload.

## Independent GNU Fortran build verification

AERMODKit reproduced the official GNU Fortran build in a Linux working container using GNU Fortran 14.2.0. The exact EPA compile flags, link flags, source order, and object order were retained.

Result:

- compilation: success for all 29 Fortran units;
- link: success;
- output: statically linked x86-64 ELF executable;
- executable size: `4779888` bytes;
- executable SHA256: `e8313b430047472ccf9a6cbd49b573c8e638aafaca25805e42c0f9c7a14341a5`;
- `ldd` result: not a dynamic executable;
- no-argument smoke invocation: exit code `0`, with the expected message that the runstream input file could not be opened;
- compiler warnings: 33 `-Wuninitialized`/`-Wmaybe-uninitialized` diagnostics.

The executable hash is a reproducibility record for this compiler and environment, not an EPA-published reference hash. Compiler version, operating system, optimization, and linker implementation can change executable bytes without changing model semantics.

The compiler warnings originate in the official source and are preserved as audit findings. AERMODKit does not modify EPA numerical code merely to silence warnings. Any future source patch must be separately documented, justified, and tested against official cases.
