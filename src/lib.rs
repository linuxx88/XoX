//! XoX epistemic tri-state logic library and Python extension module.

pub mod binding;
pub mod core;

use pyo3::prelude::*;

use crate::binding::{from_bool, PyXoX};
use crate::core::XoXValue;

/// XoX core Python module.
#[pymodule]
fn xox(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyXoX>()?;
    m.add_function(wrap_pyfunction!(from_bool, m)?)?;

    // Canonical singleton constants
    m.add("TRUE", PyXoX(XoXValue::True))?;
    m.add("FALSE", PyXoX(XoXValue::False))?;
    m.add("UNKNOWN", PyXoX(XoXValue::Unknown))?;

    Ok(())
}
