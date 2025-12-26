// polars_compat.rs - Polars DataFrame integration (stub)
//
// The optional `polars` feature is kept so `cfg(feature = "polars")` remains a
// valid configuration and `cargo check --all-features` stays green.
//
// Full Polars integration is currently disabled because the required external
// dependencies are intentionally not included in this crate.

use pyo3::prelude::*;

/// Register Polars-related functions into the PyO3 module.
///
/// This is currently a no-op stub.
pub fn register_polars_functions(_m: &Bound<'_, PyModule>) -> PyResult<()> {
    Ok(())
}
