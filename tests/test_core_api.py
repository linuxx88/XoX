"""Normal valid-path and adversarial misuse tests for the adopted XoX CORE API."""

import pytest
import xox


# ===========================================================================
# 1. Normal Tests
# ===========================================================================


def test_canonical_values_exist_and_are_distinct():
    assert xox.TRUE is not None
    assert xox.FALSE is not None
    assert xox.UNKNOWN is not None
    assert xox.TRUE != xox.FALSE
    assert xox.TRUE != xox.UNKNOWN
    assert xox.FALSE != xox.UNKNOWN
    assert repr(xox.TRUE) == "xox.TRUE"
    assert repr(xox.FALSE) == "xox.FALSE"
    assert repr(xox.UNKNOWN) == "xox.UNKNOWN"


def test_ingress_from_bool_true():
    val = xox.from_bool(True)
    assert val == xox.TRUE
    assert val.is_true() is True


def test_ingress_from_bool_false():
    val = xox.from_bool(False)
    assert val == xox.FALSE
    assert val.is_false() is True


@pytest.mark.parametrize(
    "val, expected_true, expected_false, expected_unknown",
    [
        (xox.TRUE, True, False, False),
        (xox.FALSE, False, True, False),
        (xox.UNKNOWN, False, False, True),
    ],
)
def test_state_inspection(val, expected_true, expected_false, expected_unknown):
    assert val.is_true() is expected_true
    assert val.is_false() is expected_false
    assert val.is_unknown() is expected_unknown


@pytest.mark.parametrize(
    "operand, expected_result",
    [
        (xox.TRUE, xox.FALSE),
        (xox.FALSE, xox.TRUE),
        (xox.UNKNOWN, xox.UNKNOWN),
    ],
)
def test_strong_kleene_not(operand, expected_result):
    assert ~operand == expected_result


@pytest.mark.parametrize(
    "lhs, rhs_val, expected_result",
    [
        (xox.TRUE, xox.TRUE, xox.TRUE),
        (xox.TRUE, xox.FALSE, xox.FALSE),
        (xox.TRUE, xox.UNKNOWN, xox.UNKNOWN),
        (xox.FALSE, xox.TRUE, xox.FALSE),
        (xox.FALSE, xox.FALSE, xox.FALSE),
        (xox.FALSE, xox.UNKNOWN, xox.FALSE),
        (xox.UNKNOWN, xox.TRUE, xox.UNKNOWN),
        (xox.UNKNOWN, xox.FALSE, xox.FALSE),
        (xox.UNKNOWN, xox.UNKNOWN, xox.UNKNOWN),
    ],
)
def test_strong_kleene_lazy_and_table(lhs, rhs_val, expected_result):
    assert lhs.lazy_and(lambda: rhs_val) == expected_result


def test_lazy_and_invoked_exactly_once():
    call_count = 0

    def rhs():
        nonlocal call_count
        call_count += 1
        return xox.TRUE

    result = xox.TRUE.lazy_and(rhs)
    assert result == xox.TRUE
    assert call_count == 1


def test_lazy_and_skips_rhs_on_false():
    invoked = False

    def rhs():
        nonlocal invoked
        invoked = True
        return xox.TRUE

    result = xox.FALSE.lazy_and(rhs)
    assert result == xox.FALSE
    assert invoked is False


@pytest.mark.parametrize(
    "lhs, rhs_val, expected_result",
    [
        (xox.TRUE, xox.TRUE, xox.TRUE),
        (xox.TRUE, xox.FALSE, xox.TRUE),
        (xox.TRUE, xox.UNKNOWN, xox.TRUE),
        (xox.FALSE, xox.TRUE, xox.TRUE),
        (xox.FALSE, xox.FALSE, xox.FALSE),
        (xox.FALSE, xox.UNKNOWN, xox.UNKNOWN),
        (xox.UNKNOWN, xox.TRUE, xox.TRUE),
        (xox.UNKNOWN, xox.FALSE, xox.UNKNOWN),
        (xox.UNKNOWN, xox.UNKNOWN, xox.UNKNOWN),
    ],
)
def test_strong_kleene_lazy_or_table(lhs, rhs_val, expected_result):
    assert lhs.lazy_or(lambda: rhs_val) == expected_result


def test_lazy_or_invoked_exactly_once():
    call_count = 0

    def rhs():
        nonlocal call_count
        call_count += 1
        return xox.FALSE

    result = xox.FALSE.lazy_or(rhs)
    assert result == xox.FALSE
    assert call_count == 1


def test_lazy_or_skips_rhs_on_true():
    invoked = False

    def rhs():
        nonlocal invoked
        invoked = True
        return xox.FALSE

    result = xox.TRUE.lazy_or(rhs)
    assert result == xox.TRUE
    assert invoked is False


def test_collapse_or_true_skips_fallback():
    invoked = False

    def fallback():
        nonlocal invoked
        invoked = True
        return False

    res = xox.TRUE.collapse_or(fallback)
    assert res is True
    assert invoked is False


