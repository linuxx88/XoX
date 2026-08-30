# XoX Cognitive Model: The Developer Mental Model

This document establishes the minimal, stable mental model required for developers to reason correctly about XoX across `CORE`, `SAFE`, and `SEMANTIC` without exposing internal logical machinery or implementation complexity.

---

## 1. The Core Mental Model

When a developer encounters an XoX value, they should hold exactly one foundational concept:

> **`Unknown` means the truth required for the current decision has not been established as `True` or `False`.**

From this single foundation, nine principles define correct developer reasoning:

1. **`Unknown` is Not `False`**: An unestablished outcome is not a confirmed negative. Treating metric silence as node failure or a network timeout as a failed payment causes destructive system failures.
2. **`Unknown` is Not Data or Exception**: `Unknown` is not `None`, `null`, a raised exception, a pending business workflow state, or a generic "third option". It represents an absence of conclusive evidence regarding a specific decision.
3. **Bool and XoX are Distinct Domains**: Native language booleans represent binary facts (`True`/`False`). XoX represents decision states where uncertainty is an explicit, first-class possibility. Crossing the boundary between them must always be explicit.
4. **No Silent Collapse for Convenience**: Developers must never silently coerce unresolved uncertainty into a binary default merely because an `if` statement or API parameter expects a `bool`.
5. **Separation of Uncertainty and Policy**: XoX preserves decision-relevant uncertainty; the application policy decides what action to execute in response to that uncertainty.
6. **Execution Behavior Matters**: Evaluation order and short-circuit behavior matter as much as final truth values. Valid short-circuit evaluation preserves observable execution semantics and side effects.
7. **Semantic Stability Across Levels**: `CORE`, `SAFE`, and `SEMANTIC` expose progressively more contextual control, but the meaning and algebraic rules of `True`, `False`, and `Unknown` never change.
8. **Encapsulated Machinery**: Developers reason about operational truth and consequences, not internal logical theorem provers, lattice structures, or memory buffers.
9. **Principle of the Lowest Level**: The simplest API level sufficient to safely resolve the developer's professional problem is always the correct level.

---

## 2. Fundamental Questions & Answers

### What should a developer think when they see an XoX value?
"This value represents a verified fact (`True`), a disproven fact (`False`), or a fact whose truth has not been established (`Unknown`). I must not guess or collapse it until an explicit policy is applied."

### What information does `Unknown` communicate?
`Unknown` communicates that the system lacks sufficient evidence, response data, or verification to assert whether a specific condition is definitively true or false.

### What does `Unknown` deliberately not communicate?
- It does **not** communicate *why* the condition is unestablished (e.g., whether caused by network timeout, missing database row, or unread sensor).
- It does **not** communicate *what action to take* (e.g., whether to retry, fail closed, or alert).
- It does **not** communicate a *statistical probability* or likelihood score.

### Why must Bool and XoX remain mentally distinct?
Language booleans enforce a closed-world assumption: anything not proven true is assumed false (or vice versa). XoX models an open world where truth may be indeterminate. Mixing the two implicitly re-introduces the very silent assumptions and bugs that XoX exists to prevent.

### When is explicit collapse legitimate?
Explicit collapse is legitimate only at an intentional decision boundary where the application has an authorized, explicit business policy for handling unresolved uncertainty (such as failing closed at an authorization gate or choosing a default fallback route in an ingress proxy).

### Who owns the policy decision after `Unknown` is preserved?
The **application or system policy** exclusively owns the decision. XoX guarantees that uncertainty is preserved and never silently coerced, but XoX never dictates whether the application should retry, prompt a user, route to dead-letter queues, or refuse access.

### What remains invariant as a developer moves from CORE to SAFE to SEMANTIC?
The truth values (`True`, `False`, `Unknown`), Strong Kleene logic rules, domain separation from `bool`, and non-collapsing invariants remain 100% identical. Higher levels only add tools to inspect provenance or configure guarded policy collapse.

