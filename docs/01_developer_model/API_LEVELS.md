# XoX API Levels: Progressive Disclosure Model

This document establishes the official API level architecture for XoX, defining `CORE`, `SAFE`, and `SEMANTIC` as progressive levels of developer access driven strictly by professional need and decision sensitivity.

---

## Guiding Invariants & Philosophy

1. **Levels of Need, Not Competence**: `CORE`, `SAFE`, and `SEMANTIC` represent levels of required semantic control and problem complexity, never developer seniority, skill, or prestige.
2. **Knowledge Monotonicity**: Concepts learned at lower tiers remain strictly valid at higher tiers. More access never means fewer guarantees (`XOX-GUAR-004`).
3. **Additive Control, Invariant Safety**: Higher levels expose additional inspection, contextual evidence, and explicit control mechanisms. They never provide bypasses, loopholes, or weakened evaluation semantics.
4. **Encapsulated Complexity**: Advanced internal mechanisms (such as formal proof objects, lattice operations, and algebraic engines) remain internal to XoX until a specific professional problem requires explicit interaction with them.
5. **No Concealment of Consequences**: Operational and semantic consequences relevant to a decision are never hidden merely for aesthetic API simplicity.
6. **Principle of Least Complexity**: Developers should always prefer the simplest level sufficient to safely resolve their domain problem.

---

## Summary Matrix

| Level | Primary Purpose | Intended Context | Typical Persona Baseline |
| :--- | :--- | :--- | :--- |
| **CORE** | Minimal explicit tri-state decision logic (`True`, `False`, `Unknown`) with strict boolean separation. | Standard business logic, service boundaries, data validation, and basic branching. | Backend / API, Data / Streaming (basic), SRE (basic) |
| **SAFE** | Controlled uncertainty resolution, guarded collapse policies, and sensitivity verification. | Access control, security gates, automated remediation, sensitive action triggers. | Security / IAM, SRE / Platform, AI / Agent Systems |
| **SEMANTIC** | Explicit management of semantic context, provenance lineage, and distributed validity boundaries. | Distributed consensus, consensus replication, multi-epoch protocols, extensible agent runtime engines. | Distributed Systems, Agent Framework Authors |

---

## 1. CORE Level

### Primary Purpose
Expose the minimal explicit tri-state model required for everyday professional decision logic without binary coercion or hidden state collapse.

### What Real Professional Problem Requires This Level?
Handling operations where upstream responses or environmental states are indeterminate (e.g., network timeouts, pending validations, missing fields), and where coercing uncertainty into `True` or `False` causes operational errors (such as duplicate billing, dropped transactions, or corrupted data).

### What Must the Developer Understand?
- Tri-state values: `True`, `False`, and `Unknown`.
- Strict domain separation between native booleans and XoX tri-state values (no implicit promotion or coercion).
- Standard Strong Kleene ($K_3$) logic operators (`NOT`, `AND`, `OR`).
- Identity-of-state equality comparisons.
- Explicit inspection and handling of `Unknown` before making binary control-flow decisions.
- Short-circuit evaluation behavior preserving observable state.

### What Must Remain Hidden?
- Fine-grained provenance lineage, witness structures, and proof graphs.
- Guarded collapse policy configuration and policy combinators.
- Abstract lattice representations and algebraic engine rewrite mechanisms.
- Low-level memory buffers and FFI representations.

### What Additional Capability Becomes Available?
- Safe representation of indeterminate states without exceptions, sentinel values, or nullable bugs.
- Deterministic Kleene evaluation over composite logical expressions.

### What Existing Guarantees Remain Unchanged?
- All foundational invariants: non-collapsing `Unknown`, strict truth-table evaluation, deterministic execution.

### What Common Misuse Indicates the Developer Chose the Wrong Level?
- Treating `Unknown` as a generic runtime exception or error handler.
- Using `Unknown` as a replacement for nullable data fields (`None` / `null`).
- Manually implementing ad-hoc fallback flags and timeout defaults instead of using structured safe collapse policies (indicating a need for **SAFE**).

### What Evidence Justifies Moving to the Next Level (SAFE)?
- The decision becomes sensitive or irreversible (e.g., executing access authorization or triggering automatic infrastructure failover).
- The application requires explicit, auditable collapse policies (e.g., fail-closed defaults) rather than manual conditional checks.
- The decision requires verifying whether an `Unknown` originated from an authoritative source or an unverified probe.

---

## 2. SAFE Level

### Primary Purpose
Provide structured, guarded mechanisms for resolving uncertainty when the origin, validity, authority, or controlled collapse of uncertainty directly impacts sensitive, high-stakes, or irreversible decisions.

### What Real Professional Problem Requires This Level?
Enforcing security boundaries, automated infrastructure remediation, or autonomous agent tool actions where `Unknown` cannot simply be branched on manually, but must be governed by explicit, non-bypassable policy rules (such as fail-closed authorization or guarded fallback strategies).

### What Must the Developer Understand?
- Everything in **CORE**.
- Structured collapse policies (e.g., explicit fail-closed or guarded default resolution).
- Policy boundaries: separating the logical evaluation of uncertainty from the business action policy governing that uncertainty.
- Contextual validation: evaluating whether an operational assertion meets the required safety threshold for a specific action.

### What Must Remain Hidden?
- Internal algebraic theorem-proving representations.
- Distributed consensus epoch clocks and cross-boundary wire replication protocols.
- Complex multi-agent semantic negotiation structures.

