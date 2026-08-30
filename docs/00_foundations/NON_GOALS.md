# XoX Non-Goals

The following explicit non-goals protect XoX from scope creep, architectural dilution, and semantic compromise.

## Semantic & Logic Boundaries
1. **Not a Boolean Replacement**: XoX is not a drop-in replacement for standard binary booleans (`True`/`False`) in ordinary logic.
2. **Not a Generic Container**: XoX is not an `Optional`, `Nullable`, `None`, `Result`, or exception replacement.
3. **Not Probabilistic or Fuzzy**: `Unknown` is neither a probability, confidence score, fuzzy truth degree, nor a business workflow "pending" state.
4. **Not Universal Uncertainty Modeling**: XoX does not attempt to represent every form of domain uncertainty as an XoX value.

## Domain & System Boundaries
5. **Not an Infrastructure Platform**: XoX is not a consensus protocol, distributed database, workflow engine, policy evaluator, or monitoring framework.
6. **No Premature Machine Exposure**: XoX does not expose internal semantic machinery when simpler models suffice for the developer's task.
7. **No Automatic Academic Adoption**: XoX does not automatically ingest experimental discoveries or unproven theorems from XoXLang.

## Engineering & Governance Boundaries
8. **No Unsafe Invariant Bypasses**: XoX does not provide "unsafe" or expert modes that weaken or disable core semantic invariants.
9. **No Performance-Degraded Semantics**: Optimization must never alter, approximate, or silently weaken deterministic semantic guarantees.
10. **No Indefinite Legacy Support**: XoX will not compromise guarantees or accept disproportionate complexity to maintain obsolete platforms, Python runtimes, or ABIs.
11. **No Uncertainty Masking**: XoX will not artificially conceal decision-relevant uncertainty behind naive or silent defaults.
