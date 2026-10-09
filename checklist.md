# A reporting protocol for generative materials design (version 1.0.0)

Generative models can now propose candidate materials far faster than they can be validated, and the scientifically relevant outcome of a study is therefore the small subset of candidates that survives filtering and evaluation, rather than the generated set itself. To this end, the protocol below treats the complete workflow, from data and candidate generation through filters and evaluators to validated outcomes, as the unit of reporting. Its eight steps follow the order in which a record is best completed, since the claim stated in the first step bounds every later entry. The protocol does not prescribe a preferred pipeline, and a complete record does not by itself establish that the chosen methods, thresholds, or conclusions are appropriate.

## How to use the protocol

Authors complete one entry per item at submission, in the Supplementary Information or in a versioned repository. Each entry states the choice or value that was actually used, in one or two sentences, followed by the location of the full details; a pointer alone is not an entry. Every item is answered in one of three ways: with the value or procedure; as *not applicable*, with the reason the component is absent from the workflow; or as *not performed*, with the consequence for the claim. Items marked *(if applicable)* are answered as not applicable when the component is absent. When a record is completed from a publication rather than by its authors, a fourth answer, *not stated*, marks information that only the authors could supply.

The protocol applies to any workflow in which a proposal engine, whether a generative model, an enumeration scheme, or a structure search, feeds a sequence of filters and evaluators. Model and training items refer to every model trained within the workflow, including surrogates and machine-learning interatomic potentials.

## The eight steps

### 1. State the claim

- **Claim and evidence level.** The outcome claimed; the evidence level at which it was established (surrogate, machine-learning potential, first-principles calculation, simulation, or experiment); and any comparison with other methods that is claimed.

### 2. Map the workflow

- **Stage ledger.** For every stage, the rule or evaluator, the numbers of candidates entering and leaving, the number of evaluator calls, and the cost per call; for iterative workflows, per cycle and in total.

### 3. Describe the data

- **Data.** Each dataset with version, licence, size, label types, preprocessing, filters, and deduplication; the rule and tolerances that define when two candidates are identical (for example, structure-matcher settings, composition and space group, or a Tanimoto threshold); the resulting cross-split collision rate; and split manifests or stable identifiers.
- **Splits.** Strategy, grouping unit, sizes, and rationale; every set used for model selection; and, for iterative workflows, which data were acquired during the campaign and whether a held-out test set remained untouched.

### 4. Describe how candidates were produced

- **Model.** Input representation, architecture, final hyperparameters, and random seeds for the generator, surrogates, and any machine-learning potential.
- **Training.** Optimiser and schedule, steps or epochs, batch size, numerical precision, hardware, and wall-clock time.
- **Generation.** Conditioning targets, sampler, number of proposals, diversity controls, all repair, rejection, and post-processing rules with pass rates before and after them, and inference throughput on stated hardware.

### 5. Define success and its evidence

- **Evaluation.** Definitions of validity, uniqueness, novelty, diversity, and task success, each with its reference set, matching rule, evaluator, and stage (before or after relaxation); the surrogate and the high-fidelity evaluator side by side; how conclusions change with the matching tolerance and thresholds; and the uncertainty across independent runs.
- **Feasibility.** Each level of evidence separately, namely chemical validity screens; thermodynamic stability with relaxation protocol, reference database and version, energy corrections, competing phases, and threshold; dynamical stability, with the phonon or finite-temperature protocol and the treatment of imaginary modes, whenever stability or metastability is claimed; synthesizability evidence, such as retrosynthesis settings for molecules or condition-dependent free energies, precursors, kinetics, or experiments for inorganic materials; and fabrication constraints for structured materials. A low 0 K energy above the convex hull alone does not establish synthesizability.

### 6. Establish the comparison

- **Baselines and ablations.** The strongest simpler method that addresses the same task, and a trivial baseline such as random selection or retrieval of the nearest training examples, all under the same search space, filters, evaluator protocol, and evaluator budget; at least one ablation of the claimed key component. Typical simpler methods are library screening, genetic algorithms, and the MOSES or GuacaMol protocols for molecules; prototype retrieval, data-mined ion substitution, and charge-balanced prototype enumeration for inorganic crystals; and screening of hypothetical databases or topology optimisation for porous and structured materials.

### 7. Complete the context

- **Closed loop and uncertainty** *(if applicable)*. Acquisition policy, uncertainty quantification (UQ) method, batch size, number of rounds, stopping rule, and total evaluations.
- **Reproducibility.** Code, weights, evaluation scripts, data, and environment, or the access restrictions; pinned versions; and one command that rebuilds the reported figures and tables.
- **Compute** *(if applicable)*. Training and evaluator compute where it affects comparison, with energy estimates where feasible.
- **Governance** *(if applicable)*. Whether the candidate class, capability, access pathway, or intended use creates a dual-use or safety concern, and the controls used if so.

### 8. Summarise the key numbers in the main text

- **Key numbers.** One or two sentences that condense the stage ledger: proposals generated, candidates and evaluator calls at each level of evidence, and the validated outcomes together with the level at which they were validated.

## Machine-readable identifiers

| Step | Item | Identifier | Category |
|---|---|---|---|
| 1 | Claim and evidence level | `claim` | required |
| 2 | Stage ledger | `stage_ledger` | required |
| 3 | Data | `data` | required |
| 3 | Splits | `splits` | required |
| 4 | Model | `model` | required |
| 4 | Training | `training` | required |
| 4 | Generation | `generation` | required |
| 5 | Evaluation | `evaluation` | required |
| 5 | Feasibility | `feasibility` | required |
| 6 | Baselines and ablations | `baselines` | required |
| 7 | Closed loop and uncertainty | `closed_loop` | if applicable |
| 7 | Reproducibility | `reproducibility` | required |
| 7 | Compute | `compute` | if applicable |
| 7 | Governance | `governance` | if applicable |
| 8 | Key numbers | `key_numbers` | required |

The changes from version 0.2.0, and the reason for each, are listed in [CHANGELOG.md](CHANGELOG.md).