### What internal machinery should a normal developer never need to learn?
Developers should never need to understand:
- Internal lattice representations and formal proof terms.
- Algebraic rewrite engines and simplification graphs.
- Low-level FFI buffers, memory layouts, or PyO3 runtime bindings.
- Multi-world modal logic or ontological constraint tokens.

### What mental mistakes are most likely to cause misuse?
Confusing `Unknown` with an error/exception, assuming `Unknown` means "deny" or "retry", and attempting to use XoX as a logging framework or confidence scoring system.

---

## 3. Common Incorrect Mental Models (Anti-Patterns)

| Incorrect Mental Model | Why It Is Dangerous | Correct Mental Model |
| :--- | :--- | :--- |
| **"Unknown means probably false."** | Causes premature negative decisions, dropping valid transactions or falsely flagging healthy systems as failed. | `Unknown` is non-binary; it has zero intrinsic directional bias toward `True` or `False`. |
| **"Unknown means something failed."** | Conflates an operational outage with a lack of conclusive evidence (e.g., an un-evaluated rule is not a failed rule). | `Unknown` indicates unestablished state, not necessarily an infrastructure or program failure. |
| **"Unknown is equivalent to None or null."** | Leads developers to use `Unknown` as a missing data container rather than a logical decision state. | `None` represents missing data/references; `Unknown` represents unresolved logical truth. |
| **"Unknown means retry."** | Hardcodes a specific operational action into the meaning of truth. | Retry is one possible application policy; `Unknown` is the truth state that policy evaluates. |
| **"Unknown means deny."** | Conflates security policy (fail-closed) with logical truth. | Deny is an authorization policy; `Unknown` is the unverified credential state that triggers that policy. |
| **"Unknown means ask the user."** | Assumes an interactive agent or human-in-the-loop context for all uncertainty. | Clarification is an agent-level policy choice, not a semantic property of `Unknown`. |
| **"Unknown means low model confidence."** | Conflates probabilistic ML token scores with deterministic logical facts. | `Unknown` is categorical and logical, not a thresholded continuous probability score. |
| **"SAFE is more correct than CORE."** | Creates false prestige hierarchies and unnecessary code complexity. | `CORE` is complete and fully correct for basic tri-state logic; `SAFE` is needed only for sensitive guarded policies. |
| **"SEMANTIC is the expert version of XoX."** | Promotes overuse of advanced distributed machinery for simple services. | `SEMANTIC` is specialized tooling for distributed state and lineage, not a badge of seniority. |
| **"A developer can ignore Unknown if they ultimately need a Bool."** | Reintroduces silent boolean collapse bugs at the boundary. | If a `bool` is ultimately needed, the collapse must be explicitly governed by an authorized policy. |
| **"Equivalent truth values imply equivalent program behavior."** | Ignores short-circuiting and side effects during logical evaluation. | Evaluation order and short-circuit preservation are part of observable execution semantics. |

---

## 4. Boundaries for AI and Autonomous Agent Systems

When applying XoX within AI agent architectures, developers must maintain strict cognitive boundaries:

- **Operational vs. Statistical Uncertainty**: An agent tool execution or verification step returns `True`, `False`, or `Unknown` based on deterministic operational evidence. XoX does not represent or evaluate token logits, model confidence, or hallucination probabilities.
- **Policies are Not Semantics**: When an agent encounters `Unknown`, possible actions include:
  - Requesting user clarification
  - Gathering additional evidence / executing secondary tools
  - Retrying with exponential backoff
  - Escalating to a human supervisor
  - Defers or safely refusing the action
  *All of these are application-level policies.* `Unknown` simply asserts that the precondition for action is currently unestablished.
- **Preservation Across Boundaries**: An agent orchestrator must pass `Unknown` through tool-call interfaces without coercion, allowing the governing agent policy to choose the safe next step.
