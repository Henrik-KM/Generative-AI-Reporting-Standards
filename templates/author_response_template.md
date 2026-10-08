# Author response to the reporting checklist

**Paper title:** _(fill in)_

**Version and date:** _(fill in)_

**Corresponding author:** _(fill in)_

**Code or data release:** _(URL, DOI, or repository tag/commit)_

**Declared workflow, cohort and endpoint:** _(identify the candidate population, physical evidence level and comparison)_

**Checklist format:** `1.0.0-draft` on the development branch; use the archived 0.2.0 form for unchanged historical records.

For each category, supply actual procedures and values with exact source locations, or identify unavailable information. Use `not_performed` only for an applicable operation known not to have been undertaken, explaining the consequence for the claim. Use `not_applicable` only when the operation is absent from the workflow, with an applicability reason. Do not infer non-performance from missing reporting. Retain nulls for unavailable quantities. Attach the completed record to the submission, with a short main-text reference; a list of states alone is not an operational author response. The Brorsson development example shows concrete responses and explicit gaps.

## Core response categories

| ID | Item | Disclosure state | Response | Exact source location and public artefact |
|---|---|---|---|---|
| D1 | Data |  |  |  |
| S1 | Splits |  |  |  |
| M1 | Inputs/Model |  |  |  |
| T1 | Training |  |  |  |
| G1 | Generation |  |  |  |
| E1 | Metrics |  |  |  |
| B1 | Baselines and ablations |  |  |  |
| F1 | Feasibility |  |  |  |
| R1 | Reproducibility |  |  |  |

## Context-dependent reporting items

| ID | Item | Disclosure state | Response | Exact source location and public artefact |
|---|---|---|---|---|
| CL1 | Closed-loop/UQ |  |  |  |
| C1 | Compute footprint |  |  |  |
| GOV1 | Governance and ethics |  |  |  |

## Optional key-number summary

| ID | Item | Disclosure state | Response | Exact source location and public artefact |
|---|---|---|---|---|
| K1 | Key-number summary |  |  |  |

`N_gen=...; stagewise pass rates=...; validated outcomes=...; evaluator budget=...; closed loop=R rounds × N_eval evaluations (where used); training cost=...; inference cost=...; tag=repo@vX.Y`

The compact format is optional; claim-relevant counts are not. Use the stage ledger to separate candidate populations, evaluator calls, failed calls and repeats. Nominal rounds multiplied by a batch size do not establish the budget where runs are pooled or failures, repeats and variable batches occur. Inference throughput belongs under Generation, not Training.
