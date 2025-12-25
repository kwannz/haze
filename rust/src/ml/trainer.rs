// ml/trainer.rs - 模型训练逻辑
#![allow(dead_code)]
//
// 提供统一的训练接口,支持滚动窗口训练和在线学习
// 遵循 KISS 原则: 简单直接的训练流程

use crate::ml::features::{
    prepare_atr2_features, prepare_momentum_features, prepare_supertrend_features,
    polynomial_features,
};
use crate::ml::models::{ModelType, SFGModel, SFGModelConfig};
use ndarray::Array1;

/// 训练配置
#[derive(Debug, Clone)]
pub struct TrainConfig {
    /// 训练窗口大小
    pub train_window: usize,
    /// 特征滞后周期
    pub lookback: usize,
    /// 是否使用滚动窗口
    pub rolling: bool,
    /// 模型类型
    pub model_type: ModelType,
    /// Ridge alpha
    pub ridge_alpha: f64,
    /// 是否使用多项式特征
    pub use_polynomial: bool,
}

impl Default for TrainConfig {
    fn default() -> Self {
        Self {
            train_window: 200,
            lookback: 10,
            rolling: true,
            model_type: ModelType::LinearRegression,
            ridge_alpha: 1.0,
            use_polynomial: false,
        }
    }
}

/// 训练结果
#[derive(Debug)]
pub struct TrainResult {
    pub model: SFGModel,
    pub training_samples: usize,
    pub features_dim: usize,
}

// ============================================================
// SuperTrend 训练器
// ============================================================

/// 训练 AI SuperTrend 模型
///
/// # 参数
/// - `close`: 收盘价序列
/// - `atr`: ATR 序列
/// - `config`: 训练配置
///
/// # 返回
/// - 训练好的模型
pub fn train_supertrend_model(
    close: &[f64],
    atr: &[f64],
    config: &TrainConfig,
) -> Result<TrainResult, String> {
    // 准备特征
    let (features, targets) = prepare_supertrend_features(close, atr, config.lookback);

    if features.dim().0 == 0 {
        return Err("Insufficient data for training".to_string());
    }

    // 应用多项式特征(可选)
    let features = if config.use_polynomial {
        polynomial_features(&features)
    } else {
        features
    };

    // 选择训练窗口
    let n = features.dim().0;
    let train_size = config.train_window.min(n);
    let start = if config.rolling { n - train_size } else { 0 };

    let train_features = features.slice(ndarray::s![start.., ..]).to_owned();
    let train_targets = targets.slice(ndarray::s![start..]).to_owned();

    // 创建并训练模型
    let model_config = SFGModelConfig {
        model_type: config.model_type,
        ridge_alpha: config.ridge_alpha,
        use_polynomial: config.use_polynomial,
        polynomial_degree: 2,
    };

    let mut model = SFGModel::from_config(&model_config);
    model.train(&train_features, &train_targets)?;

    Ok(TrainResult {
        model,
        training_samples: train_features.dim().0,
        features_dim: train_features.dim().1,
    })
}

// ============================================================
// ATR2 训练器
// ============================================================

/// 训练 ATR2 模型
///
/// # 参数
/// - `close`: 收盘价序列
/// - `atr`: ATR 序列
/// - `volume`: 成交量序列
/// - `config`: 训练配置
pub fn train_atr2_model(
    close: &[f64],
    atr: &[f64],
    volume: &[f64],
    config: &TrainConfig,
) -> Result<TrainResult, String> {
    // 准备特征
    let (features, targets) = prepare_atr2_features(close, atr, volume, config.lookback);

    if features.dim().0 == 0 {
        return Err("Insufficient data for training".to_string());
    }

    // 选择训练窗口
    let n = features.dim().0;
    let train_size = config.train_window.min(n);
    let start = if config.rolling { n - train_size } else { 0 };

    let train_features = features.slice(ndarray::s![start.., ..]).to_owned();
    let train_targets = targets.slice(ndarray::s![start..]).to_owned();

    // ATR2 默认使用 Ridge
    let model_config = SFGModelConfig {
        model_type: ModelType::Ridge,
        ridge_alpha: config.ridge_alpha,
        use_polynomial: false,
        polynomial_degree: 2,
    };

    let mut model = SFGModel::from_config(&model_config);
    model.train(&train_features, &train_targets)?;

    Ok(TrainResult {
        model,
        training_samples: train_features.dim().0,
        features_dim: train_features.dim().1,
    })
}

// ============================================================
// Momentum 训练器
// ============================================================

