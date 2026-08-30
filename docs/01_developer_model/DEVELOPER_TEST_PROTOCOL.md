# XoX Developer Usability & Misuse Testing Protocol

This document establishes the official protocol for testing whether practicing developers can understand, adopt, and correctly apply XoX without relying on hidden project knowledge, theoretical logic machinery, or unsafe semantic shortcuts.

---

## 1. Protocol Purpose & Foundational Principles

The objective of this protocol is to empirically measure developer comprehension, cognitive burden, API level selection, and misuse resistance across realistic engineering tasks.

### Core Principles

1. **Decisions Over Terminology**: Test understanding through realistic professional design and implementation decisions, not terminology recall or abstract logic definitions.
2. **Zero Theoretical Prerequisite**: A developer must be able to succeed without reading or understanding XoXLang formal research, lattice algebra, or proof theory.
3. **Blinded Evaluation**: Never reveal the expected answer or nudge the target API level before or during a task attempt.
4. **Dual Measurement**: Measure both semantic correctness and cognitive cost (e.g., reasoning time, documentation lookups, correction loops).
5. **Taxonomic Separation of Failures**: Strictly distinguish between semantic failures, security failures, cognitive model failures, and tooling/UX failures.
6. **Error Pattern Weighting**: Repeated conceptual mistakes carry higher diagnostic weight than single accidental typographical or syntax slips.
7. **Complexity Penalization**: Selecting a higher API level than necessary is a meaningful failure signal (violates Principle of Least Complexity).
8. **Critical Shortcut Detection**: Silent boolean collapse or unprincipled coercion of `Unknown` is treated as a critical failure.
9. **Lowest Sufficient Level Validation**: The protocol explicitly evaluates whether participants identify and stay at the lowest sufficient level (`CORE` vs. `SAFE` vs. `SEMANTIC`).
10. **Observed Behavior Over Stated Confidence**: Objective behavioral evidence (actions taken, code written, invariants preserved) strictly supersedes self-reported confidence.
11. **Anti-Memorization & Unseen Variants**: Success on a previously documented canonical example alone does not establish understanding; participants must resolve unseen structurally equivalent variants with different surface vocabulary.
12. **Domain Isolation**: Specialized domain terminology must not act as a barrier to testing XoX comprehension; domain scaffolding must provide neutral vocabulary without revealing expected XoX reasoning.
13. **Tooling Isolation**: External environment, build-system, or framework friction must be isolated from semantic evaluation; unobserved reasoning due to external blockers results in an `INCONCLUSIVE` task result, not a failure.

---

## 2. Test Environment & Execution Rules

To ensure reproducible and unbiased evaluation, testing sessions must adhere to strict operational constraints:

- **No Coaching During Initial Attempt**: The facilitator/evaluator must remain strictly passive during the initial attempt; no hints, guiding questions, or clarifications on correct logic are permitted.
- **First Interpretation Recording**: Record the participant's immediate first interpretation, structural assumptions, and baseline reasoning prior to any hint or feedback.
- **Controlled Documentation Access**: Permit access only to standard developer-facing reference documentation (excluding research papers and formal logic specifications) and log every lookup event and query string.
- **Progression & Remediation Logging**: When an error occurs, record whether the participant self-corrects independently, self-corrects after consulting documentation, or requires direct remediation.
- **Primary Persona Alignment**: Test participants primarily with scenarios aligned with their actual professional persona. Do not require specialized external domain expertise outside their domain merely to test XoX comprehension.
- **Neutral Domain Scaffolding**: For unfamiliar transfer domains, provide minimal, neutral background vocabulary. Scaffolding must strictly describe the domain mechanics without hinting at XoX truth states or policies. Missing domain knowledge must never be counted as a `SEMANTIC_FAILURE` or `COGNITIVE_FAILURE`.
- **Infrastructure & Tooling Scaffolding**: Provide minimal, pre-configured execution harnesses and scaffolding to remove framework, build-system, or mocking-library friction. Measure `xox_reasoning_time` strictly separate from `environment_setup_time`.
- **Handling External Tooling Blockers**: Record `external_tooling_blocker` independently. If an external tooling blocker prevents observing XoX reasoning, mark the task as `INCONCLUSIVE`.
- **Transfer & Variant Verification**: Evaluators must administer at least one unseen structurally equivalent variant per task family, using distinct surface vocabulary and domain nouns not found in documentation.
- **Behavioral Verification**: Never accept keyword repetition (e.g., repeating "Unknown is not False") as proof of understanding without observing correct handling in code or architecture design.
- **Sample Diversity & Cross-Persona Normalization**: Usability findings must be drawn from diverse cohorts rather than single experts. Raw performance metrics must not be compared across personas unless scenario difficulty and domain complexity have been normalized.
- **Isolation from Performance**: Semantic correctness and cognitive clarity must be measured independently of execution performance, runtime benchmarks, or FFI overhead.

