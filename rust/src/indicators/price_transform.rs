/// Price Transform Indicators Module
///
/// 价格变换指标，用于从 OHLC 数据计算各种典型价格
/// 这些是 TA-Lib 中最基础的价格计算函数

/// AVGPRICE - Average Price
///
/// 平均价格 = (Open + High + Low + Close) / 4
///
/// # 参数
/// - `open`: 开盘价序列
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
///
/// # 返回
/// - 平均价格序列
pub fn avgprice(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    let n = open.len().min(high.len()).min(low.len()).min(close.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        let avg = (open[i] + high[i] + low[i] + close[i]) / 4.0;
        result.push(avg);
    }

    result
}

/// MEDPRICE - Median Price
///
/// 中间价 = (High + Low) / 2
///
/// 用途：代表当日价格的中点，常用于计算其他指标
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
///
/// # 返回
/// - 中间价序列
pub fn medprice(high: &[f64], low: &[f64]) -> Vec<f64> {
    let n = high.len().min(low.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        let med = (high[i] + low[i]) / 2.0;
        result.push(med);
    }

    result
}

/// TYPPRICE - Typical Price
///
/// 典型价格 = (High + Low + Close) / 3
///
/// 用途：最常用的价格代表，用于 VWAP、CCI 等指标计算
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
///
/// # 返回
/// - 典型价格序列
pub fn typprice(high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    let n = high.len().min(low.len()).min(close.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        let typ = (high[i] + low[i] + close[i]) / 3.0;
        result.push(typ);
    }

    result
}

/// WCLPRICE - Weighted Close Price
///
/// 加权收盘价 = (High + Low + 2 * Close) / 4
///
/// 用途：给收盘价更高权重的价格代表
///
/// # 参数
/// - `high`: 最高价序列
/// - `low`: 最低价序列
/// - `close`: 收盘价序列
///
/// # 返回
/// - 加权收盘价序列
pub fn wclprice(high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    let n = high.len().min(low.len()).min(close.len());
    let mut result = Vec::with_capacity(n);

    for i in 0..n {
        let wcl = (high[i] + low[i] + 2.0 * close[i]) / 4.0;
        result.push(wcl);
    }

    result
}

/// HL2 - (High + Low) / 2
///
/// 等同于 MEDPRICE，为兼容性保留
pub fn hl2(high: &[f64], low: &[f64]) -> Vec<f64> {
    medprice(high, low)
}

/// HLC3 - (High + Low + Close) / 3
///
/// 等同于 TYPPRICE，为兼容性保留
pub fn hlc3(high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    typprice(high, low, close)
}

/// OHLC4 - (Open + High + Low + Close) / 4
///
/// 等同于 AVGPRICE，为兼容性保留
pub fn ohlc4(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Vec<f64> {
    avgprice(open, high, low, close)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_avgprice() {
        let open = vec![100.0, 102.0];
        let high = vec![105.0, 107.0];
        let low = vec![99.0, 101.0];
        let close = vec![103.0, 105.0];

        let result = avgprice(&open, &high, &low, &close);

        // (100+105+99+103)/4 = 101.75
        assert!((result[0] - 101.75).abs() < 1e-10);
        // (102+107+101+105)/4 = 103.75
        assert!((result[1] - 103.75).abs() < 1e-10);
    }

    #[test]
    fn test_medprice() {
        let high = vec![105.0, 107.0];
        let low = vec![99.0, 101.0];

        let result = medprice(&high, &low);

        // (105+99)/2 = 102.0
        assert_eq!(result[0], 102.0);
        // (107+101)/2 = 104.0
        assert_eq!(result[1], 104.0);
    }

    #[test]
    fn test_typprice() {
        let high = vec![105.0, 107.0];
        let low = vec![99.0, 101.0];
        let close = vec![103.0, 105.0];

        let result = typprice(&high, &low, &close);

        // (105+99+103)/3 = 102.333...
        assert!((result[0] - 102.333333333).abs() < 1e-9);
        // (107+101+105)/3 = 104.333...
        assert!((result[1] - 104.333333333).abs() < 1e-9);
    }

    #[test]
    fn test_wclprice() {
        let high = vec![105.0, 107.0];
        let low = vec![99.0, 101.0];
        let close = vec![103.0, 105.0];

        let result = wclprice(&high, &low, &close);

        // (105+99+2*103)/4 = 102.5
        assert_eq!(result[0], 102.5);
        // (107+101+2*105)/4 = 104.5
        assert_eq!(result[1], 104.5);
    }

    #[test]
    fn test_compatibility_aliases() {
        let high = vec![105.0];
        let low = vec![99.0];
        let close = vec![103.0];
        let open = vec![100.0];

        // HL2 == MEDPRICE
        assert_eq!(hl2(&high, &low), medprice(&high, &low));

        // HLC3 == TYPPRICE
        assert_eq!(hlc3(&high, &low, &close), typprice(&high, &low, &close));

        // OHLC4 == AVGPRICE
        assert_eq!(ohlc4(&open, &high, &low, &close), avgprice(&open, &high, &low, &close));
    }
}
