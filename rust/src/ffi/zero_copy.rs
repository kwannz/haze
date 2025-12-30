//! 零拷贝 NumPy 数组工具函数
//!
//! 这个模块提供辅助函数用于在 Python 和 Rust 之间进行零拷贝数据传输。
//! 使用 pyo3-numpy 的 PyReadonlyArray1 和 PyArray1 类型实现高效的数据交换。

use numpy::PyArray1;
use pyo3::prelude::*;

/// 将 Option<Vec<f64>> 转换为 PyArray1，错误时返回 NaN 数组
///
/// # 参数
///
/// * `py` - Python GIL 引用
/// * `result` - 计算结果，None 表示计算失败
/// * `len` - 输出数组长度
///
/// # 返回
///
/// 成功时返回计算结果的 NumPy 数组，失败时返回全 NaN 数组
///
/// # 性能
///
/// 这个函数仅在输出时拷贝一次数据（Rust Vec → NumPy Array），
/// 相比传统方法减少了 50% 的拷贝次数。
///
/// # PyO3 0.27 API
///
/// 使用 Bound<PyArray1> 包装类型以符合新版本 PyO3 的生命周期管理
pub fn to_pyarray_or_nan<'py>(
    py: Python<'py>,
    result: Option<Vec<f64>>,
    len: usize,
) -> PyResult<Bound<'py, PyArray1<f64>>> {
    match result {
        Some(vec) => Ok(PyArray1::from_vec(py, vec)),
        None => Ok(PyArray1::from_vec(py, vec![f64::NAN; len])),
    }
}

/// 将 2 个 Vec<f64> 转换为 2 个 PyArray1 (用于 Stochastic 等多输出指标)
///
/// # 参数
///
/// * `py` - Python GIL 引用
/// * `result` - 2 元组计算结果，None 表示计算失败
/// * `len` - 输出数组长度
///
/// # 返回
///
/// 成功时返回 2 个计算结果的 NumPy 数组，失败时返回 2 个全 NaN 数组
///
/// # 用例
///
/// 用于返回 2 个输出值的指标，例如:
/// - Stochastic Oscillator (k_line, d_line)
/// - Aroon (aroon_up, aroon_down)
/// - DMI (plus_di, minus_di)
/// - StochRSI (stochrsi_k, stochrsi_d)
///
/// # PyO3 0.27 API
///
/// 使用 Bound<PyArray1> 二元组返回类型
pub fn to_pyarray2_or_nan<'py>(
    py: Python<'py>,
    result: Option<(Vec<f64>, Vec<f64>)>,
    len: usize,
) -> PyResult<(Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>)> {
    match result {
        Some((v1, v2)) => Ok((
            PyArray1::from_vec(py, v1),
            PyArray1::from_vec(py, v2),
        )),
        None => {
            let nan_vec = vec![f64::NAN; len];
            Ok((
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec),
            ))
        }
    }
}

/// 将 3 个 Vec<f64> 转换为 3 个 PyArray1 (用于 MACD 等多输出指标)
///
/// # 参数
///
/// * `py` - Python GIL 引用
/// * `result` - 3 元组计算结果，None 表示计算失败
/// * `len` - 输出数组长度
///
/// # 返回
///
/// 成功时返回 3 个计算结果的 NumPy 数组，失败时返回 3 个全 NaN 数组
///
/// # 用例
///
/// 用于返回多个输出值的指标，例如:
/// - MACD (macd_line, signal_line, histogram)
/// - Bollinger Bands (upper, middle, lower)
/// - DMI with ADX (plus_di, minus_di, adx)
///
/// # PyO3 0.27 API
///
/// 使用 Bound<PyArray1> 三元组返回类型
pub fn to_pyarray3_or_nan<'py>(
    py: Python<'py>,
    result: Option<(Vec<f64>, Vec<f64>, Vec<f64>)>,
    len: usize,
) -> PyResult<(Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>)> {
    match result {
        Some((v1, v2, v3)) => Ok((
            PyArray1::from_vec(py, v1),
            PyArray1::from_vec(py, v2),
            PyArray1::from_vec(py, v3),
        )),
        None => {
            let nan_vec = vec![f64::NAN; len];
            Ok((
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec),
            ))
        }
    }
}

/// 将 4 个 Vec<f64> 转换为 4 个 PyArray1 (用于 Ichimoku Cloud 等多输出指标)
///
/// # 参数
///
/// * `py` - Python GIL 引用
/// * `result` - 4 元组计算结果，None 表示计算失败
/// * `len` - 输出数组长度
///
/// # 返回
///
/// 成功时返回 4 个计算结果的 NumPy 数组，失败时返回 4 个全 NaN 数组
///
/// # 用例
///
/// 用于返回 4 个输出值的指标，例如:
/// - Ichimoku Cloud (tenkan, kijun, senkou_a, senkou_b)
///
/// # PyO3 0.27 API
///
/// 使用 Bound<PyArray1> 四元组返回类型
pub fn to_pyarray4_or_nan<'py>(
    py: Python<'py>,
    result: Option<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)>,
    len: usize,
) -> PyResult<(
    Bound<'py, PyArray1<f64>>,
    Bound<'py, PyArray1<f64>>,
    Bound<'py, PyArray1<f64>>,
    Bound<'py, PyArray1<f64>>,
)> {
    match result {
        Some((v1, v2, v3, v4)) => Ok((
            PyArray1::from_vec(py, v1),
            PyArray1::from_vec(py, v2),
            PyArray1::from_vec(py, v3),
            PyArray1::from_vec(py, v4),
        )),
        None => {
            let nan_vec = vec![f64::NAN; len];
            Ok((
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec),
            ))
        }
    }
}

/// 将 5 个 Vec<f64> 转换为 5 个 PyArray1 (用于 Pivot Points 等多输出指标)
///
/// # 参数
///
/// * `py` - Python GIL 引用
/// * `result` - 5 元组计算结果，None 表示计算失败
/// * `len` - 输出数组长度
///
/// # 返回
///
/// 成功时返回 5 个计算结果的 NumPy 数组，失败时返回 5 个全 NaN 数组
///
/// # 用例
///
/// 用于返回 5 个输出值的指标，例如:
/// - Pivot Points (pivot, r1, r2, s1, s2)
///
/// # PyO3 0.27 API
///
/// 使用 Bound<PyArray1> 五元组返回类型
pub fn to_pyarray5_or_nan<'py>(
    py: Python<'py>,
    result: Option<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)>,
    len: usize,
) -> PyResult<(
    Bound<'py, PyArray1<f64>>,
    Bound<'py, PyArray1<f64>>,
    Bound<'py, PyArray1<f64>>,
    Bound<'py, PyArray1<f64>>,
    Bound<'py, PyArray1<f64>>,
)> {
    match result {
        Some((v1, v2, v3, v4, v5)) => Ok((
            PyArray1::from_vec(py, v1),
            PyArray1::from_vec(py, v2),
            PyArray1::from_vec(py, v3),
            PyArray1::from_vec(py, v4),
            PyArray1::from_vec(py, v5),
        )),
        None => {
            let nan_vec = vec![f64::NAN; len];
            Ok((
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec.clone()),
                PyArray1::from_vec(py, nan_vec),
            ))
        }
    }
}