def test_collapse_or_false_skips_fallback():
    invoked = False

    def fallback():
        nonlocal invoked
        invoked = True
        return True

    res = xox.FALSE.collapse_or(fallback)
    assert res is False
    assert invoked is False


def test_collapse_or_unknown_returns_fallback_true():
    call_count = 0

    def fallback():
        nonlocal call_count
        call_count += 1
        return True

    res = xox.UNKNOWN.collapse_or(fallback)
    assert res is True
    assert call_count == 1


def test_collapse_or_unknown_returns_fallback_false():
    call_count = 0

    def fallback():
        nonlocal call_count
        call_count += 1
        return False

    res = xox.UNKNOWN.collapse_or(fallback)
    assert res is False
    assert call_count == 1


def test_xox_state_equality():
    assert xox.TRUE == xox.from_bool(True)
    assert xox.FALSE == xox.from_bool(False)
    assert xox.UNKNOWN == xox.UNKNOWN
    assert xox.TRUE != xox.FALSE
    assert xox.TRUE != xox.UNKNOWN
    assert xox.FALSE != xox.UNKNOWN


def test_xox_hash_and_collection_stability():
    s = {xox.TRUE, xox.FALSE, xox.UNKNOWN}
    assert len(s) == 3
    assert xox.from_bool(True) in s
    assert xox.from_bool(False) in s
    assert xox.UNKNOWN in s

    d = {xox.TRUE: "T", xox.FALSE: "F", xox.UNKNOWN: "U"}
    assert d[xox.from_bool(True)] == "T"
    assert d[xox.from_bool(False)] == "F"
    assert d[xox.UNKNOWN] == "U"


# ===========================================================================
# 2. Adversarial & Misuse Tests
# ===========================================================================


class CustomTestException(Exception):
    """Custom exception to verify error propagation without alteration."""


# --- Truthiness & Bool Coercion Blocking ---


@pytest.mark.parametrize("state", [xox.TRUE, xox.FALSE, xox.UNKNOWN])
def test_adv_bool_coercion_raises_typeerror(state):
    with pytest.raises(TypeError) as excinfo:
        bool(state)
    assert "Cannot use XoX value directly in boolean context" in str(excinfo.value)


@pytest.mark.parametrize("state", [xox.TRUE, xox.FALSE, xox.UNKNOWN])
def test_adv_if_evaluation_raises_typeerror(state):
    with pytest.raises(TypeError) as excinfo:
        if state:
            pass
    assert "Cannot use XoX value directly in boolean context" in str(excinfo.value)


# --- Strict Ingress Rejections ---


@pytest.mark.parametrize(
    "invalid_input",
    [
        1,
        0,
        -1,
        2,
        None,
        "",
        "True",
        "False",
        [],
        [True],
        {},
        {"val": True},
        (True,),
        object(),
    ],
)
def test_adv_from_bool_rejects_non_bool(invalid_input):
    with pytest.raises(TypeError) as excinfo:
        xox.from_bool(invalid_input)
    assert "requires an exact Python bool" in str(excinfo.value)


# --- Equality & Hash Isolation from Python Bool ---


def test_adv_equality_domain_isolation():
    assert (xox.TRUE == True) is False  # noqa: E712
    assert (xox.TRUE != True) is True  # noqa: E712
    assert (xox.FALSE == False) is False  # noqa: E712
    assert (xox.FALSE != False) is True  # noqa: E712
    assert (xox.UNKNOWN == True) is False  # noqa: E712
    assert (xox.UNKNOWN == False) is False  # noqa: E712
    assert (xox.UNKNOWN == None) is False  # noqa: E711


def test_adv_collection_isolation_from_bool():
    d = {True: "bool_true", False: "bool_false", xox.TRUE: "xox_true", xox.FALSE: "xox_false"}
    assert len(d) == 4
    assert d[True] == "bool_true"
    assert d[False] == "bool_false"
    assert d[xox.TRUE] == "xox_true"
    assert d[xox.FALSE] == "xox_false"

    s = {True, False, xox.TRUE, xox.FALSE, xox.UNKNOWN}
    assert len(s) == 5
    assert True in s
    assert False in s
    assert xox.TRUE in s
    assert xox.FALSE in s
    assert xox.UNKNOWN in s


# --- Mixed Operators Blocking ---


def test_adv_bitwise_operators_not_supported():
    with pytest.raises(TypeError):
        _ = xox.TRUE & xox.FALSE  # type: ignore

    with pytest.raises(TypeError):
        _ = xox.TRUE | xox.FALSE  # type: ignore

    with pytest.raises(TypeError):
        _ = xox.TRUE & True  # type: ignore

    with pytest.raises(TypeError):
        _ = False | xox.UNKNOWN  # type: ignore


# --- Lazy Logic Short-Circuiting & Non-Execution ---


def test_adv_lazy_and_skip_mutation_and_error():
    mutated = False

    def bad_callable():
        nonlocal mutated
        mutated = True
        raise CustomTestException("Should never be reached")

    res = xox.FALSE.lazy_and(bad_callable)
    assert res == xox.FALSE
    assert mutated is False