---

## 3. Persona Coverage Matrix

The protocol requires testing across all six adopted XoX developer personas with normalized, role-appropriate evaluation paths:

| Persona | Primary Focus Area | Key Cognitive Challenge | Baseline Level |
| :--- | :--- | :--- | :--- |
| **Backend / API Developer** | Remote timeouts, microservice choreography, idempotency | Distinguishing transport timeout from operational truth state; avoiding premature `bool` cast. | `CORE` |
| **SRE / Platform Engineer** | Health probes, telemetry loss, automated circuit-breakers | Preventing missing metrics from triggering cascading restarts or black-hole traffic routing. | `CORE -> SAFE` |
| **Security / IAM Engineer** | Access control evaluation, claims resolution, fail-closed gates | Ensuring indeterminate credentials fail closed without corrupting the distinction between deny and unknown. | `SAFE` |
| **Data / Streaming Engineer** | Event streams, late-arriving schema fields, pipeline aggregations | Preventing coercion of unresolved fields to `False`/`0` from corrupting analytical aggregates. | `CORE -> SAFE` |
| **AI / Agent Systems Developer** | Tool execution results, action verification, autonomous guardrails | Separating operational tool uncertainty from model confidence; enforcing policy separation. | `CORE -> SAFE` *(SEMANTIC for framework engines)* |
| **Distributed Systems Developer** | Consensus state, epoch drift, split-brain recovery, cross-boundary lineage | Reasoning about provenance, valid authority boundaries, and non-collapsing state across wire protocols. | `SEMANTIC` |

---

## 4. Test Categories

Every testing evaluation is structured across seven standardized categories:

1. **`TEST-UNDERSTANDING`**: Verify whether the developer correctly internalizes the core mental model: `Unknown` represents an unestablished truth state for a specific decision.
2. **`TEST-UNKNOWN-DISTINCTION`**: Verify that the developer clearly distinguishes `Unknown` from `False`, `None`/`null`, exceptions/errors, timeouts, pending workflows, and probabilistic metrics.
3. **`TEST-POLICY-SEPARATION`**: Verify that the developer separates the logical truth state from the application's action policy (e.g., retry, clarify, fail-closed, escalate, defer).
4. **`TEST-LEVEL-SELECTION`**: Verify whether the developer identifies and selects the lowest sufficient level (`CORE`, `SAFE`, or `SEMANTIC`) without unnecessary escalation.
5. **`TEST-MISUSE-RESISTANCE`**: Verify whether the developer resists unsafe shortcuts (e.g., ad-hoc `bool` coercion, premature collapse) when placed under realistic time pressure or API impedance.
6. **`TEST-TRANSFER`**: Verify that the developer can transfer the learned mental model to an unfamiliar engineering domain without re-training.
7. **`TEST-DIAGNOSTIC-USABILITY`**: Verify whether error diagnostics, type hints, and explanations enable fast, autonomous repair without theoretical logic references.

---

## 5. Canonical Task Families & Variant Requirements

The 10 canonical test families define the invariant semantic properties tested across all evaluations. For each family, the evaluator must present an unseen variant (`variant_id`) that uses distinct domain vocabulary and never copies literal phrasing from `COGNITIVE_MODEL.md`.

### DEVTEST-FAM-01: Operational Interruption vs. Propositional Truth
- **Invariant Semantic Property**: A transport or operational fault (timeout, disconnect, packet drop) is an execution event, not the truth value itself; the proposition whose truth could not be established becomes `Unknown`.
- **Category**: `TEST-UNKNOWN-DISTINCTION`, `TEST-UNDERSTANDING`
- **Canonical Illustrative Scenario**: Remote payment gateway status check times out during checkout validation.
- **Unseen Structural Variant Example**: An IoT telemetry ingest service experiences an HTTP 504 gateway timeout while checking if a remote valve closure sensor acknowledged completion.
- **Success Criteria**: Developer isolates the unestablished proposition ("valve is closed") as `Unknown` without assuming the valve failed to close (`False`) or treating the timeout exception itself as the data value.

