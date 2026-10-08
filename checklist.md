# Reporting checklist for generative materials design

Development version `1.0.0-draft` contains nine core response categories, three context-dependent categories, and one optional compact summary. It is separate from the published 0.2.0 archive. Core means that a category receives an operational response, not that every named experiment must be performed. The manuscript uses full category names; the existing machine identifiers are retained for compatibility. Attach the consolidated record to the submission and refer to it briefly in the main text.

## Core reporting categories

- [ ] **Data (`D1`)**: Name dataset versions, licences, sizes, labels, preprocessing, filters and duplicate rules. For held-out claims, give manifests, matching tolerances and collision rates. Aim for zero forbidden collisions; justify any remainder and show whether exclusion changes the conclusion. Identify a claim-relevant shortcut or perturbation check, its result, or its non-performance and consequence. A formula-only predictor can test a geometry-dependent claim; a label-permutation check with retraining can test dependence on the intended data-label association. State why the diagnostic is relevant.

- [ ] **Splits (`S1`)**: Give partition sizes, grouping units, rationale and data used for model selection. Distinguish online acquisition from a held-out predictive test. An initial acquisition cohort is not a train-test split. If no partition forms part of the workflow, explain why and bound the generalisation claim.

- [ ] **Inputs and model (`M1`)**: Give representations, architecture, actual final hyperparameters and seeds for each generator and evaluator. Distinguish run settings from software defaults and identify frozen external components.

- [ ] **Training (`T1`)**: Report optimiser, schedule, steps or epochs, batch size, precision, hardware and training time for trained components. Identify components that were not trained in the study. Report inference throughput under generation.

- [ ] **Generation (`G1`)**: Give targets, sampler, attempted and unique-candidate counts, diversity controls, repair and rejection rules, and inference throughput on stated hardware. Define the cohort and each post-processing stage, and distinguish metrics before and after post-processing. Do not substitute a training-set size for a proposal total.

- [ ] **Metrics (`E1`)**: Define each claimed measure, denominator, reference set, matching rule, evaluator and stage. Report uncertainty where stochastic variation affects interpretation. Keep computational screening and experimental outcomes distinct; do not label pooled or within-run variation as independent-run confidence intervals.

- [ ] **Baselines and ablations (`B1`)**: State comparisons actually performed and justify their relevance. A superiority claim needs matched search spaces, filters, evaluators and budgets, and an ablation of the claimed component. Molecular random/retrieval selection, virtual screening and simple generators, and inorganic ion substitution or prototype enumeration are task-dependent options, not compulsory methods for every paper. MOSES and GuacaMol are applicable when their task and protocol match the claim. Describe missing comparisons and the resulting claim limits.

- [ ] **Feasibility (`F1`)**: Separate chemical validity, thermodynamic and dynamical stability, synthesizability, and manufacturability. Pin relaxation and hull protocols, reference phases, corrections and thresholds. Low 0 K hull energy and structural relaxation alone do not establish dynamical stability or synthesizability. For stability claims, state whether phonons or an appropriate finite-temperature assessment were used, with the evaluator, convergence and unstable-mode handling. Give routes, conditions and kinetic evidence where required by the claim. For molecules, identify route tools and constraints; for structured materials, give geometric, connectivity and fabrication-tolerance limits. Report stage counts and identify applicable assessments not performed.

- [ ] **Reproducibility (`R1`)**: Identify data, weights, configurations, evaluation code, candidate and split manifests, environment and determinism settings, with versions or checksums. Give a rebuild command where available and define what it rebuilds. State restrictions and unavailable historical artefacts explicitly. An inspected implementation commit is not automatically the commit used in a publication run.

## Context-dependent reporting items

Retain a response for these categories. Include operational details when they affect interpretation, or justify inapplicability. In the development format, a category-level `not_applicable` response needs an `applicability_reason`, including for core categories whose operations are absent from the declared workflow.

- [ ] **Closed loop and uncertainty quantification (`CL1`)**: Give acquisition and uncertainty methods, batches, rounds, stopping criteria and cumulative evaluator calls when acquisition or updating is iterative. Account explicitly for pooled runs, duplicates, failed calls and repeats; nominal rounds multiplied by a nominal batch size may not equal the evaluator budget.

- [ ] **Compute footprint (`C1`)**: Separate training, generation and evaluation costs. Give devices, timings and throughput. Supply energy or carbon only where measured or defensibly estimated, with assumptions and uncertainty. Do not infer evaluator cost from the number of retained candidates.

- [ ] **Governance and ethics (`GOV1`)**: State whether the candidate class, capability, access pathway or intended use creates a material concern. Give corresponding controls or a reasoned inapplicability statement. Missing discussion is not evidence of no risk; prospective validation is required only when a governance or safety claim depends on it.

## Optional key-number summary

- [ ] **K1 Key-number summary**: `N_gen=...; stagewise pass rates=...; validated outcomes=...; evaluator budget=...; closed loop=R rounds × N_eval evaluations (where used); training cost=...; inference cost=...; tag=repo@vX.Y`.

The compact-summary format is optional; counts and evaluator accounting needed to interpret a claim still belong in the relevant categories. Keep candidate counts and evaluator-call counts in separate stage-ledger columns.

## Operational responses and status

`reported` supplies a value or method and its source. `not_performed` describes an applicable operation known not to have been undertaken, with a reason and claim consequence. `not_applicable` means the operation is absent from the declared workflow, with a rationale. `not_reported` means the available evidence does not establish the detail, including unavailable historical records. Audits can use `partially_reported` at category level. Missing values remain null rather than zero. These states support transparent reporting; they do not establish the adequacy of a method, threshold or conclusion.