def test_adv_lazy_or_skip_mutation_and_error():
    mutated = False

    def bad_callable():
        nonlocal mutated
        mutated = True
        raise CustomTestException("Should never be reached")

    res = xox.TRUE.lazy_or(bad_callable)
    assert res == xox.TRUE
    assert mutated is False


def test_adv_skipped_invalid_return_type_not_inspected():
    # When skipped, the return value of the callable is never inspected or called
    assert xox.FALSE.lazy_and(lambda: "INVALID_RETURN_TYPE") == xox.FALSE
    assert xox.TRUE.lazy_or(lambda: 12345) == xox.TRUE


# --- Lazy Logic Invocations & Type Contracts ---


def test_adv_lazy_and_required_invoked_exactly_once():
    count = 0

    def rhs():
        nonlocal count
        count += 1
        return xox.UNKNOWN

    res = xox.TRUE.lazy_and(rhs)
    assert res == xox.UNKNOWN
    assert count == 1


def test_adv_lazy_or_required_invoked_exactly_once():
    count = 0

    def rhs():
        nonlocal count
        count += 1
        return xox.UNKNOWN

    res = xox.FALSE.lazy_or(rhs)
    assert res == xox.UNKNOWN
    assert count == 1


@pytest.mark.parametrize("invalid_ret", [True, False, 1, 0, None, "xox.TRUE", object()])
def test_adv_lazy_and_rejects_non_xox_return(invalid_ret):
    with pytest.raises(TypeError) as excinfo:
        xox.TRUE.lazy_and(lambda: invalid_ret)
    assert "must return an XoX value" in str(excinfo.value)


@pytest.mark.parametrize("invalid_ret", [True, False, 1, 0, None, "xox.TRUE", object()])
def test_adv_lazy_or_rejects_non_xox_return(invalid_ret):
    with pytest.raises(TypeError) as excinfo:
        xox.FALSE.lazy_or(lambda: invalid_ret)
    assert "must return an XoX value" in str(excinfo.value)


@pytest.mark.parametrize("non_callable", [xox.TRUE, True, False, 123, None, "string"])
def test_adv_lazy_logic_rejects_non_callable_arg(non_callable):
    with pytest.raises(TypeError) as exc_and:
        xox.TRUE.lazy_and(non_callable)
    assert "requires a zero-argument callable" in str(exc_and.value)

    with pytest.raises(TypeError) as exc_or:
        xox.FALSE.lazy_or(non_callable)
    assert "requires a zero-argument callable" in str(exc_or.value)


def test_adv_lazy_and_propagates_callable_exception():
    def raising_rhs():
        raise CustomTestException("Direct error in RHS")

    with pytest.raises(CustomTestException) as excinfo:
        xox.TRUE.lazy_and(raising_rhs)
    assert "Direct error in RHS" in str(excinfo.value)


def test_adv_lazy_or_propagates_callable_exception():
    def raising_rhs():
        raise CustomTestException("Direct error in RHS")

    with pytest.raises(CustomTestException) as excinfo:
        xox.FALSE.lazy_or(raising_rhs)
    assert "Direct error in RHS" in str(excinfo.value)


# --- Collapse Fallback Adversarial Contracts ---


def test_adv_collapse_known_skips_raising_or_mutating_fallback():
    mutated = False

    def bad_fallback():
        nonlocal mutated
        mutated = True
        raise CustomTestException("Should not be called")

    assert xox.TRUE.collapse_or(bad_fallback) is True
    assert xox.FALSE.collapse_or(bad_fallback) is False
    assert mutated is False


def test_adv_collapse_skipped_invalid_return_not_inspected():
    assert xox.TRUE.collapse_or(lambda: "INVALID_RETURN") is True
    assert xox.FALSE.collapse_or(lambda: xox.TRUE) is False


def test_adv_collapse_unknown_invoked_exactly_once():
    count = 0

    def fallback():
        nonlocal count
        count += 1
        return False

    res = xox.UNKNOWN.collapse_or(fallback)
    assert res is False
    assert count == 1


@pytest.mark.parametrize(
    "invalid_ret",
    [
        xox.TRUE,
        xox.FALSE,
        xox.UNKNOWN,
        0,
        1,
        None,
        "True",
        "False",
        [],
        object(),
    ],
)
def test_adv_collapse_rejects_non_bool_return(invalid_ret):
    with pytest.raises(TypeError) as excinfo:
        xox.UNKNOWN.collapse_or(lambda: invalid_ret)
    assert "must return an exact Python bool" in str(excinfo.value)


@pytest.mark.parametrize("non_callable", [True, False, xox.FALSE, 0, None, "lambda"])
def test_adv_collapse_rejects_non_callable_arg(non_callable):
    with pytest.raises(TypeError) as excinfo:
        xox.UNKNOWN.collapse_or(non_callable)
    assert "requires a zero-argument callable" in str(excinfo.value)


def test_adv_collapse_propagates_fallback_exception():
    def raising_fallback():
        raise CustomTestException("Fallback error")

    with pytest.raises(CustomTestException) as excinfo:
        xox.UNKNOWN.collapse_or(raising_fallback)
    assert "Fallback error" in str(excinfo.value)