### DEVTEST-FAM-02: Indeterminate Fact vs. Reaction Policy
- **Invariant Semantic Property**: `Unknown` carries zero intrinsic reaction semantics (neither allow, deny, retry, nor abort); application policy exclusively owns the reaction to uncertainty.
- **Category**: `TEST-POLICY-SEPARATION`, `TEST-MISUSE-RESISTANCE`
- **Canonical Illustrative Scenario**: IAM policy evaluator encounters an unverified user attribute due to a directory cache miss.
- **Unseen Structural Variant Example**: A medical device dosage controller evaluates patient allergy status when the remote electronic health record database is offline.
- **Success Criteria**: Developer maintains explicit separation between the unverified medical fact (`Unknown`) and the fail-safe emergency policy without mutating truth into `False`.

### DEVTEST-FAM-03: Absence of Data vs. Truth Uncertainty
- **Invariant Semantic Property**: Data container absence (`None`, `null`, empty collection, 0 rows) represents missing records or references, distinct from an unestablished logical proposition.
- **Category**: `TEST-UNKNOWN-DISTINCTION`
- **Canonical Illustrative Scenario**: A database lookup for a user preference record returns zero rows.
- **Unseen Structural Variant Example**: A query for an optional discount coupon code returns `None` in an order summary struct.
- **Success Criteria**: Developer models missing optional data with language nullability (`None`) and reserves XoX `Unknown` strictly for unresolved logical decision states.

### DEVTEST-FAM-04: Continuous Probability vs. Categorical Truth
- **Invariant Semantic Property**: Continuous probabilistic metrics (model confidence, token logits, sensor variance) are statistical values, not categorical XoX truth states.
- **Category**: `TEST-UNKNOWN-DISTINCTION`
- **Canonical Illustrative Scenario**: An LLM classifier outputs an intent prediction with a 0.42 confidence score.
- **Unseen Structural Variant Example**: A radar obstacle detector outputs a 0.68 Bayesian posterior probability of an obstacle ahead.
- **Success Criteria**: Developer maintains the numerical confidence score in numerical data types and avoids coercing arbitrary probability thresholds into categorical XoX states.

### DEVTEST-FAM-05: Unverified Side-Effect Action in Autonomous Systems
- **Invariant Semantic Property**: When an automated action or tool invocation lacks verified completion, the operational completion proposition is `Unknown`, while candidate responses (retry, clarify, escalate, defer, refuse) remain application-layer policies.
- **Category**: `TEST-POLICY-SEPARATION`, `TEST-UNDERSTANDING`
- **Canonical Illustrative Scenario**: An autonomous agent invokes a database modification tool and loses connection before receipt of ACK.
- **Unseen Structural Variant Example**: An automated CI/CD pipeline triggers an external container deployment script that exits abruptly without status output.
- **Success Criteria**: Developer tracks the deployment status proposition as `Unknown` and routes to an explicit policy handler rather than hardcoding retry or failure directly into the logic state.

### DEVTEST-FAM-06: Boundary Type Impedance vs. Semantic Integrity
- **Invariant Semantic Property**: The requirement of a downstream binary API (`bool`) does not justify unprincipled or silent boolean coercion; conversion across boundaries requires an explicit, documented policy boundary.
- **Category**: `TEST-MISUSE-RESISTANCE`
- **Canonical Illustrative Scenario**: Downstream client library method expects a native `bool` argument when local state is unresolved XoX.
- **Unseen Structural Variant Example**: An analytics event emitter schema requires a boolean `is_verified` flag, but upstream KYC verification is still pending.
- **Success Criteria**: Developer introduces an explicit guarded policy conversion boundary rather than using implicit language coercion (`bool(x)`).

