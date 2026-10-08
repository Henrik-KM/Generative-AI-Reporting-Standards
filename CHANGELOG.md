# Changelog

We recommend semantic versioning: `MAJOR.MINOR.PATCH`.

- **MAJOR**: changes that could change checklist interpretation (IDs added, removed, or materially redefined).
- **MINOR**: backward compatible additions or clarifications.
- **PATCH**: typo fixes and purely editorial changes.

## v1.0.0 (2026-10-08)

Version 1.0.0 was revised after version 0.2.0 had been applied to published studies, and it is frozen; later changes will be recorded here in the same form. The changes and their reasons are as follows.

- **Structure.** The items are ordered into eight steps, from stating the claim to summarising the key numbers, and the identifiers D1, S1, and so on are replaced by item names. The order in which authors complete a record matters, since the claim bounds every later entry.
- **Use and scope.** The protocol now states how authors complete it, the three admissible answers (value, not applicable, not performed), and its scope, including proposal engines that are not generative models. Version 0.2.0 did not state whether the checklist was a submission artefact or an internal aid, nor how a component absent from the workflow should be recorded.
- **Claim and evidence level.** New item; evaluation and feasibility entries can only be judged against an explicit claim and the evidence level at which it was established.
- **Stage ledger and key numbers.** The optional key-number summary is replaced by a required stage ledger, with evaluator calls and cost per call, and a required main-text summary. Retrospective applications showed that these numbers are the most dispersed in published studies, although they are the ones needed to compare workflows.
- **Data.** The shortcut baseline and perturbation check are replaced by a retrieval baseline under Baselines and a tolerance-and-threshold sensitivity analysis under Evaluation, which serve their purpose, namely to detect memorisation and fragile conclusions, more directly.
- **Training and Generation.** Inference throughput moved from Training to Generation, since it is a property of sampling.
- **Evaluation.** Renamed from Metrics; the stage of novelty assessment, the side-by-side report of surrogate and high-fidelity evaluator, and the sensitivity analysis were added, since relaxation can change candidate identity.
- **Baselines and ablations.** Restated as one domain-independent principle followed by domain-specific instances, with the MOSES and GuacaMol protocols listed alongside inorganic baselines.
- **Feasibility.** Dynamical stability added as a separate level of evidence; a relaxed structure with a low energy above hull can still be a saddle point with unstable modes.
- **Closed loop.** Renamed Closed loop and uncertainty; the abbreviation UQ is defined.
- **Records.** Author records use three answers; records completed from publications add `not_stated`; retrospective audits keep four disclosure states. The schema, validator, and templates were rewritten accordingly, and an optional structured stage ledger was added.
- **Examples.** Two worked records completed from publications (an active-learning study of high-entropy oxygen carriers and the MatterGen bulk-modulus campaign) were added, and two retrospective audits were converted to version 1.0.0 identifiers. The stage counts and plotting script for Figure 2 of the accompanying article were added.
- **Legacy.** The version 0.2.0 checklist, schema, validator, templates, and audits are preserved unchanged in `legacy/v0.2.0`, and the validator checks version 0.2.0 records with the archived validator.

## v0.2.0 (2026-08-28)

- Aligned the checklist with the revised manuscript: nine required items, three context-dependent items, and one optional key-number summary.
- Made the leakage audit, inorganic feasibility criteria, and inorganic baseline requirements operational.
- Required uncertainty across independent runs when stochastic variation affects a claim, without prescribing a fixed number of runs for every study.
- Clarified that governance controls are context dependent and should be reported only when a material concern exists.
- Added a JSON Schema, a dependency-free validator, and three sourced worked examples.
- Corrected text-encoding artefacts and updated the author-response templates.

## v0.1.0 (2026-05-21)

- Initial public draft of the minimum reporting checklist.