/// 训练 Momentum 模型
///
/// # 参数
/// - `rsi`: RSI 序列
/// - `config`: 训练配置
pub fn train_momentum_model(rsi: &[f64], config: &TrainConfig) -> Result<TrainResult, String> {
    // 准备特征
    let (features, targets) = prepare_momentum_features(rsi, config.lookback);

    if features.dim().0 == 0 {
        return Err("Insufficient data for training".to_string());
    }

    // 应用多项式特征(可选)
    let features = if config.use_polynomial {
        polynomial_features(&features)
    } else {
        features
    };

    // 选择训练窗口
    let n = features.dim().0;
    let train_size = config.train_window.min(n);
    let start = if config.rolling { n - train_size } else { 0 };

    let train_features = features.slice(ndarray::s![start.., ..]).to_owned();
    let train_targets = targets.slice(ndarray::s![start..]).to_owned();

    // Momentum 使用 LinReg
    let model_config = SFGModelConfig {
        model_type: ModelType::LinearRegression,
        ridge_alpha: config.ridge_alpha,
        use_polynomial: config.use_polynomial,
        polynomial_degree: 2,
    };

    let mut model = SFGModel::from_config(&model_config);
    model.train(&train_features, &train_targets)?;

    Ok(TrainResult {
        model,
        training_samples: train_features.dim().0,
        features_dim: train_features.dim().1,
    })
}

// ============================================================
// 在线预测 (无需预训练)
// ============================================================

/// 在线训练并预测 SuperTrend
///
/// 适用于实时场景: 每个点使用历史数据训练后预测
pub fn online_predict_supertrend(
    close: &[f64],
    atr: &[f64],
    config: &TrainConfig,
) -> Vec<f64> {
    let len = close.len();
    let mut predictions = vec![0.0; len];

    let min_data = config.train_window + config.lookback;
    if len < min_data {
        return predictions;
    }

    // 准备所有特征
    let (all_features, _) = prepare_supertrend_features(close, atr, config.lookback);
    let all_features = if config.use_polynomial {
        polynomial_features(&all_features)
    } else {
        all_features
    };

    if all_features.dim().0 == 0 {
        return predictions;
    }

    // 一次性训练 (使用最近 train_window 数据)
    let n = all_features.dim().0;
    let train_size = config.train_window.min(n);

    let train_features = all_features.slice(ndarray::s![..train_size, ..]).to_owned();

    // 构造目标 (价格变化率)
    let mut train_targets = Array1::zeros(train_size);
    for i in 0..train_size {
        let idx = i + config.lookback;
        if idx > 0 && close[idx - 1] != 0.0 {
            train_targets[i] = (close[idx] - close[idx - 1]) / close[idx - 1];
        }
    }

    // 训练模型
    let model_config = SFGModelConfig {
        model_type: config.model_type,
        ridge_alpha: config.ridge_alpha,
        use_polynomial: config.use_polynomial,
        polynomial_degree: 2,
    };

    let mut model = SFGModel::from_config(&model_config);
    if model.train(&train_features, &train_targets).is_err() {
        return predictions;
    }

    // 预测
    let all_predictions = model.predict(&all_features);

    // 填充结果
    for i in 0..all_predictions.len() {
        let idx = i + config.lookback;
        if idx < len {
            predictions[idx] = all_predictions[i];
        }
    }

    predictions
}

/// 在线训练并预测 ATR2 阈值调整
pub fn online_predict_atr2(
    close: &[f64],
    atr: &[f64],
    volume: &[f64],
    config: &TrainConfig,
) -> Vec<f64> {
    let len = close.len();
    let mut predictions = vec![0.0; len];

    let min_data = config.train_window + config.lookback;
    if len < min_data {
        return predictions;
    }

    // 准备所有特征
    let (all_features, all_targets) = prepare_atr2_features(close, atr, volume, config.lookback);

    if all_features.dim().0 == 0 {
        return predictions;
    }

    // 一次性训练
    let n = all_features.dim().0;
    let train_size = config.train_window.min(n);

    let train_features = all_features.slice(ndarray::s![..train_size, ..]).to_owned();
    let train_targets = all_targets.slice(ndarray::s![..train_size]).to_owned();

    // 训练模型
    let model_config = SFGModelConfig {
        model_type: ModelType::Ridge,
        ridge_alpha: config.ridge_alpha,
        use_polynomial: false,
        polynomial_degree: 2,
    };

    let mut model = SFGModel::from_config(&model_config);
    if model.train(&train_features, &train_targets).is_err() {
        return predictions;
    }

    // 预测
    let all_predictions = model.predict(&all_features);

    // 填充结果
    for i in 0..all_predictions.len() {
        let idx = i + config.lookback;
        if idx < len {
            predictions[idx] = all_predictions[i];
        }
    }

    predictions
}

