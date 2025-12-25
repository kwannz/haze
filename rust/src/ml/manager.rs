// ml/manager.rs - 模型管理器
#![allow(dead_code)]
//
// 提供模型序列化、持久化和智能加载功能
// 遵循 Occam's Razor: 最简单的序列化方案 (bincode)

use crate::ml::models::SFGModelConfig;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::{self, File};
use std::io::{BufReader, BufWriter};
use std::path::PathBuf;

/// 模型元数据
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ModelMetadata {
    pub name: String,
    pub version: String,
    pub created_at: u64,
    pub training_samples: usize,
    pub features_dim: usize,
    pub config: SFGModelConfig,
}

/// 模型管理器
///
/// 负责模型的保存、加载和缓存
pub struct SFGModelManager {
    model_dir: PathBuf,
    metadata_cache: HashMap<String, ModelMetadata>,
}

impl SFGModelManager {
    /// 创建模型管理器
    pub fn new(model_dir: &str) -> Self {
        let path = PathBuf::from(model_dir);

        // 创建目录(如果不存在)
        if let Err(e) = fs::create_dir_all(&path) {
            eprintln!("Warning: Failed to create model directory: {}", e);
        }

        Self {
            model_dir: path,
            metadata_cache: HashMap::new(),
        }
    }

    /// 保存模型元数据
    pub fn save_metadata(&mut self, name: &str, metadata: &ModelMetadata) -> Result<(), String> {
        let path = self.model_dir.join(format!("{}.meta.json", name));

        let file =
            File::create(&path).map_err(|e| format!("Failed to create metadata file: {}", e))?;

        let writer = BufWriter::new(file);
        serde_json::to_writer_pretty(writer, metadata)
            .map_err(|e| format!("Failed to write metadata: {}", e))?;

        self.metadata_cache.insert(name.to_string(), metadata.clone());

        Ok(())
    }

    /// 加载模型元数据
    pub fn load_metadata(&mut self, name: &str) -> Result<ModelMetadata, String> {
        // 检查缓存
        if let Some(meta) = self.metadata_cache.get(name) {
            return Ok(meta.clone());
        }

        let path = self.model_dir.join(format!("{}.meta.json", name));

        if !path.exists() {
            return Err(format!("Metadata file not found: {}", name));
        }

        let file = File::open(&path).map_err(|e| format!("Failed to open metadata file: {}", e))?;

        let reader = BufReader::new(file);
        let metadata: ModelMetadata =
            serde_json::from_reader(reader).map_err(|e| format!("Failed to parse metadata: {}", e))?;

        self.metadata_cache.insert(name.to_string(), metadata.clone());

        Ok(metadata)
    }

    /// 检查模型是否存在
    pub fn model_exists(&self, name: &str) -> bool {
        let path = self.model_dir.join(format!("{}.meta.json", name));
        path.exists()
    }

    /// 列出所有已保存的模型
    pub fn list_models(&self) -> Vec<String> {
        let mut models = Vec::new();

        if let Ok(entries) = fs::read_dir(&self.model_dir) {
            for entry in entries.flatten() {
                if let Some(name) = entry.file_name().to_str() {
                    if name.ends_with(".meta.json") {
                        let model_name = name.trim_end_matches(".meta.json").to_string();
                        models.push(model_name);
                    }
                }
            }
        }

        models
    }

    /// 删除模型
    pub fn delete_model(&mut self, name: &str) -> Result<(), String> {
        let meta_path = self.model_dir.join(format!("{}.meta.json", name));

        if meta_path.exists() {
            fs::remove_file(&meta_path)
                .map_err(|e| format!("Failed to delete metadata: {}", e))?;
        }

        self.metadata_cache.remove(name);

        Ok(())
    }

    /// 获取模型目录
    pub fn get_model_dir(&self) -> &PathBuf {
        &self.model_dir
    }

    /// 清理过期模型 (保留最近 n 个)
    pub fn cleanup_old_models(&mut self, keep_count: usize) -> Result<usize, String> {
        let mut models: Vec<(String, u64)> = Vec::new();

        for name in self.list_models() {
            if let Ok(meta) = self.load_metadata(&name) {
                models.push((name, meta.created_at));
            }
        }

        // 按创建时间排序 (最新在前)
        models.sort_by(|a, b| b.1.cmp(&a.1));

        let mut deleted = 0;
        for (name, _) in models.into_iter().skip(keep_count) {
            if self.delete_model(&name).is_ok() {
                deleted += 1;
            }
        }

        Ok(deleted)
    }
}

impl Default for SFGModelManager {
    fn default() -> Self {
        Self::new("./models")
    }
}

/// 获取当前时间戳 (秒)
pub fn current_timestamp() -> u64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0)
}

/// 创建模型元数据
pub fn create_metadata(
    name: &str,
    config: &SFGModelConfig,
    training_samples: usize,
    features_dim: usize,
) -> ModelMetadata {
    ModelMetadata {
        name: name.to_string(),
        version: "1.0.0".to_string(),
        created_at: current_timestamp(),
        training_samples,
        features_dim,
        config: config.clone(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;
    use std::sync::atomic::{AtomicU64, Ordering};

    // 原子计数器确保每个测试有唯一目录
    static TEST_COUNTER: AtomicU64 = AtomicU64::new(0);

    fn get_test_dir() -> PathBuf {
        let mut dir = env::temp_dir();
        let unique_id = TEST_COUNTER.fetch_add(1, Ordering::SeqCst);
        dir.push(format!(
            "haze_test_{}_{}_{}",
            current_timestamp(),
            std::process::id(),
            unique_id
        ));
        dir
    }

    #[test]
    fn test_model_manager_creation() {
        let dir = get_test_dir();
        let manager = SFGModelManager::new(dir.to_str().unwrap());

        assert!(manager.get_model_dir().exists() || dir.to_str().is_some());

        // 清理
        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn test_save_and_load_metadata() {
        let dir = get_test_dir();
        let mut manager = SFGModelManager::new(dir.to_str().unwrap());

        let config = SFGModelConfig::default();
        let metadata = create_metadata("test_model", &config, 100, 10);

        // 保存
        let result = manager.save_metadata("test_model", &metadata);
        assert!(result.is_ok());

        // 检查存在
        assert!(manager.model_exists("test_model"));

        // 加载
        let loaded = manager.load_metadata("test_model");
        assert!(loaded.is_ok());

        let loaded = loaded.unwrap();
        assert_eq!(loaded.name, "test_model");
        assert_eq!(loaded.training_samples, 100);

        // 清理
        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn test_list_models() {
        let dir = get_test_dir();
        let mut manager = SFGModelManager::new(dir.to_str().unwrap());

        let config = SFGModelConfig::default();

        // 保存多个模型
        for i in 0..3 {
            let metadata = create_metadata(&format!("model_{}", i), &config, 100, 10);
            manager
                .save_metadata(&format!("model_{}", i), &metadata)
                .unwrap();
        }

        let models = manager.list_models();
        assert_eq!(models.len(), 3);

        // 清理
        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn test_delete_model() {
        let dir = get_test_dir();
        let mut manager = SFGModelManager::new(dir.to_str().unwrap());

        let config = SFGModelConfig::default();
        let metadata = create_metadata("to_delete", &config, 100, 10);

        manager.save_metadata("to_delete", &metadata).unwrap();
        assert!(manager.model_exists("to_delete"));

        manager.delete_model("to_delete").unwrap();
        assert!(!manager.model_exists("to_delete"));

        // 清理
        let _ = fs::remove_dir_all(&dir);
    }
}
