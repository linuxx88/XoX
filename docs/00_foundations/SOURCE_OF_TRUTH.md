# Source of Truth & Semantic Authority

This document defines the boundary of semantic authority and product governance between XoXLang and XoX.

## Authority Separation
1. **Scientific Semantic Authority**: XoXLang is the sole scientific authority governing formal semantic rules, logical invariants, and mathematical definitions.
2. **Product Implementation Authority**: XoX is the developer-facing product, runtime implementation, and distribution layer.

## Boundary Principles & Adoption
3. **Independent Evolution**: XoXLang evolves independently through theoretical discoveries, adversarial analyses, and experimental formulations.
4. **Selective Adoption**: XoX does not automatically inherit XoXLang modifications. Only rules with proven, sufficient maturity may become binding XoX guarantees.
5. **Semantic Invariant Inviolability**: XoX must never reinterpret, weaken, or approximate an adopted XoXLang rule for implementation convenience, performance, or ergonomics.
6. **Defect Classification**: Any behavioral discrepancy between an adopted XoXLang rule and XoX implementation is classified as a defect in XoX, unless an explicit, documented boundary states the rule is unadopted.
7. **No Authority for Immature Rules**: Experimental, provisional, superseded, or rejected XoXLang rules carry zero binding authority in XoX.
8. **Product Policy Autonomy**: XoX governs runtime ergonomics, target platforms, packaging, and API organization, provided these policies do not alter or compromise adopted semantics.
9. **Traceable Provenance**: Every adopted XoX guarantee must maintain verifiable provenance back to its originating XoXLang specification when applicable.
10. **Fail-Closed Ambiguity**: In cases of ambiguity or conflicting interpretations regarding semantic authority, XoX must fail closed rather than adopting a speculative or convenient interpretation.
