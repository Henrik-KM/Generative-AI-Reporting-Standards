# A reporting protocol for generative materials design

Generative models can now propose candidate materials far faster than they can be validated. The scientifically relevant outcome of a study is therefore the small subset of candidates that survives filtering and evaluation, and whether a reported advance reflects a better model, a different filter, a more permissive evaluator, or a larger validation budget can only be judged from the complete workflow. This repository provides a reporting protocol that treats that workflow, from data and candidate generation through filters and evaluators to validated outcomes, as the unit of reporting. The protocol does not prescribe a preferred pipeline, and a complete record does not by itself establish that the chosen methods, thresholds, or conclusions are appropriate.

## Repository contents

- [checklist.md](checklist.md) gives the protocol (version 1.0.0): eight steps, from stating the claim and its evidence level to summarising the key numbers, with stable machine-readable identifiers.
- [templates](templates) contains an author-record template in Markdown, LaTeX, and PDF.
- [schema/reporting-checklist.schema.json](schema/reporting-checklist.schema.json) defines the machine-readable format for author records, records completed from publications, and retrospective audits, including an optional structured stage ledger.
- [examples](examples) contains two worked records completed from publications, for an active-learning study of high-entropy oxygen carriers and for the MatterGen bulk-modulus campaign, and two retrospective audits.
- [tools/validate.py](tools/validate.py) checks records for completeness, allowed answers, and basic types using only the Python standard library.
- [figure2](figure2) contains the stage counts and plotting script for Figure 2 of the accompanying article.
- [legacy/v0.2.0](legacy/v0.2.0) preserves the previous version of the checklist, schema, validator, templates, and audits unchanged.

## Use in a manuscript

1. Complete one entry per item of [checklist.md](checklist.md), in the Supplementary Information or in a versioned repository, stating the choice or value that was actually used and the location of the details.
2. Answer every item with a value, as `not_applicable` with the reason the component is absent, or as `not_performed` with the consequence for the claim.
3. Include the stage ledger, with candidate counts and evaluator calls at every stage.
4. Summarise the key numbers in one or two sentences in the main text.

When a record is completed from a publication rather than by its authors, a fourth answer, `not_stated`, marks information that only the authors could supply. Retrospective audits by readers or reviewers instead assign one of four disclosure states: `reported`, `partially_reported`, `not_reported`, or `not_applicable`.

## Validate a record

Python 3.9 or newer is sufficient; no packages need to be installed.

```console
python tools/validate.py examples
```

The command accepts one JSON file or a directory of JSON files. Records with `checklist_version` 0.2.0 are checked with the archived version 0.2.0 validator. The validator checks structure and completeness only; it does not judge whether a scientific method, threshold, baseline, or conclusion is appropriate.

## Citation and licence

Please cite this repository using [CITATION.cff](CITATION.cff); the associated article is in preparation. The protocol text, templates, schema, examples, and code are licensed under CC BY 4.0; see [LICENSE](LICENSE). The changes from version 0.2.0, and the reason for each, are listed in [CHANGELOG.md](CHANGELOG.md).