### DEVTEST-FAM-07: Final Truth Equivalence vs. Observable Execution Semantics
- **Invariant Semantic Property**: Identical final truth values under Strong Kleene logic do not guarantee operational or behavioral equivalence when expressions evaluate side-effecting operations.
- **Category**: `TEST-UNDERSTANDING`, `TEST-MISUSE-RESISTANCE`
- **Canonical Illustrative Scenario**: Two logical expressions produce the same truth table result, but one short-circuits an RPC while the other evaluates all sub-expressions eagerly.
- **Unseen Structural Variant Example**: Evaluating `A OR B` where `A` is `True` and `B` writes an audit log entry vs evaluating `B OR A`.
- **Success Criteria**: Developer accounts for evaluation order, short-circuit preservation, and side-effect guarantees.

### DEVTEST-FAM-08: Tri-State Logic Sufficiency (CORE Selection)
- **Invariant Semantic Property**: Routine non-sensitive tri-state decisions require only basic Strong Kleene logic without policy guardrails or provenance lineage.
- **Category**: `TEST-LEVEL-SELECTION`
- **Canonical Illustrative Scenario**: Evaluating whether an inbound request contains a valid, invalid, or indeterminate session token.
- **Unseen Structural Variant Example**: A search filter engine evaluating whether an item matches, does not match, or has unindexed metadata for a user query.
- **Expected Level**: **CORE**
- **Success Criteria**: Developer selects `CORE` tri-state logic without escalating to `SAFE` or `SEMANTIC`.

### DEVTEST-FAM-09: Sensitive Guarded Remediation (SAFE Selection)
- **Invariant Semantic Property**: Irreversible, sensitive, or high-stakes actions requiring auditable, fail-closed, or guarded collapse policies demand `SAFE`.
- **Category**: `TEST-LEVEL-SELECTION`, `TEST-POLICY-SEPARATION`
- **Canonical Illustrative Scenario**: An automated node drain and termination script executing guarded fallback on ambiguous health state.
- **Unseen Structural Variant Example**: An automated financial trading bot executing portfolio liquidation only when margin call conditions are established, requiring guarded auditable policy collapse.
- **Expected Level**: **SAFE**
- **Success Criteria**: Developer selects `SAFE` for guarded policy collapse and auditable boundaries, resisting manual un-guarded `CORE` branching.

### DEVTEST-FAM-10: Cross-Boundary Authority & Provenance (SEMANTIC Selection)
- **Invariant Semantic Property**: Coordinating state across distributed consensus boundaries, independent trust domains, epoch drift, or multi-replica lineages requires `SEMANTIC`.
- **Category**: `TEST-LEVEL-SELECTION`, `TEST-TRANSFER`
- **Canonical Illustrative Scenario**: Coordinating distributed consensus decisions across asynchronous replication boundaries with epoch drift and authority validation.
- **Unseen Structural Variant Example**: A cross-datacenter state sync engine verifying cryptographic provenance and lease epoch validity before committing ledger updates.
- **Expected Level**: **SEMANTIC**
- **Success Criteria**: Developer identifies the necessity of provenance tracking and epoch boundaries, correctly selecting `SEMANTIC`.

---

## 6. Observation Metrics & Data Collection

During each test execution, observers must record the following objective data points:

1. `xox_reasoning_time`: Seconds elapsed actively reasoning about and implementing XoX logic (isolated from environment setup).
2. `environment_setup_time`: Seconds spent on IDE setup, harness compilation, or local dependencies.
3. `documentation_lookups`: Total count and specific queries executed in developer documentation.
4. `incorrect_assumptions`: Explicit mistaken assertions voiced or encoded during development.
5. `repeated_errors`: Number of times the same conceptual mistake is made after an initial failure across variants.
6. `silent_unknown_collapses`: Instances where `Unknown` was coerced into `True`/`False` without an explicit policy boundary.
7. `wrong_level_selections`: Instances where an inappropriate API level was chosen for the task.
8. `unnecessary_level_escalations`: Choosing `SAFE` or `SEMANTIC` when `CORE` was fully sufficient.
9. `policy_truth_confusions`: Conflating the truth state with the action policy (e.g., defining `Unknown` as "must retry").
10. `unknown_none_confusions`: Conflating `Unknown` with `None`, `null`, or empty data sets.
11. `unknown_probability_confusions`: Attempting to use `Unknown` as a numerical threshold or confidence score.
12. `requests_for_theory_before_use`: Participant asking for mathematical/formal logic explanations before being able to write code.
13. `corrections_required`: Count of interventions or retries needed before achieving a correct solution.
14. `domain_scaffolding_provided`: Record of any neutral domain glossaries provided to the participant.
15. `external_tooling_blocker`: Record of any third-party framework, compiler, or environment issue encountered.
16. `successful_transfer_to_new_scenario`: Binary outcome indicating whether the participant correctly solves an equivalent unseen variant in a new domain without prompting.

