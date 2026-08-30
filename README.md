# XoX

Tri-state epistemic uncertainty engine preserving explicit `True`, `False`, and `Unknown` decision semantics in Python.

---

## The Problem

Standard boolean logic provides only two states: `True` and `False`. When a system evaluates an assertion—such as whether an account is authorized, whether a remote record exists, or whether an external precondition holds—the state of that assertion is often indeterminate due to incomplete or unreachable information.

Coercing an unestablished proposition into `False` (or `True`) conflates **known falsity** with **absence of knowledge**. This silent collapse can introduce subtle defects, improper fallbacks, or security vulnerabilities where systems act on assumptions rather than established truth.

XoX provides a principled tri-state logical model where uncertainty is preserved across function boundaries, combined using Strong Kleene logic, and collapsed into Python booleans only when the application explicitly defines a fallback policy.

---

## Semantic Model

XoX represents three distinct, immutable logical states:

- **`xox.TRUE`**: The proposition is definitively established as true.
- **`xox.FALSE`**: The proposition is definitively refuted as false.
- **`xox.UNKNOWN`**: The proposition has not been established as true or false.

`Unknown` carries no intrinsic bias toward `True` or `False`.

### What `UNKNOWN` Is Not

To prevent semantic confusion, `xox.UNKNOWN` has strict boundaries:
- **Not `None`**: It represents an unresolved proposition, not the absence of an object.
- **Not an exception**: Runtime errors, system failures, and contract violations remain standard Python exceptions.
- **Not a pending async state**: It is an evaluated outcome, not an incomplete future or promise.
- **Not a timeout**: A timeout is an execution event, whereas `UNKNOWN` is a state of knowledge.
- **Not probabilistic confidence**: It indicates that truth has not been established, not a probability score.
- **Not an action directive**: `UNKNOWN` does not intrinsically mean retry, deny, allow, wait, fail, or default. Any action taken in response to uncertainty is defined strictly by caller policy.

---

## Installation

```bash
pip install project-xox
```

> **Note**: The package distribution name on PyPI is `project-xox`, while the Python import name is `xox`.

---

## Basic Usage

```python
import xox

# Canonical value constants
t = xox.TRUE
f = xox.FALSE
u = xox.UNKNOWN

# State inspection
if t.is_true():
    print("Definitely True")

if f.is_false():
    print("Definitely False")

if u.is_unknown():
    print("State is indeterminate")
```

---

## Strict Domain Separation & Truthiness Prohibition

Python `bool` and `xox.XoX` belong to strictly separated domains. Crossing between them requires explicit operations.

### Truthiness is Prohibited

XoX values prohibit direct boolean coercion (`__bool__`). Evaluating an `XoX` instance in an `if`, `while`, `bool()`, `and`, `or`, or `not` context raises a `TypeError`:

```python
val = xox.UNKNOWN

# Prohibited - raises TypeError:
# if val:
#     ...
# bool(val)
```

This prevents uncertainty from silently collapsing into boolean control flow.

### Domain Equality Isolation

XoX values never compare equal to native Python booleans:

```python
assert (xox.TRUE == True) is False
assert (xox.FALSE == False) is False
assert (xox.UNKNOWN == False) is False
```

---

## Ingress: Bool to XoX

To bring a Python boolean into the XoX domain, use `xox.from_bool()`:

```python
xox_val = xox.from_bool(True)   # returns xox.TRUE
xox_val = xox.from_bool(False)  # returns xox.FALSE
```

`xox.from_bool()` accepts only exact Python `bool` instances (`True` or `False`). Non-boolean values (including `1`, `0`, `None`, or truthy objects) raise a `TypeError`.

---

## Strong Kleene Logic Operations

XoX implements standard Strong Kleene ($K_3$) logic with host-level short-circuiting.

### Unary NOT (`~`)

The bitwise inversion operator `~` performs Strong Kleene negation:

```python
assert ~xox.TRUE == xox.FALSE
assert ~xox.FALSE == xox.TRUE
assert ~xox.UNKNOWN == xox.UNKNOWN
```

### Lazy Conjunction (`lazy_and`) & Disjunction (`lazy_or`)

Python evaluates binary operator operands (`&`, `|`) eagerly. To guarantee real short-circuit evaluation without evaluating unneeded branches, conjunction and disjunction require zero-argument callables:

```python
# Conjunction: FALSE short-circuits; RHS is never called
result = xox.FALSE.lazy_and(lambda: expensive_query())  # returns xox.FALSE

# Disjunction: TRUE short-circuits; RHS is never called
result = xox.TRUE.lazy_or(lambda: expensive_query())    # returns xox.TRUE

# When LHS cannot determine the outcome, RHS is executed exactly once:
result = xox.UNKNOWN.lazy_and(lambda: xox.TRUE)         # returns xox.UNKNOWN
result = xox.UNKNOWN.lazy_or(lambda: xox.TRUE)          # returns xox.TRUE
```

