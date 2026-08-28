# Reporting Checklist for Generative Materials Design

This repository provides a lightweight reporting checklist for generative materials design studies. It treats the complete workflow, from data and candidate generation to filtering, evaluator use, and validation, as the unit that should be reported. The checklist does not prescribe one preferred discovery pipeline or treat reporting completeness as a substitute for scientific assessment.

## Repository contents

- [checklist.md](checklist.md) contains the canonical checklist wording and stable identifiers.
- [templates/author_response_template.md](templates/author_response_template.md) and [templates/author_response_template.tex](templates/author_response_template.tex) provide short author-response forms.
- [schema/reporting-checklist.schema.json](schema/reporting-checklist.schema.json) defines the machine-readable JSON format.
- [examples](examples) contains three retrospective worked examples spanning molecular design, inorganic crystal generation, and active-learning crystal structure search.
- [tools/validate.py](tools/validate.py) checks required fields, item coverage, allowed disclosure states, and basic field types using only the Python standard library.

## Use in a manuscript

1. Summarise the nine required items in the main text and place full protocol details in the Supplementary Information or a versioned repository when needed.
2. Retain the stable item identifiers and give an exact source location for each response.
3. Include the three context-dependent items and use `not_applicable` only when the corresponding workflow component or material concern is absent, with a brief rationale.
4. State and justify any deviation from the checklist.

The machine-readable format uses four disclosure states: `reported`, `partially_reported`, `not_reported`, and `not_applicable`. These states describe reporting completeness. In particular, `not_reported` does not imply that the underlying method was inadequate.

## Validate a JSON response

Python 3.9 or newer is sufficient; no packages need to be installed.

```console
python tools/validate.py examples
```

The same command accepts one JSON file or a directory containing JSON files. The validator intentionally checks structure and completeness only. It does not judge whether a scientific method, threshold, baseline, or conclusion is appropriate.

## Worked examples

The examples apply the checklist retrospectively to three published studies. Each item contains a concise disclosure judgement and the section, figure, table, or availability statement from which it was derived. They demonstrate how information can be assembled when it is distributed across an article, Supplementary Information, and public artefacts; they are not rankings of the studies.

## Citation and licence

Please cite the associated review article using [CITATION.cff](CITATION.cff). Until publication, the journal details remain provisional. The checklist text is licensed under CC BY 4.0; see [LICENSE](LICENSE).
