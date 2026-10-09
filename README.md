# A reporting protocol for generative materials design

Separating the few candidates that merit costly validation from the many that do not has become a central challenge in materials design. Generative models can now propose thousands to millions of molecules, polymers, crystals, or frameworks, whereas every DFT calculation, simulation, synthesis, or measurement needed to substantiate a claim remains expensive. The scientifically relevant outcome of a study is therefore not the generated set itself, but the much smaller subset that survives filtering and evaluation. This means that whether a reported advance reflects a better model, a different filter, a more permissive evaluator, or simply a larger validation budget can only be judged from the complete workflow.

To this end, this repository provides a reporting protocol that treats the complete workflow, from data and candidate generation through filters and evaluators to validated outcomes, as the unit of reporting. In practice, the protocol consists of eight steps that together complete a checklist and a stage ledger, which follows candidates from proposal to validated outcome. It does not prescribe a preferred pipeline, and a complete record does not by itself establish that the chosen methods, thresholds, or conclusions are appropriate; rather, it makes the information needed to judge them available.

## Repository contents

- [checklist.md](checklist.md) gives the protocol (version 1.0.0) with its eight steps and stable machine-readable identifiers.
- [templates](templates) contains an author-record template in Markdown, LaTeX, and PDF.
- [schema/reporting-checklist.schema.json](schema/reporting-checklist.schema.json) defines the machine-readable format for author records, records completed from publications, and retrospective audits, including an optional structured stage ledger.
- [examples](examples) contains two worked records completed from publications, for the MatterGen bulk-modulus campaign and for an active-learning study of high-entropy oxygen carriers, together with two retrospective audits.
- [tools/validate.py](tools/validate.py) checks records for completeness, allowed answers, and basic types, using only the Python standard library.
- [figure2](figure2) contains the stage counts and plotting script behind Figure 2 of the accompanying article.
- [legacy/v0.2.0](legacy/v0.2.0) preserves the previous version of the checklist, schema, validator, templates, and audits unchanged.

## Using the protocol in a manuscript

The protocol is intended as a submission artefact rather than an internal aid. Authors complete one entry per item of [checklist.md](checklist.md), in the Supplementary Information or in a versioned repository, and each entry states the choice or value that was actually used, followed by the location of the details; a pointer alone leaves the reader to reconstruct precisely the information that the protocol is meant to collect. Every item is answered, but not every operation has to be performed. An item can be answered with a value (`value`), as not applicable when the component is absent from the workflow (`not_applicable`), or as not performed, together with the consequence for the claim (`not_performed`). The stage ledger records candidate counts and evaluator calls at every stage, and the key numbers are condensed into one or two sentences in the main text.

Two further situations follow from the same logic. When a record is completed from a publication rather than by its authors, a fourth answer, `not_stated`, marks information that only the authors could supply. Readers and reviewers, in turn, face a different task, namely to establish what was reported rather than what was done, and retrospective audits therefore assign one of four disclosure states: `reported`, `partially_reported`, `not_reported`, or `not_applicable`.

## Validating a record

Python 3.9 or newer is sufficient, and no packages need to be installed:

```console
python tools/validate.py examples
```

The command accepts one JSON file or a directory of JSON files, and records with `checklist_version` 0.2.0 are checked with the archived version 0.2.0 validator. The validator checks structure and completeness only. It cannot judge whether a scientific method, threshold, baseline, or conclusion is appropriate, which remains a matter of scientific assessment.

## Citation and licence

Please cite this repository using [CITATION.cff](CITATION.cff); the associated article is in preparation. The protocol text, templates, schema, examples, and code are licensed under CC BY 4.0 (see [LICENSE](LICENSE)). Each change from version 0.2.0, together with the reason for it, is listed in [CHANGELOG.md](CHANGELOG.md).