- **Short-circuiting**: If the outcome is determined by the LHS, the RHS callable executes **zero** times.
- **Evaluation**: When needed, the RHS callable executes **exactly once** and must return an `XoX` instance.
- **Exceptions**: Exceptions raised inside evaluated RHS callables propagate normally as standard Python exceptions.

---

## Egress: Collapsing Uncertainty to Python Bool

When application code must interface with a native boolean API, collapse the `XoX` value using `collapse_or()` with an explicit fallback callable:

```python
# TRUE and FALSE resolve directly without invoking fallback
assert xox.TRUE.collapse_or(lambda: False) is True
assert xox.FALSE.collapse_or(lambda: True) is False

# UNKNOWN executes the fallback callable exactly once
decision = xox.UNKNOWN.collapse_or(lambda: False)  # returns False
```

- **Caller-Owned Policy**: The fallback callable represents an application policy decision (such as fail-closed or optimistic pass), not newly discovered truth.
- **Lazy Execution**: The fallback callable is evaluated only when the value is `xox.UNKNOWN`.
- **Type Contract**: The fallback callable must return an exact Python `bool` (`True` or `False`). Returning any other type raises a `TypeError`.

---

## Realistic Example: External Verification Gate

```python
import xox
import logging

def verify_remote_entitlement(user_id: str) -> xox.XoX:
    """Queries an upstream service; returns UNKNOWN if indeterminate."""
    try:
        response = call_auth_service(user_id)
        if response.status == "AUTHORIZED":
            return xox.TRUE
        elif response.status == "DENIED":
            return xox.FALSE
        else:
            # Service responded, but entitlement status is indeterminate
            return xox.UNKNOWN
    except NetworkTimeoutError:
        # Runtime transport failure is handled by application logic
        return xox.UNKNOWN

def handle_user_request(user_id: str):
    entitlement = verify_remote_entitlement(user_id)

    # 1. Explicit three-way branch
    if entitlement.is_true():
        grant_access()
    elif entitlement.is_false():
        deny_access("Explicitly denied by auth policy")
    else:  # entitlement.is_unknown()
        # The reaction to UNKNOWN is owned by the application:
        queue_for_manual_review(user_id)

    # 2. Or explicit policy collapse at a boolean boundary (e.g., fail-closed)
    def fail_closed_policy() -> bool:
        logging.warning("Entitlement indeterminate for %s; applying fail-closed default.", user_id)
        return False

    can_proceed = entitlement.collapse_or(fail_closed_policy)
    if can_proceed:
        execute_privileged_task()
```

---

## Project Status: CORE 0.1.0

XoX `0.1.0` delivers the minimal public `CORE` semantic surface:
- Singleton constants: `xox.TRUE`, `xox.FALSE`, `xox.UNKNOWN`.
- Canonical ingress: `xox.from_bool()`.
- State inspection: `.is_true()`, `.is_false()`, `.is_unknown()`, and `==`.
- Strong Kleene logic: `~` (NOT), `.lazy_and()`, and `.lazy_or()`.
- Explicit egress: `.collapse_or()`.
- Strict domain separation and truthiness blocking.

Advanced capabilities (such as auditable policy tokens, evidence provenance tracking, and distributed consensus negotiation) are intentionally outside the scope of `CORE` and are not included in this release.

---

## Supported Platforms & Scope

- **Python Interpreters:** CPython 3.12, 3.13, and 3.14 (version-specific CPython extension wheels).
- **Supported Platform:** Linux x86_64.
- **Binary Compatibility Baseline:** `manylinux_2_34_x86_64` (glibc 2.34+).
- **Source Build MSRV:** Rust 1.83+.
- **Unclaimed / Unsupported:** macOS, Windows, Linux aarch64, musllinux, PyPy, GraalPy, and free-threaded CPython builds are not currently claimed or supported.

> **Note**: The binary compatibility baseline reflects the currently audited distribution artifact floor, not an intrinsic semantic limitation of XoX logic.

---

## Documentation

- [Normative Public CORE API Specification](docs/04_api/CORE_API.md)
- [Foundational Guarantees & Philosophy](docs/00_foundations/GUARANTEES.md)
- [Runtime & Portability Model](docs/03_runtime/PORTABILITY_MODEL.md)

---

## License

XoX is licensed under the [Apache-2.0 License](LICENSE).
