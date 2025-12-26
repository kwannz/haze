// ml/mod.rs - 纯 Rust ML 模块
//
// 使用 linfa 库实现 SVR 和 Linear Regression,替代 KNN
// 提供高性能、零 Python 依赖的机器学习能力

pub mod features;
pub mod manager;
pub mod models;
pub mod trainer;

// 内部模块重导出 (供未来扩展使用)
#[allow(unused_imports)]
pub use features::*;
#[allow(unused_imports)]
pub use manager::*;
#[allow(unused_imports)]
pub use models::*;
#[allow(unused_imports)]
pub use trainer::*;