---

## 7. Failure Taxonomy

Observed participant outcomes are categorized across four failure classes and an external blocker state:

```
                  ┌───────────────────────────────┐
                  │      Observed Deviation       │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┬────────────────────────┐
         ▼                        ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ SEMANTIC_FAILURE │    │ SECURITY_FAILURE │    │ COGNITIVE_FAILURE│    │    UX_FAILURE    │
│ Violates truth   │    │ Uncertainty      │    │ Flawed mental    │    │ Unclear errors,  │
│ table, Kleene    │    │ enables unsafe / │    │ model despite    │    │ friction, or doc │
│ rules, or state  │    │ unauthorized     │    │ accidental       │    │ ambiguity.       │
│ preservation.    │    │ execution path.  │    │ correct output.  │    │                  │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │ TOOLING_BLOCKER  │
                        │ Unrelated build/ │
                        │ framework error  │
                        │ -> INCONCLUSIVE  │
                        └──────────────────┘
```

- **`SEMANTIC_FAILURE`**: The participant implements or expects behavior inconsistent with canonical XoX invariants (e.g., violating Strong Kleene logic, mutating truth tables, or ignoring short-circuit guarantees).
- **`SECURITY_FAILURE`**: The participant's interpretation or code allows uncertainty to bypass a security boundary or trigger an unauthorized action (e.g., defaulting an unverified credential to allow).
- **`COGNITIVE_FAILURE`**: The participant forms an incorrect mental model (e.g., equating `Unknown` with `None` or an HTTP 500 error), even if their immediate code snippet produces the desired outcome by coincidence. Missing external domain knowledge or vocabulary confusion must **never** be classified as a cognitive or semantic failure.
- **`UX_FAILURE`**: The participant understands the semantic concept, but naming conventions, error messages, compiler diagnostics, or API ergonomy cause avoidable friction or errors.
- **`TOOLING_BLOCKER`**: An external framework, mocking library, build error, or environment crash prevents observing XoX reasoning. The task result is classified as **`INCONCLUSIVE`** and is omitted from semantic failure rate calculations.

### Multi-Failure Classification Rules

When an observed participant error exhibits multiple manifestations across the taxonomy, evaluators must apply the following causal classification protocol:

1. **Single Primary Root Cause**: Every failure observation must record at most one `primary_failure_type` representing the best-supported causal root cause (`SEMANTIC_FAILURE`, `SECURITY_FAILURE`, `COGNITIVE_FAILURE`, `UX_FAILURE`, or `null`).
2. **Evidence-Backed Secondary Manifestations**: Zero or more `secondary_failure_types` (array) may record observable consequences or additional independently supported classifications.
3. **No Obscuring of Root Cause**: A secondary classification must never replace, downgrade, or obscure the primary causal interpretation.
4. **No Speculative Tagging**: Do not infer a secondary type merely because an outcome could theoretically have been unsafe or problematic; every recorded type must be backed by observed behavioral evidence.
5. **Independent Critical Failures**: Critical failure disqualifications remain independently recordable and may coexist alongside primary and secondary failure types.

#### Classification Examples

- **Example 1 (Cognitive Cause with Security Consequence)**:
  - *Scenario*: Participant believes `Unknown` literally means `deny` and therefore denies access in an authorization gate.
  - *Primary*: `"primary_failure_type": "COGNITIVE_FAILURE"`
  - *Secondary*: `"secondary_failure_types": ["SECURITY_FAILURE"]"`
  - *Reasoning*: The incorrect mental model (believing truth state equals policy action) is the causal defect; the safe security action is its downstream manifestation.
- **Example 2 (UX Friction with Correct Mental Model)**:
  - *Scenario*: Participant understands `Unknown` correctly, but ambiguous documentation phrasing leads to an avoidable incorrect API-level selection.
  - *Primary*: `"primary_failure_type": "UX_FAILURE"`
  - *Secondary*: `"secondary_failure_types": []`
  - *Reasoning*: The mental model is sound; documentation/interface friction directly caused the mistake.
