# Reporting checklist for generative materials design

The checklist contains nine required items, three context-dependent items, and one optional key-number summary. The stable identifiers are intended for versioned citations and reviewer cross-referencing. Required items should be summarised in the main text, while complete protocol details can be placed in the Supplementary Information or a versioned repository when space is limited.

## Required reporting items

- [ ] **D1 Data**: Name and version of each dataset and the licence. Include size (`n`), label types, preprocessing, filters, and split manifests. Predeclare a modality-appropriate duplicate rule and its tolerances, such as a structure matcher, composition plus space-group bucket, Tanimoto threshold, or sample, batch, or acquisition identifier. Report the cross-split collision rate. For claims of held-out generalisation, aim for zero collisions under the predeclared matching rule; if collisions remain, justify them, repeat the analysis after excluding them, and state whether the conclusion changes. Include one shortcut baseline, such as metadata only or formula only, and one perturbation check, such as shuffled labels or removed structure information. Publish exact item IDs and, where relevant, file hashes with checksums or a repository tag or commit.

- [ ] **S1 Splits**: State the split strategy, sizes, rationale, and grouping unit, and identify every split or external dataset used for model selection.

- [ ] **M1 Inputs/Model**: State the input representations, architecture family, final hyperparameters, and random seeds.

- [ ] **T1 Training**: Report steps or epochs, optimiser and schedule, hardware type and count, wall-clock time, batch size, numerical precision, and inference throughput on stated hardware.

- [ ] **G1 Generation**: Describe conditioning targets, the sampler or solver, total candidates (`N_gen`), diversity controls, and any repair, rejection, or post-processing rules. For comparisons, report whether metrics are computed on as-generated samples or after post-processing, such as chemistry canonicalisation, geometry relaxation, redocking, or DFT relaxation. Report both raw and post-filter pass rates when filters are used.

- [ ] **E1 Metrics**: Define validity, novelty, diversity, relaxability, and task success, including the reference set, matching rule, evaluator, and evaluation stage. Report uncertainty across independent runs where stochastic variation affects the claim.

- [ ] **B1 Baselines and ablations**: Include a trivial baseline, such as random generation or retrieval; a transparent non-generative baseline, such as virtual screening; and, where relevant, a simple non-deep-learning generator, such as a genetic algorithm. For inorganic crystals, compare against retrieval from known prototypes, data-mined ion substitution, and charge-balanced, oxidation-state-constrained random or decorated prototype enumeration where the task permits. Apply the same search space, fast filters, evaluator protocol, and evaluator budget to every method. Include an ablation that removes the key component, and state all benchmark protocol details.

- [ ] **F1 Feasibility**: Separate chemical validity, thermodynamic stability, synthesizability, and manufacturability. For inorganics, report fast charge, oxidation-state, and element screens separately from post-relaxation stability. No universal inorganic synthesizability proxy exists, and low 0 K `E_hull` alone is insufficient. Pin the relaxation protocol, reference database and version, energy corrections, competing phases, thresholds, and any stated metastability window. If the claim concerns experimental conditions, report temperature, pressure, chemical potentials, or finite-temperature free energies as applicable. Report route- or kinetics-based evidence separately. For molecules, state the retrosynthesis tool and version, template set, depth or time limits, and success criterion. For structured materials, report minimum feature size, connectivity, and tolerance constraints. At every stage, report `N_pass/N_gen` and whether the metric is before or after relaxation.

- [ ] **R1 Reproducibility**: Provide public code and model weights when release is permissible. Otherwise, state access restrictions, provide executable evaluation scripts where possible, and document the exact artefacts needed to reproduce the reported metrics. Include an environment lockfile, pinned evaluation scripts and split manifests with a repository URL and tag or commit, short checksums for split-list files, a single command to rebuild figures and tables, and notes on determinism, including seeds and cuDNN settings.

## Context-dependent reporting items

These items should be included when they affect interpretation. Supplementary Information or a versioned repository is acceptable when space is limited. A machine-readable response should retain each identifier and use `not_applicable` only when the corresponding workflow component or material concern is absent, with a brief rationale.

- [ ] **CL1 Closed-loop/UQ**: If a closed loop is used, state the acquisition policy, batch size, number of rounds, stopping rule, uncertainty-quantification method, and total evaluations.

- [ ] **C1 Compute footprint**: Report training and inference throughput in candidates per GPU-hour, accelerator types and counts, and wall-clock time. When feasible, report energy and carbon estimates. As a default, estimate energy as wall-clock time multiplied by average power draw and carbon as energy multiplied by the grid-emissions factor, optionally scaled by an assumed power usage effectiveness. Report uncertainty bands.

- [ ] **GOV1 Governance and ethics**: Explain whether the model, candidate class, access pathway, or intended use creates a material dual-use, safety, misuse, or access concern. Where it does, describe the relevant controls, such as hazard filtering, controlled access, or monitoring. Where it does not, state the rationale briefly. Prospective validation is required here only when a governance or safety claim depends on it.

## Optional key-number summary

- [ ] **K1 Key-number summary**: `N_gen=...; stagewise pass rates=...; validated outcomes=...; evaluator budget=...; closed loop=R rounds × N_eval evaluations (where used); training cost=...; inference cost=...; tag=repo@vX.Y`.

Any deviation from the checklist should be stated and briefly justified. The checklist records what was done and where it was reported; it does not by itself establish that the selected methods, thresholds, or scientific claims are appropriate.
