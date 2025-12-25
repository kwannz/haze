// types.rs - 核心数据类型定义
#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(not(feature = "python"))]
type PyResult<T> = Result<T, String>;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// K线数据结构（OHLCV）
#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct Candle {
#[cfg_attr(feature = "python", pyo3(get, set))]
    pub timestamp: i64,  // Unix 毫秒时间戳

#[cfg_attr(feature = "python", pyo3(get, set))]
    pub open: f64,

#[cfg_attr(feature = "python", pyo3(get, set))]
    pub high: f64,

#[cfg_attr(feature = "python", pyo3(get, set))]
    pub low: f64,

#[cfg_attr(feature = "python", pyo3(get, set))]
    pub close: f64,

#[cfg_attr(feature = "python", pyo3(get, set))]
    pub volume: f64,
}

#[cfg_attr(feature = "python", pymethods)]
impl Candle {
#[cfg_attr(feature = "python", new)]
    pub fn new(
        timestamp: i64,
        open: f64,
        high: f64,
        low: f64,
        close: f64,
        volume: f64,
    ) -> Self {
        Self {
            timestamp,
            open,
            high,
            low,
            close,
            volume,
        }
    }

    /// 转换为 Python 字典
    pub fn to_dict(&self) -> PyResult<HashMap<String, f64>> {
        let mut map = HashMap::new();
        map.insert("timestamp".to_string(), self.timestamp as f64);
        map.insert("open".to_string(), self.open);
        map.insert("high".to_string(), self.high);
        map.insert("low".to_string(), self.low);
        map.insert("close".to_string(), self.close);
        map.insert("volume".to_string(), self.volume);
        Ok(map)
    }

    /// 获取典型价格 (high + low + close) / 3
#[cfg_attr(feature = "python", getter)]
    pub fn typical_price(&self) -> f64 {
        (self.high + self.low + self.close) / 3.0
    }

    /// 获取中间价 (high + low) / 2
#[cfg_attr(feature = "python", getter)]
    pub fn median_price(&self) -> f64 {
        (self.high + self.low) / 2.0
    }

    /// 获取加权收盘价 (high + low + 2*close) / 4
#[cfg_attr(feature = "python", getter)]
    pub fn weighted_close(&self) -> f64 {
        (self.high + self.low + 2.0 * self.close) / 4.0
    }

    /// 字符串表示
    pub fn __repr__(&self) -> String {
        format!(
            "Candle(O:{:.2}, H:{:.2}, L:{:.2}, C:{:.2}, V:{:.2})",
            self.open, self.high, self.low, self.close, self.volume
        )
    }
}

/// 指标计算结果（单序列）
#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug, Clone)]
pub struct IndicatorResult {
#[cfg_attr(feature = "python", pyo3(get))]
    pub name: String,

#[cfg_attr(feature = "python", pyo3(get))]
    pub values: Vec<f64>,

#[cfg_attr(feature = "python", pyo3(get))]
    pub metadata: HashMap<String, String>,
}

#[cfg_attr(feature = "python", pymethods)]
impl IndicatorResult {
#[cfg_attr(feature = "python", new)]
    pub fn new(name: String, values: Vec<f64>) -> Self {
        Self {
            name,
            values,
            metadata: HashMap::new(),
        }
    }

    /// 添加元数据
    pub fn add_metadata(&mut self, key: String, value: String) {
        self.metadata.insert(key, value);
    }

    /// 获取长度
#[cfg_attr(feature = "python", getter)]
    pub fn len(&self) -> usize {
        self.values.len()
    }
}

/// 多序列指标结果（如 MACD 返回 3 条线）
#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug, Clone)]
pub struct MultiIndicatorResult {
#[cfg_attr(feature = "python", pyo3(get))]
    pub name: String,

#[cfg_attr(feature = "python", pyo3(get))]
    pub series: HashMap<String, Vec<f64>>,

#[cfg_attr(feature = "python", pyo3(get))]
    pub metadata: HashMap<String, String>,
}

#[cfg_attr(feature = "python", pymethods)]
impl MultiIndicatorResult {
#[cfg_attr(feature = "python", new)]
    pub fn new(name: String) -> Self {
        Self {
            name,
            series: HashMap::new(),
            metadata: HashMap::new(),
        }
    }

    /// 添加序列
    pub fn add_series(&mut self, key: String, values: Vec<f64>) {
        self.series.insert(key, values);
    }

    /// 添加元数据
    pub fn add_metadata(&mut self, key: String, value: String) {
        self.metadata.insert(key, value);
    }
}

// ==================== 辅助函数 ====================

/// 将 Vec<Candle> 转换为分离的 OHLCV 向量
pub fn candles_to_vectors(candles: &[Candle]) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let open: Vec<f64> = candles.iter().map(|c| c.open).collect();
    let high: Vec<f64> = candles.iter().map(|c| c.high).collect();
    let low: Vec<f64> = candles.iter().map(|c| c.low).collect();
    let close: Vec<f64> = candles.iter().map(|c| c.close).collect();
    let volume: Vec<f64> = candles.iter().map(|c| c.volume).collect();
    (open, high, low, close, volume)
}

/// 验证 OHLC 逻辑（high >= max(O,C), low <= min(O,C)）
pub fn validate_ohlc(candles: &[Candle]) -> Result<(), String> {
    for (i, candle) in candles.iter().enumerate() {
        let max_oc = candle.open.max(candle.close);
        let min_oc = candle.open.min(candle.close);

        if candle.high < max_oc {
            return Err(format!("Candle {} 违反 OHLC 逻辑: high < max(open, close)", i));
        }

        if candle.low > min_oc {
            return Err(format!("Candle {} 违反 OHLC 逻辑: low > min(open, close)", i));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_candle_creation() {
        let candle = Candle::new(1704067200000, 100.0, 102.0, 99.0, 101.0, 1000.0);
        assert_eq!(candle.open, 100.0);
        assert_eq!(candle.high, 102.0);
        assert_eq!(candle.typical_price(), 100.66666666666667);
        assert_eq!(candle.median_price(), 100.5);
    }

    #[test]
    fn test_ohlc_validation() {
        let valid_candles = vec![
            Candle::new(0, 100.0, 102.0, 99.0, 101.0, 1000.0),
            Candle::new(1, 101.0, 103.0, 100.0, 102.0, 1100.0),
        ];
        assert!(validate_ohlc(&valid_candles).is_ok());

        let invalid_candles = vec![
            Candle::new(0, 100.0, 99.0, 98.0, 101.0, 1000.0),  // high < close
        ];
        assert!(validate_ohlc(&invalid_candles).is_err());
    }
}
