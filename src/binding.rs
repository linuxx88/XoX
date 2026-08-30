//! PyO3 bindings exposing the XoX CORE API to Python.

use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::types::PyBool;

use crate::core::XoXValue;

/// Python representation of an immutable XoX tri-state logical value.
#[pyclass(name = "XoX", frozen, from_py_object)]
#[derive(Clone, Copy, Debug)]
pub struct PyXoX(pub XoXValue);

#[pymethods]
impl PyXoX {
    /// Inspect if the value is definitively True.
    pub fn is_true(&self) -> bool {
        self.0 == XoXValue::True
    }

    /// Inspect if the value is definitively False.
    pub fn is_false(&self) -> bool {
        self.0 == XoXValue::False
    }

    /// Inspect if the value is Unknown.
    pub fn is_unknown(&self) -> bool {
        self.0 == XoXValue::Unknown
    }

    /// Strong Kleene unary NOT (~).
    pub fn __invert__(&self) -> Self {
        PyXoX(self.0.not())
    }

    /// Strong Kleene lazy conjunction (AND).
    pub fn lazy_and(&self, rhs: &Bound<'_, PyAny>) -> PyResult<Self> {
        if !rhs.is_callable() {
            return Err(PyTypeError::new_err(
                "lazy_and() requires a zero-argument callable returning XoX.",
            ));
        }

        if self.0.should_short_circuit_and() {
            return Ok(PyXoX(XoXValue::False));
        }

        let res = rhs.call0()?;
        let rhs_val = match res.extract::<PyRef<PyXoX>>() {
            Ok(r) => r.0,
            Err(_) => {
                return Err(PyTypeError::new_err(
                    "RHS callable in lazy_and must return an XoX value (xox.TRUE, xox.FALSE, xox.UNKNOWN).",
                ))
            }
        };

        Ok(PyXoX(self.0.and(rhs_val)))
    }

    /// Strong Kleene lazy disjunction (OR).
    pub fn lazy_or(&self, rhs: &Bound<'_, PyAny>) -> PyResult<Self> {
        if !rhs.is_callable() {
            return Err(PyTypeError::new_err(
                "lazy_or() requires a zero-argument callable returning XoX.",
            ));
        }

        if self.0.should_short_circuit_or() {
            return Ok(PyXoX(XoXValue::True));
        }

        let res = rhs.call0()?;
        let rhs_val = match res.extract::<PyRef<PyXoX>>() {
            Ok(r) => r.0,
            Err(_) => {
                return Err(PyTypeError::new_err(
                    "RHS callable in lazy_or must return an XoX value (xox.TRUE, xox.FALSE, xox.UNKNOWN).",
                ))
            }
        };

        Ok(PyXoX(self.0.or(rhs_val)))
    }

    /// Explicit lazy collapse of uncertainty into Python bool.
    pub fn collapse_or(&self, fallback: &Bound<'_, PyAny>) -> PyResult<bool> {
        if !fallback.is_callable() {
            return Err(PyTypeError::new_err(
                "collapse_or() requires a zero-argument callable returning Python bool.",
            ));
        }

        match self.0 {
            XoXValue::True => Ok(true),
            XoXValue::False => Ok(false),
            XoXValue::Unknown => {
                let res = fallback.call0()?;
                if !res.is_exact_instance_of::<PyBool>() {
                    return Err(PyTypeError::new_err(
                        "Collapse fallback callable must return an exact Python bool (True or False).",
                    ));
                }
                res.extract::<bool>()
            }
        }
    }

    /// Explicitly block Python truthiness evaluation for all states.
    pub fn __bool__(&self) -> PyResult<bool> {
        Err(PyTypeError::new_err(
            "Cannot use XoX value directly in boolean context. Use '.is_true()', pattern match, or '.collapse_or(lambda: fallback)' to resolve uncertainty explicitly.",
        ))
    }

    /// State-identity equality. Comparing with Python bool evaluates to False.
    pub fn __eq__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        if let Ok(other_xox) = other.extract::<PyRef<PyXoX>>() {
            Ok(self.0 == other_xox.0)
        } else {
            Ok(false)
        }
    }

    pub fn __ne__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        Ok(!self.__eq__(other)?)
    }

    /// Consistent hashing for dict/set collection isolation.
    pub fn __hash__(&self) -> isize {
        match self.0 {
            XoXValue::True => 1_000_003,
            XoXValue::False => 1_000_004,
            XoXValue::Unknown => 1_000_005,
        }
    }

    pub fn __repr__(&self) -> &'static str {
        match self.0 {
            XoXValue::True => "xox.TRUE",
            XoXValue::False => "xox.FALSE",
            XoXValue::Unknown => "xox.UNKNOWN",
        }
    }
}

/// Canonical single Bool-to-XoX ingress function.
#[pyfunction]
pub fn from_bool(value: &Bound<'_, PyAny>) -> PyResult<PyXoX> {
    if !value.is_exact_instance_of::<PyBool>() {
        return Err(PyTypeError::new_err(
            "xox.from_bool() requires an exact Python bool (True or False).",
        ));
    }
    let b: bool = value.extract()?;
    if b {
        Ok(PyXoX(XoXValue::True))
    } else {
        Ok(PyXoX(XoXValue::False))
    }
}
