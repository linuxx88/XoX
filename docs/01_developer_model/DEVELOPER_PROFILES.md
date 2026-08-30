# XoX Developer Profiles & Problem Model

This document establishes the official developer personas for XoX, mapping real-world professional contexts and operational decisions to the appropriate levels of XoX capability.

## Foundation & Guiding Principles

- **Levels of Need, Not Skill**: `CORE`, `SAFE`, and `SEMANTIC` represent levels of required semantic precision, not developer seniority or competence. An experienced engineer building a high-throughput cache may need only `CORE`, while an engineer implementing a sensitive access guardrail legitimately relies on `SAFE`.
- **Knowledge Monotonicity**: Concepts learned at lower tiers remain strictly valid at higher tiers. More access never means fewer guarantees (`XOX-GUAR-004`).
- **Selective Applicability**: XoX is not intended for every developer or every boolean decision. It is designed specifically for domains where collapsing operational uncertainty into binary truth causes operational, financial, or security failure.
- **Application Policy Independence**: XoX does not dictate how an application or agent must resolve or react to `Unknown`; it guarantees that `Unknown` cannot silently collapse into a binary default before an explicit, authorized application policy handles it.

---

## Official Personas

### 1. Backend / API Developer

- **Professional Context**: Builds backend web services, orchestrates microservices, integrates third-party REST/gRPC endpoints, and validates request payloads.
- **Real Problem**: Handling upstream dependencies that return network timeouts, gateway drops, or indeterminate intermediate states during state-changing operations.
- **Decision the Developer Must Make**: Whether to commit a local state transition, return a terminal success/failure HTTP code, or trigger compensatory reconciliation.
- **Why Bool is Insufficient**: Standard `bool` forces an immediate binary decision (`True`/`False`), turning a network timeout into an assumed failure that can trigger duplicate billing charges or dropped orders.
- **Minimum XoX Concepts Needed**: `True`, `False`, `Unknown`, and basic domain separation between `Bool` and XoX values.
- **Complexity That Should Remain Hidden**: Custom witness structures, world-state tracking, fine-grained provenance graphs, and constraint-satisfaction engines.
- **Likely API Level**: **CORE**
- **Common Misuse or Confusion**: Treating `Unknown` as a general error/exception or using it as a replacement for nullable fields (`None`).

---

### 2. SRE / Platform Engineer

- **Professional Context**: Automates infrastructure health checks, canary rollouts, autoscaling policies, and circuit-breaking mechanisms.
- **Real Problem**: Intermittent telemetry loss, flapping network probes, or degraded nodes reporting conflicting or absent health metrics during rolling updates.
- **Decision the Developer Must Make**: Whether to terminate an instance, route traffic away from a cluster, or trigger automatic failover.
- **Why Bool is Insufficient**: Binary health probes interpret metric silence as unhealthy (`False`), causing cascading restart storms, or as healthy (`True`), routing live user traffic into black holes.
- **Minimum XoX Concepts Needed**: Tri-state logic, guarded collapse policies with explicit defaults, and evaluation order preservation.
- **Complexity That Should Remain Hidden**: Internal algebraic rewrite engines, low-level FFI representations, and formal logical proof objects.
- **Likely API Level**: **CORE -> SAFE**
- **Common Misuse or Confusion**: Assuming `Unknown` represents an infrastructure failure rather than an absence of conclusive health evidence.

---

### 3. Security / IAM Engineer

- **Professional Context**: Implements access control engines (RBAC/ABAC), token validation pipelines, and sensitive authorization gates.
- **Real Problem**: Evaluating permissions when directory services suffer partial outages, token caches are stale, or contextual claims are missing from the request.
- **Decision the Developer Must Make**: Whether to grant access, deny access, or route the request to step-up authentication.
- **Why Bool is Insufficient**: Inverted boolean evaluation (`not allowed`) can inadvertently grant access when an evaluation returns indeterminate or error states, creating critical security bypasses.
- **Minimum XoX Concepts Needed**: Fail-closed evaluation guarantees, explicit non-collapsing `Unknown`, and safe policy collapse rules.
- **Complexity That Should Remain Hidden**: Abstract mathematical lattice representations and distributed epoch clocks.
- **Likely API Level**: **SAFE**
- **Common Misuse or Confusion**: Believing that access denial requires `False`, rather than recognizing that `Unknown` must fail closed to prevent unauthorized execution.

