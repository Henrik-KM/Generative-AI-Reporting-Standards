# Changelog

A reporting protocol is only useful if its requirements are stable and the reason for each requirement is clear. Versions therefore follow `MAJOR.MINOR.PATCH`, where a major version changes how the protocol is interpreted (items added, removed, or materially redefined), a minor version adds backward-compatible clarifications, and a patch corrects typographical or purely editorial errors. Every change is listed together with its reason.

## v1.0.0 (2026-10-09)

Version 1.0.0 was revised after version 0.2.0 had been applied retrospectively to published studies and to the two worked examples in this repository. In practice, these applications showed where the earlier checklist was ambiguous, and every change below addresses one such ambiguity. Version 1.0.0 is frozen, and later changes will be recorded here in the same form.

- Structure. The items are ordered into eight steps, from stating the claim to summarising the key numbers, and the identifiers D1, S1, and so on are replaced by item names. The order matters, since the claim stated in the first step bounds every later entry, whereas the codes carried no information that the names do not.
- Use and scope. The protocol now states how authors complete it, the three admissible answers (value, not applicable, not performed), and its scope, which includes proposal engines that are not generative models. Version 0.2.0 stated neither whether the checklist was a submission artefact or an internal aid, nor how a component absent from the workflow should be recorded.
- Claim and evidence level. This item is new, since evaluation and feasibility entries can only be judged against an explicit claim and the evidence level at which it was established.
- Stage ledger and key numbers. The optional key-number summary is replaced by a required stage ledger, with evaluator calls and cost per call, and by a required main-text summary. The retrospective applications showed that these numbers are the most dispersed in published studies, although they are precisely the ones needed to compare workflows.
- Data. The shortcut baseline and perturbation check are replaced by a retrieval baseline under Baselines and a tolerance-and-threshold sensitivity analysis under Evaluation. Both replacements serve the original purpose, namely to detect memorisation and fragile conclusions, more directly than the undefined checks of version 0.2.0.
- Training and Generation. Inference throughput moved from Training to Generation, since it is a property of sampling rather than of training.
- Evaluation. The item is renamed from Metrics, and the stage of novelty assessment, the side-by-side report of surrogate and high-fidelity evaluator, and the sensitivity analysis are added. This reflects that the item covers the evaluation protocol rather than only metric definitions, and that relaxation can change the identity of a candidate.
- Baselines and ablations. The item is restated as one domain-independent principle followed by domain-specific instances, with the MOSES and GuacaMol protocols listed alongside the inorganic baselines. The principle applies across domains, whereas suitable comparators differ between them.
- Feasibility. Dynamical stability is added as a separate level of evidence, since a relaxed structure with a low energy above the convex hull can still sit at a saddle point with unstable modes.
- Closed loop. The item is renamed Closed loop and uncertainty, and the abbreviation UQ is defined.
- Records. Author records use three answers, records completed from publications add `not_stated`, and retrospective audits keep four disclosure states, since an author knows whether an operation was performed, whereas a reader can only establish whether it was reported. The schema, validator, and templates were rewritten accordingly, and an optional structured stage ledger was added.
- Examples. Two worked records completed from publications, for the MatterGen bulk-modulus campaign and for an active-learning study of high-entropy oxygen carriers, were added, and two retrospective audits were converted to version 1.0.0 identifiers. The stage counts and plotting script behind Figure 2 of the accompanying article were added as well.
- Legacy. The version 0.2.0 checklist, schema, validator, templates, and audits are preserved unchanged in `legacy/v0.2.0`, and the validator checks version 0.2.0 records with the archived validator.

## v0.2.0 (2026-08-28)

- Aligned the checklist with the revised manuscript: nine required items, three context-dependent items, and one optional key-number summary.
- Made the leakage audit, inorganic feasibility criteria, and inorganic baseline requirements operational.
- Required uncertainty across independent runs when stochastic variation affects a claim, without prescribing a fixed number of runs for every study.
- Clarified that governance controls are context dependent and should be reported only when a material concern exists.
- Added a JSON Schema, a dependency-free validator, and three sourced worked examples.
- Corrected text-encoding artefacts and updated the author-response templates.

## v0.1.0 (2026-05-21)

- Initial public draft of the minimum reporting checklist.