### What Additional Capability Becomes Available?
- Guarded policy collapse operators with mandatory explicit defaults.
- Fail-closed and fail-safe execution wrappers for sensitive gates.
- Auditable policy enforcement at authorization and remediation boundaries.

### What Existing Guarantees Remain Unchanged?
- All **CORE** semantics remain identical: `True`, `False`, and `Unknown` retain the exact same truth tables and algebraic invariants.
- No safety rules or domain separations are relaxed.

### What Common Misuse Indicates the Developer Chose the Wrong Level?
- Writing custom, verbose boilerplate around **CORE** primitives to enforce repetitive fail-closed logic across multiple services.
- Attempting to inspect low-level cryptographic signatures or distributed consensus epochs directly (indicating a need for **SEMANTIC**).
- Assuming `SAFE` allows automatic coercion of continuous machine learning confidence scores or token logits into categorical `Unknown`.

### What Evidence Justifies Moving to the Next Level (SEMANTIC)?
- The system coordinates state across distributed consensus boundaries, independent trust domains, or multi-epoch replications.
- The application runtime must track and verify explicit provenance, lineage, or authority certificates across foreign service boundaries.
- The developer is building an extensible framework or runtime engine requiring explicit semantic context manipulation.

---

## 3. SEMANTIC Level

### Primary Purpose
Expose advanced semantic machinery for distributed-state systems, consensus engines, security infrastructure, and extensible runtimes that require fine-grained control over provenance, validity contexts, and authority boundaries.

### What Real Professional Problem Requires This Level?
Resolving distributed consensus ambiguity, split-brain partition detection, epoch-drift validation, and managing provenance across heterogeneous systems where the authority and lineage of an evaluation must be verified before accepting state transitions.

### What Must the Developer Understand?
- Everything in **CORE** and **SAFE**.
- Provenance tracking and semantic lineage models.
- Contextual validity constraints, epoch boundaries, and stale-authority invalidation.
- Boundary translation invariants across external protocol boundaries.

### What Must Remain Hidden?
- Application-specific business heuristics and high-level conversational agent orchestration patterns (these belong in user application space, not XoX core semantics).

### What Additional Capability Becomes Available?
- Explicit provenance attachment and inspection.
- Contextual and temporal validity bounds enforcement.
- Cross-boundary semantic mapping and verification tools for distributed protocol adapters.

### What Existing Guarantees Remain Unchanged?
- All **CORE** logic rules and **SAFE** policy guarantees remain strictly binding.
- SEMANTIC provides deeper introspection and contextual control; it never permits the invalidation or relaxation of canonical evaluation invariants.

### What Common Misuse Indicates the Developer Chose the Wrong Level?
- Utilizing SEMANTIC primitives for ordinary local microservice logic or standard backend web endpoints.
- Treating SEMANTIC as a prestige tier or "more correct" mode of XoX for routine boolean decisions.
- Using provenance structures as a general-purpose logging or distributed tracing framework.

### What Evidence Justifies Remaining at a Lower Level?
- If state evaluation does not cross untrusted distributed boundaries, require provenance verification, or demand explicit epoch coordination, **CORE** or **SAFE** is fully sufficient and strictly preferred.

---

## Persona Alignment & Guidance

The mapping between developer personas and API levels represents professional necessity based on the problem domain, not static restrictions:

1. **Backend / API Developer**: Baseline is **CORE**. Uses explicit tri-state logic to prevent premature boolean failure on remote timeouts and service integrations.
2. **SRE / Platform Engineer**: Baseline is **CORE -> SAFE**. Relies on **SAFE** guarded collapse to prevent telemetry loss from triggering destructive failovers or cascading restarts.
3. **Security / IAM Engineer**: Baseline is **SAFE**. Uses explicit fail-closed policies to guarantee that indeterminate evaluations cannot bypass authentication or authorization barriers.
4. **Data / Streaming Engineer**: Baseline is **CORE -> SAFE**. Uses tri-state transformations to prevent missing or late-arriving schema data from corrupting downstream aggregates.
5. **AI / Agent Systems Developer**: Baseline is **CORE -> SAFE**. Uses **SAFE** policy gates to ensure ambiguous tool-call outcomes or unverified external states fail closed before executing irreversible side effects. *(Framework and runtime creators building extensible agent platforms may require **SEMANTIC**)*.
6. **Distributed Systems Developer**: Primary **SEMANTIC** persona. Uses explicit provenance and boundary invariants to coordinate consensus across network partitions and replication boundaries.

---

## Boundaries for AI and Agent Systems

To preserve the integrity of the XoX semantic model within autonomous agent environments, the following boundaries are strictly enforced across all API levels:

- **No Probabilistic Uncertainty**: XoX API levels do not model, process, or represent model-internal probabilistic uncertainty, token probabilities, softmax logits, or subjective hallucination confidence scores.
- **Operational Uncertainty Only**: XoX is strictly concerned with deterministic operational and environmental uncertainty (e.g., tool execution outcomes, authorization validity, external state verification, and evidence sufficiency).
- **Application Policy Independence**: XoX preserves `Unknown` across tool and agent execution boundaries without collapsing. It never prescribes what action an agent must take upon encountering `Unknown` (e.g., whether to ask for user clarification, retry, defer, or abort). That decision remains the exclusive responsibility of the application policy.
