# Reporting Checklist for Generative Materials Design

This repository provides a lightweight reporting checklist for generative materials design studies. It treats the complete workflow, from data and candidate generation to filtering, evaluator use, and validation, as the unit that should be reported. The checklist does not prescribe one preferred discovery pipeline or treat reporting completeness as a substitute for scientific assessment.

## Development revision for npj Computational Materials

The `hkm/npj-computational-materials` branch develops `1.0.0-draft`. It changes applicability and reporting requirements and is identified separately from the published 0.2.0 archive. It is not a new Zenodo release. Existing 0.2.0 audit records remain unchanged and are validated under their original applicability rules.

The manuscript uses full category names. Machine-readable records retain the existing identifiers so that older citations and artefacts remain traceable. Core categories require a response, not performance of every operation named in the checklist.

## Repository contents

- [checklist.md](checklist.md) contains the canonical checklist wording and stable identifiers.
- [templates/author_response_template.md](templates/author_response_template.md) and [templates/author_response_template.tex](templates/author_response_template.tex) provide short author-response forms.
- [schema/reporting-checklist.schema.json](schema/reporting-checklist.schema.json) defines the machine-readable JSON format.
- [examples](examples) contains the three original retrospective applications and a development author-format oxygen-carrier record with operational values, source locations and explicit gaps in historical run evidence.
- [tools/validate.py](tools/validate.py) checks required fields, item coverage, allowed disclosure states, and basic field types using only the Python standard library.

## Use in a manuscript

1. Declare the workflow, cohort, claimed physical endpoint, and comparison before completing the form.
2. Give an operational response for every core category, identifying the actual values, procedures, supporting locations and versions. Attach one consolidated record to the submission and refer to it briefly in the main text.
3. Distinguish information supplied, applicable work not performed, genuine inapplicability, and unavailable reporting. In the development format, an inapplicable category needs an `applicability_reason`; every unavailable operational detail needs a `rationale` and a null value.
4. Keep training, proposal attempts, unique candidates, evaluator calls, retries and retained outcomes separate. Inference throughput belongs to generation. An initial dataset is not a cumulative proposal total.
5. Supply context-dependent categories when they affect the claim, or justify inapplicability. The optional summary is only a compact presentation; claim-relevant counts and evaluator accounting still belong in the underlying categories.

The 0.2.0 format uses `reported`, `partially_reported`, `not_reported`, and `not_applicable`. The development format adds `not_performed` for an applicable operation known not to have been undertaken. A retrospective auditor must not infer `not_performed` from missing reporting. Partial coverage can still be recorded at category level, with individual `details` carrying operational responses. A record can cover every category and still expose missing scientific or archival evidence.

## Validate a JSON response

Python 3.9 or newer is sufficient; no packages need to be installed.

```console
python tools/validate.py examples
```

The same command accepts one JSON file or a directory containing JSON files. The validator checks structure, coverage, explicit gaps and justified inapplicability. It does not judge whether a scientific method, threshold, baseline, or conclusion is appropriate. A passing result is not a certificate of methodological adequacy or complete historical run provenance.

## Worked examples

The three 0.2.0 applications audit published reporting and preserve the section, figure, table or availability statement from which a judgement was derived. Hessmann et al. is an adjacent active-learning search without a trained generative proposal model, not a generative-model performance benchmark. These records are not rankings and have not been silently rescored against the development revision.

The development Brorsson record instead shows the form an author would supply: concrete decisions and values in each category, with the evidence boundary and unavailable quantities stated. The initial GitLab database directly verifies 1815 cycle-zero entries, 1066 retained and 749 filtered, with an exact matching export. It is not used as a campaign proposal or evaluator budget. The ACS publication, companion methods account, source snapshots and historical model-run provenance are kept separate. Differences in the reported initial-run count and entropy-filter scope remain explicit; later logs and public dataset access still need resolution.

## Citation and licence

Please cite the associated review article using [CITATION.cff](CITATION.cff). Until publication, the journal details remain provisional. The checklist text is licensed under CC BY 4.0; see [LICENSE](LICENSE).