---

### 4. Data / Streaming Engineer

- **Professional Context**: Constructs high-throughput stream processing pipelines (e.g., Kafka, Flink), ETL workflows, and real-time feature transformations.
- **Real Problem**: Processing records with late-arriving schema fields, out-of-order event streams, or partial tombstone entries.
- **Decision the Developer Must Make**: Whether to route a record downstream, quarantine it in a dead-letter queue, or include it in an active windowed aggregation.
- **Why Bool is Insufficient**: Coercing missing or unestablished fields to default `False` or `0` silently corrupts analytical aggregates, metrics, and downstream machine learning models.
- **Minimum XoX Concepts Needed**: Tri-state field values, non-collapsing transport across pipeline boundaries, and deterministic tri-state combinators.
- **Complexity That Should Remain Hidden**: Multi-agent interaction policies, interactive clarification protocols, and complex authorization tokens.
- **Likely API Level**: **CORE -> SAFE**
- **Common Misuse or Confusion**: Conflating `Unknown` with SQL `NULL` or treating `Unknown` as a third business data category rather than state uncertainty.

---

### 5. AI / Agent Systems Developer

- **Professional Context**: Develops autonomous agent workflows, LLM tool-calling orchestrators, and automated agentic decision systems.
- **Real Problem**: Managing operational and decision uncertainty around agent actions—such as determining whether a tool call succeeded, whether a requested action is authorized, whether external environment state has been verified, or whether retrieved evidence is sufficient to proceed. (Strictly distinct from model-internal probabilistic uncertainty or token logits).
- **Decision the Developer Must Make**: Whether the agent should execute a consequential tool action, commit environment modifications, ask for user clarification, gather more evidence, retry safely, escalate, defer, or refuse the sensitive action.
- **Why Bool is Insufficient**: Forcing ambiguous tool executions or unverified external states into binary `True`/`False` causes agents to hallucinate definitive task completion or execute unauthorized, irreversible side effects.
- **Minimum XoX Concepts Needed**: Explicit `Unknown` tracking across tool-call boundaries, fail-closed policy gates, and explicit collapse policies for action triggers.
- **Complexity That Should Remain Hidden**: Deep logical theorem proving and low-level memory-managed FFI buffers.
- **Likely API Level**: **CORE -> SAFE** *(Agent framework and runtime authors building extensible orchestration platforms may require **SEMANTIC**)*.
- **Common Misuse or Confusion**: Expecting XoX to automatically dictate what the agent should do on `Unknown`, or attempting to model continuous token confidence scores as XoX `Unknown`.

---

### 6. Distributed Systems Developer

- **Professional Context**: Implements distributed consensus adapters, state machine replication, transaction coordinators, and cross-region synchronization engines.
- **Real Problem**: Managing split-brain network partitions, partial quorum acknowledgments, epoch drift, and indeterminate consensus state.
- **Decision the Developer Must Make**: Whether a distributed consensus state is conclusively achieved or whether state reconciliation, election, or rollback is necessary.
- **Why Bool is Insufficient**: Simple booleans cannot distinguish between an acknowledged negative response and an unacknowledged/indeterminate quorum state across network boundaries.
- **Minimum XoX Concepts Needed**: Fine-grained provenance, contextual validity constraints, stale-authority detection, and explicit boundary invariants.
- **Complexity That Should Remain Hidden**: Application-level business heuristics and high-level agent conversational protocols.
- **Likely API Level**: **Primary SEMANTIC persona**
- **Common Misuse or Confusion**: Using `Unknown` as a replacement for network retry loops rather than using it to formally represent indeterminate consensus states.
