# Universal XoX Guarantees

These universal guarantees are inviolable invariants that bind all layers, bindings, runtime optimizations, and future extensions of XoX.

### `XOX-GUAR-001`: Tri-State Distinction
XoX values preserve the fundamental semantic distinction between `True`, `False`, and `Unknown` in all contexts where the distinction is semantically relevant.

### `XOX-GUAR-002`: Non-Collapsing Unknown
`Unknown` must never be silently collapsed, coerced, or defaulted into `True` or `False`.

### `XOX-GUAR-003`: Domain Separation
The domain of binary booleans (`Bool`) and the domain of XoX values remain strictly distinct unless an explicit, authorized conversion is invoked.

### `XOX-GUAR-004`: Monotonic Guarantee Hierarchy
Greater API access or higher abstraction levels must never weaken, bypass, or invalidate guarantees provided at a lower level.

### `XOX-GUAR-005`: Invariant Priority
Implementation convenience, runtime performance, backward compatibility, or platform ergonomics must never silently alter or degrade an adopted semantic invariant.

### `XOX-GUAR-006`: Fail-Closed Verification
Whenever required semantic evidence, authority, or contextual inputs are missing or ambiguous, evaluation must fail closed rather than assuming success.

### `XOX-GUAR-007`: Consequence Visibility
While internal execution mechanisms may be encapsulated, all decision-relevant semantic consequences must remain directly visible and accessible to the caller.

### `XOX-GUAR-008`: Observable Determinism
Observable semantics—including evaluation ordering, skipped side effects, state transitions, and error paths—must not be altered by execution optimizations when they form part of the adopted contract.

### `XOX-GUAR-009`: Boundary State Preservation
Serialization, language bindings (FFI), inter-process communication, and cross-boundary transport must not silently drop, truncate, or corrupt semantically required state.

### `XOX-GUAR-010`: Invariant Inviolability
Any operation or state transition that would force an invariant violation must be strictly rejected.

### `XOX-GUAR-011`: Guarantee Traceability
Every adopted guarantee must remain verifiable and traceable to its formal justification, evidence record, and originating specification.
