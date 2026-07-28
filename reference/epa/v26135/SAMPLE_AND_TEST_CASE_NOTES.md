# AERMOD v26135 official sample and test-case inventory

## Cryptographic provenance

| Asset | Size (bytes) | SHA256 | ZIP entries |
|---|---:|---|---:|
| `AERMOD_Sample_Run.zip` | 95949615 | `3ee2180fd0ad9c954350bbbe3ca3567ce02df91a2869cec5f6c45178bff32da0` | 28 |
| `aermod_test_cases.zip` | 488669681 | `fc5ad71de5ba64a50ed72d4d19c45b32ad14447353b1216c3d1f420ce84beff8` | 1931 |

Both archives were downloaded from canonical EPA SCRAM URLs by GitHub Actions run `30391161469`. The original large ZIPs were deleted before artifact upload; only hashes, archive indexes, and selected text fixtures were retained.

## Official sample run

The sample archive contains 28 entries under `SampleRun/` and demonstrates the complete preprocessing chain:

- AERMAP input plus original receptor/source/domain/map outputs;
- AERMET stage 1 and stage 2 inputs plus original surface/profile outputs;
- AERMOD input, hourly emissions, main output, summary output, and error output;
- the official sample-run instruction PDF and explanatory readme.

The Git repository stores the full entry index in `archive-index/sample-run.csv`. The sample is a workflow example, not a comprehensive regulatory regression suite.

## Official AERMOD test archive

The archive contains 1,931 entries. It provides three 53-input model configurations:

1. `aermet24142_aermod24142` — previous AERMET and previous AERMOD baseline;
2. `aermet24142_aermod26135` — isolates the AERMOD update while holding meteorology constant;
3. `aermet26135_aermod26135` — current AERMET/AERMOD configuration.

Each configuration contains the same 53 AERMOD input decks, associated include and meteorological files, expected outputs, plot files, post files, and test-run scripts. Three additional directories contain 429 comparison PNGs across the version combinations. The archive also includes R scripts for processing and comparison plus the official test instructions document.

The full archive index is retained in GitHub Actions artifact `8701201873` (digest `sha256:0c237c57eefcdde1d4ab05495bf8260539d1d76d75de8e9fecf712bb38e5a291`) rather than committed to Git. A configuration-level summary is stored in `reference/coverage/v26135-test-configuration-summary.csv`.

## Current v26135 fixture registry

`reference/coverage/v26135-official-fixtures.csv.gz` decompresses to a UTF-8 CSV that records the 53 current `aermet26135_aermod26135` input decks with:

- title and pollutant;
- MODELOPT and averaging-time settings;
- pathways and source types;
- inferred capability tags;
- include/external-file references;
- declared output paths;
- expected main-output filename when matched from the official archive.

`reference/coverage/v26135-official-keyword-fixture-coverage.csv` records how many of the 53 current official decks exercise each observed pathway/keyword pair.

## Test suite execution

The official Windows script runs every `*.inp` file in the configuration's `inputs` directory with `aermod.exe`, moves generated `*.out` files to `Outputs`, and searches all outputs for `UN-Successfully`. It expects the official executable to be placed in the `inputs` directory.

The archive also includes `aermod_run.sh` for Linux. AERMODKit must preserve the official files and build a separate deterministic comparison harness rather than modifying the supplied suite in place.

## Current limitations

- The initial compact artifact retained text files in archive order and therefore did not preserve every current-version meteorological/output file. A dedicated current-fixture snapshot workflow has been added to retain only `aermet26135_aermod26135/inputs`, `meteorology`, and `Outputs` for numerical regression.
- Fixture tags are mechanically derived from input records and must be reviewed before being treated as semantic classifications.
- Matching expected main output by input stem is reliable for most decks, but declared output files remain the authoritative source for auxiliary outputs.
- Passing the official test suite is necessary but not sufficient for complete AERMOD semantic support.
