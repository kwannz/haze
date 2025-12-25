
// ==================== 周期指标包装 (Hilbert Transform) ====================
#[pyfunction]
fn py_ht_dcperiod(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::ht_dcperiod(&values))
}

#[pyfunction]
fn py_ht_dcphase(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::ht_dcphase(&values))
}

#[pyfunction]
fn py_ht_phasor(values: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::ht_phasor(&values))
}

#[pyfunction]
fn py_ht_sine(values: Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>)> {
    Ok(indicators::ht_sine(&values))
}

#[pyfunction]
fn py_ht_trendmode(values: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(indicators::ht_trendmode(&values))
}