/// 在线训练并预测 Momentum
pub fn online_predict_momentum(rsi: &[f64], config: &TrainConfig) -> Vec<f64> {
    let len = rsi.len();
    let mut predictions = vec![0.0; len];

    let min_data = config.train_window + config.lookback;
    if len < min_data {
        return predictions;
    }

    // 准备所有特征
    let (all_features, all_targets) = prepare_momentum_features(rsi, config.lookback);

    let all_features = if config.use_polynomial {
        polynomial_features(&all_features)
    } else {
        all_features
    };

    if all_features.dim().0 == 0 {
        return predictions;
    }

    // 一次性训练
    let n = all_features.dim().0;
    let train_size = config.train_window.min(n);

    let train_features = all_features.slice(ndarray::s![..train_size, ..]).to_owned();
    let train_targets = all_targets.slice(ndarray::s![..train_size]).to_owned();

    // 训练模型
    let model_config = SFGModelConfig {
        model_type: ModelType::LinearRegression,
        ridge_alpha: config.ridge_alpha,
        use_polynomial: config.use_polynomial,
        polynomial_degree: 2,
    };

    let mut model = SFGModel::from_config(&model_config);
    if model.train(&train_features, &train_targets).is_err() {
        return predictions;
    }

    // 预测
    let all_predictions = model.predict(&all_features);

    // 填充结果
    for i in 0..all_predictions.len() {
        let idx = i + config.lookback;
        if idx < len {
            predictions[idx] = all_predictions[i];
        }
    }

    predictions
}

#[cfg(test)]
mod tests {
    use super::*;

    fn generate_test_data(len: usize) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
        let mut close = Vec::with_capacity(len);
        let mut atr = Vec::with_capacity(len);
        let mut volume = Vec::with_capacity(len);
        let mut rsi = Vec::with_capacity(len);

        let mut price = 100.0;
        for i in 0..len {
            // 模拟价格走势
            let trend = (i as f64 * 0.01).sin() * 5.0;
            price = price + trend + (i as f64 * 0.1).cos();
            close.push(price);

            atr.push(2.0 + (i as f64 * 0.05).sin());
            volume.push(1000.0 + (i as f64 * 0.1).cos() * 100.0);
            rsi.push(50.0 + (i as f64 * 0.1).sin() * 20.0);
        }

        (close, atr, volume, rsi)
    }

    #[test]
    fn test_train_supertrend_model() {
        let (close, atr, _, _) = generate_test_data(300);

        let config = TrainConfig {
            train_window: 100,
            lookback: 5,
            rolling: true,
            model_type: ModelType::LinearRegression,
            ..Default::default()
        };

        let result = train_supertrend_model(&close, &atr, &config);
        assert!(result.is_ok());

        let result = result.unwrap();
        assert!(result.model.is_trained());
        assert!(result.training_samples > 0);
    }

    #[test]
    fn test_train_atr2_model() {
        let (close, atr, volume, _) = generate_test_data(300);

        let config = TrainConfig {
            train_window: 100,
            lookback: 5,
            rolling: true,
            model_type: ModelType::Ridge,
            ridge_alpha: 1.0,
            ..Default::default()
        };

        let result = train_atr2_model(&close, &atr, &volume, &config);
        assert!(result.is_ok());
    }

    #[test]
    fn test_train_momentum_model() {
        let (_, _, _, rsi) = generate_test_data(300);

        let config = TrainConfig {
            train_window: 100,
            lookback: 5,
            rolling: true,
            model_type: ModelType::LinearRegression,
            ..Default::default()
        };

        let result = train_momentum_model(&rsi, &config);
        assert!(result.is_ok());
    }

    #[test]
    fn test_online_predict_supertrend() {
        let (close, atr, _, _) = generate_test_data(300);

        let config = TrainConfig {
            train_window: 100,
            lookback: 5,
            ..Default::default()
        };

        let predictions = online_predict_supertrend(&close, &atr, &config);

        assert_eq!(predictions.len(), close.len());
        // 检查后半部分有非零预测
        let non_zero_count = predictions.iter().filter(|x| **x != 0.0).count();
        assert!(non_zero_count > 0);
    }

    #[test]
    fn test_insufficient_data() {
        let close = vec![100.0, 101.0, 102.0];
        let atr = vec![2.0, 2.1, 2.2];

        let config = TrainConfig {
            train_window: 100,
            lookback: 5,
            ..Default::default()
        };

        let result = train_supertrend_model(&close, &atr, &config);
        assert!(result.is_err());
    }
}