- **Example 3 (Direct Semantic Breach)**:
  - *Scenario*: Participant understands the tri-state model but deliberately violates an understood semantic invariant during code implementation.
  - *Primary*: `"primary_failure_type": "SEMANTIC_FAILURE"`
  - *Secondary*: `"secondary_failure_types": []`
  - *Reasoning*: Observed implementation violates semantics without evidence of a flawed conceptual mental model.

### Critical Failures (Disqualifying Events)

Any occurrence of the following represents a critical protocol failure:
1. Treating `Unknown` as `False` by default.
2. Treating `Unknown` as `True` by default.
3. Treating `Unknown` as `None`, `null`, or generic exception without evaluating a proposition.
4. Treating probabilistic model confidence as an XoX `Unknown` value.
5. Assuming explicit collapse is automatically semantically valid without an authorized policy.
6. Assuming XoX dictates application reactions (e.g., retry, deny, clarify, escalate, defer, refuse).
7. Choosing a lower API level specifically to evade safety guardrails or validation checks.
8. Using `SEMANTIC` because it appears more advanced rather than because problem requirements demand it.
9. Assuming identical final truth states guarantee identical observable program side effects.

---

## 8. Success Metrics & Pass Criteria

A participant or cohort evaluation passes when all of the following criteria are met:

- **Clear Articulation**: Participant explains `Unknown` in ordinary engineering language without relying on formal logic jargon.
- **Accurate Distinction**: Participant reliably distinguishes `Unknown` from `False`, `None`/`null`, errors, timeouts, pending workflows, and probabilities across all scenarios.
- **Rigorous Separation**: Participant cleanly separates truth evaluation from action policies.
- **Optimal Level Selection**: Participant consistently selects the lowest sufficient level (`CORE`, `SAFE`, `SEMANTIC`).
- **Zero Theory Dependency**: Participant completes tasks without requiring exposure to XoXLang formal research or lattice theory.
- **Successful Transfer on Unseen Variants**: Participant correctly resolves unseen variants across unfamiliar engineering domains with zero coaching.
- **Zero Critical Failures**: No critical failure occurs across any evaluated task.
- **Decreasing Friction**: Frequency of documentation lookups and corrections decreases over time.

---

## 9. Result Data Model & Reporting

Test findings must be structured using the following formal schema:

### Per-Task Record
```json
{
  "task_family_id": "DEVTEST-FAM-01",
  "variant_id": "VAR-IOT-VALVE-01",
  "persona": "Backend / API Developer",
  "expected_level_if_applicable": "CORE",
  "domain_scaffolding_provided": "Standard IoT valve telemetry glossary (neutral)",
  "external_tooling_blocker": null,
  "xox_reasoning_time_sec": 75,
  "environment_setup_time_sec": 30,
  "first_response": "string",
  "correctness": true,
  "primary_failure_type": null,
  "secondary_failure_types": [],
  "documentation_lookups": 1,
  "corrections_required": 0,
  "task_result": "PASS",
  "notes": "Participant correctly mapped unacknowledged valve closure to Unknown."
}
```
*(Task result must be one of: `PASS`, `FRICTION`, `FAIL`, or `INCONCLUSIVE`)*

### Per-Participant Summary
```json
{
  "participant_id": "P-042",
  "persona": "Security / IAM Engineer",
  "unknown_model_correct": true,
  "policy_separation_correct": true,
  "level_selection_correct": true,
  "transfer_success": true,
  "critical_failures": 0,
  "repeated_failures": 0,
  "inconclusive_tasks": 0,
  "overall_result": "PASS"
}
```
*(Overall result must be one of: `PASS`, `FRICTION`, or `FAIL`)*

### Aggregate Evaluation Report
```json
{
  "cohort_id": "COHORT-2026-Q3",
  "total_participants": 24,
  "pass_rate": 0.92,
  "critical_failure_rate": 0.0,
  "inconclusive_task_rate": 0.02,
  "median_xox_reasoning_time_sec": 95,
  "median_environment_setup_time_sec": 35,
  "median_documentation_lookups": 2,
  "wrong_level_selection_rate": 0.04,
  "unnecessary_escalation_rate": 0.04,
  "repeated_error_rate": 0.0,
  "transfer_success_rate": 0.96
}
```
