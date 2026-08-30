# XoX Canonical Nomenclature

This document establishes the canonical vocabulary for the XoX project. Each concept has exactly one canonical definition to prevent semantic drift.

## Semantic States & Domains

- **True**: The definite positive semantic state in XoX.
- **False**: The definite negative semantic state in XoX.
- **Unknown**: The state of inability to currently establish `True` or `False` under the applicable semantic context.
  - *Distinction*: `Unknown` is NOT `None`, missing data, pending execution, unresolved state, probabilistic confidence, fuzzy truth, runtime error, or contradiction.
- **Contradiction**: A state of simultaneous conflicting assertions. It is semantically distinct from `Unknown` and cannot be resolved by treating it as uncertainty.
- **Bool**: The standard binary domain (`true`/`false`) external to and distinct from the XoX tri-state domain.

## Domain Operations

- **Collapse**: An explicit, intentional conversion from the XoX domain to the `Bool` domain under a defined resolution policy.
- **Promotion**: An explicit, intentional conversion from the `Bool` domain into the XoX domain.

## Invariants & Semantic Safety

- **Guarantee**: A formal product-level invariant adopted and verified by XoX.
- **Invariant**: A condition or rule that must never be violated across any execution path, optimization, or layer.
- **Authority**: Explicit semantic permission required to execute a protected operation.
- **Provenance**: Verifiable record of origin, lineage, and contextual history of a semantic state.
- **Stale**: A state, context, or evidence that is no longer valid for the current evaluation context.
- **Fail-Closed**: The mandatory refusal to assert a protected outcome or perform an operation when required evidence, context, or authority is absent or ambiguous.

## Authority & Governance

- **Semantic Authority**: The scientific jurisdiction over formal logic, proofs, and invariants (vested in XoXLang).
- **Product Authority**: The engineering jurisdiction over runtime implementation, packaging, platform support, and ergonomics (vested in XoX).

## Maturity States (Terminology)

- **Experimental**: An upstream or prototype concept undergoing research; holds zero product authority.
- **Candidate**: A proposed rule undergoing formal verification and adversarial attack.
- **Adopted**: A rule that has passed all verification gates and is bound by XoX guarantees.
- **Stable**: An adopted rule with extended production validation and strict backward-compatibility protection.
- **Rejected**: A candidate permanently denied adoption due to guarantee failure, unjustified complexity, or lack of developer need.
- **Superseded**: A previously adopted rule formally replaced by a strictly superior, non-regressive rule.

## Access Tiers

- **Core / Safe / Semantic**: Levels of required professional capability and semantic precision, NOT measures of developer skill or seniority.
  - **Core**: Baseline tri-state operations and minimal surface.
  - **Safe**: Ergonomic workflows with automated safety guardrails.
  - **Semantic**: Direct, explicit interaction with rich semantic contexts, provenance, and fine-grained constraints.

## Dangerous Near-Synonyms & Anti-Patterns

| Ambiguous / Dangerous Term | Canonical XoX Term | Reason for Distinction |
| :--- | :--- | :--- |
| `Null` / `None` / `Nil` | *Do not use for Unknown* | Implies absence of value, not semantic uncertainty. |
| `Pending` / `Loading` | *Do not use for Unknown* | Implies temporal progression or pending I/O. |
| `Probability` / `Confidence` | *Do not use for Unknown* | Implies continuous Bayesian degree, not tri-state logic. |
| `Error` / `Exception` | *Do not use for Unknown* | Implies abnormal failure, whereas `Unknown` is a valid result. |
| `Cast` / `Coerce` | **Collapse** or **Promotion** | Casting implies implicit or unsafe type transmutation. |
| `Expert Mode` | **Semantic Tier** | Implies unsafe privilege, violating monotonic guarantees. |
