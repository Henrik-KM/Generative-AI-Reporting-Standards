# Minimum reporting checklist (generative materials design)

We group items into **Required** (must report in the main text) and **Optional** (recommended; SI is acceptable).
Each item has a stable identifier (ID) intended for versioned citations and reviewer cross referencing.

## Required (must report in main text)

- [ ] **D1 Data**: Name and version of each dataset and the license. Include size (`n`), label types, preprocessing or filters, deduplication, and leakage checks (overlap between splits).
  - Include a minimal shortcut learning audit that probes for trivial cues.
  - The audit should include at least one intentionally underspecified baseline (for example metadata only or formula only), and at least one perturbation check (for example shuffled labels, or removed structure information) to test whether apparent performance persists without the intended signal.
  - Report leakage outcomes (for example cross split collision rate) and summarize the audit outcome in one line.
  - Publish split manifests (exact item IDs and, if relevant, file hashes) with checksums or a repository tag or commit.

- [ ] **S1 Splits**: Describe the split strategy (time based or group based, for example composition or scaffold). Provide split sizes and rationale. Note any data used for model selection.

- [ ] **M1 Inputs and model**: State the input representations, the architecture family, final hyperparameters, and random seeds.

- [ ] **T1 Training and inference**: Report steps or epochs, optimizer and schedule, hardware type and count, wall clock time (mean ± SD), batch size, precision, and inference throughput (samples per second or seconds per sample) with the same hardware specification.

- [ ] **G1 Generation protocol**: Describe conditioning targets, the sampler or solver, total candidates (`N_gen`), diversity controls, and any repair, rejection, or post processing rules.
  - For comparisons, state whether metrics are computed on as generated samples or after post processing (for example chemistry canonicalization, geometry relaxation, redocking, or DFT relaxation).
  - When filters are used, report both raw and post filter pass rates.

- [ ] **E1 Metrics**: Define validity, novelty, diversity, and relaxability precisely, including whether each is computed as generated or post processing. Report confidence intervals across at least three independent seeds.

- [ ] **B1 Baselines and ablations**: Include at least one trivial baseline (random or retrieval), one transparent non generative baseline (for example virtual screening), and where relevant a simple non deep learning generative baseline (for example genetic algorithm).
  - Include at least one ablation that removes the key component.
  - Where appropriate, report results under domain relevant benchmark protocols; suites such as MOSES and GuacaMol can be useful reference implementations, but they should not be treated as gold standard benchmarks, and protocol details (splits, filters, post processing) must be stated.

- [ ] **F1 Feasibility (thermodynamic vs synthetic)**: Separate thermodynamic and synthetic feasibility.
  - Thermodynamic feasibility: report protocol defined stability proxies under a pinned relaxation protocol; state whether stability refers to 0 K `E_hull`, finite temperature free energy stability, or metastability within a stated window.
  - Synthetic feasibility: report synthesizability or manufacturability proxies that depend on routes, conditions, and kinetics; specify the settings of any retrosynthesis analysis (tool and version, template set, depth or time limits, and success criterion).
  - For inorganics, apply charge neutrality, oxidation state consistency, and element constraints as fast screens and report post relaxation stability metrics separately.
  - For porous or metamaterial tasks, enforce minimum feature size and connectivity.
  - State each proxy and report `N_pass/N_gen` at each stage, separating pre and post relaxation metrics where applicable.

- [ ] **R1 Reproducibility**: Provide public code and model weights when release is permissible; otherwise, state access restrictions, provide executable evaluation scripts where possible, and document the exact artifacts needed to reproduce reported metrics. Include an environment lockfile (pins exact package versions), pinned evaluation artifacts (evaluation scripts and split manifests with repository URL and tag or commit, plus short checksums for split list files), a single command to rebuild figures or tables, and notes on determinism (seeds and cuDNN).

## Optional (recommended; SI acceptable)

- [ ] **CL1 Closed loop and uncertainty quantification (if used)**: State the acquisition policy (for example expected improvement or Thompson sampling), batch size, number of rounds, stopping rule, the uncertainty quantification method (ensemble, Monte Carlo dropout, or evidential), and total evaluations.

- [ ] **C1 Compute footprint**: Report training and inference throughput (candidates per GPU hour), accelerator types and counts, wall clock, and when feasible energy or carbon estimates.
  - As a default: energy ≈ wall clock × average power draw; carbon ≈ energy × grid emissions factor (optionally scaled by an assumed PUE). Report uncertainty bands.

- [ ] **GOV1 Governance and ethics**: State dataset licenses, any dual use screening, and a brief OECD aligned safeguards statement.
  - If external or prospective validation is not included, disclose why and outline a minimal proxy plan (for example preregistered evaluation protocol, external blind test in a later phase, or cross lab computational validation with frozen code and splits).

- [ ] **K1 Key number summary (optional)**: `Ngen=...; Validity=...% (CI; seeds ≥3); Novelty=...%; Relaxability=...% (protocol=...); Feasibility pass rate=pass/gen=... (pre or post); Closed loop=R rounds × N_eval evaluations; Training=(T) h on H GPUs; Tag=repo@vX.Y`.
