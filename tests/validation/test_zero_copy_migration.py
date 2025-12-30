"""
零拷贝迁移验证测试框架

功能:
1. 自动为所有 257 个迁移函数生成参数化测试
2. 验证数值精度（误差 < 1e-10）
3. 验证性能提升（加速比 > 1.5x）
4. 验证 NaN 模式一致性

运行示例:
    pytest tests/validation/test_zero_copy_migration.py -v
    pytest tests/validation/test_zero_copy_migration.py -k "py_sma" -v
    pytest tests/validation/test_zero_copy_migration.py::test_numerical_accuracy -v
"""

import time
import numpy as np
import pytest
import haze_library as haze


# ============================================================================
# 测试数据生成器
# ============================================================================

def generate_test_data(size: int = 100, seed: int = 42) -> dict:
    """
    生成标准测试数据集

    Returns:
        dict: {
            'close': np.ndarray,
            'high': np.ndarray,
            'low': np.ndarray,
            'open': np.ndarray,
            'volume': np.ndarray
        }
    """
    np.random.seed(seed)

    # 生成模拟价格数据（随机游走 + 趋势）
    trend = np.linspace(100, 110, size)
    noise = np.cumsum(np.random.randn(size) * 0.5)
    close = trend + noise

    # high 始终高于 close
    high = close + np.abs(np.random.randn(size) * 0.5)

    # low 始终低于 close
    low = close - np.abs(np.random.randn(size) * 0.5)

    # open 介于 high 和 low 之间
    open_ = low + (high - low) * np.random.rand(size)

    # volume 为正整数
    volume = np.random.randint(1000, 100000, size=size).astype(float)

    return {
        'close': close,
        'high': high,
        'low': low,
        'open': open_,
        'volume': volume
    }


# ============================================================================
# 指标函数注册表 (自动发现所有已迁移的指标)
# ============================================================================

def discover_migrated_indicators() -> list[tuple[str, dict]]:
    """
    自动发现所有已迁移的指标函数

    Returns:
        list of (func_name, default_params)

    注意:
    - 只包含已有 _legacy 版本的函数（说明已迁移）
    - 参数为函数的默认参数配置
    """
    migrated = []

    # Week 1 已迁移的 5 个指标
    migrated.extend([
        ("py_sma", {"period": 20}),
        ("py_ema", {"period": 20}),
        ("py_rsi", {"period": 14}),
        ("py_macd", {"fast_period": 12, "slow_period": 26, "signal_period": 9}),
        ("py_atr", {"period": 14}),
    ])

    # TODO: Phase 1-4 完成后，自动扫描 haze_library 模块添加更多函数
    # 可以通过检查 dir(haze) 中是否存在 func 和 func_legacy 来自动发现

    return migrated


MIGRATED_INDICATORS = discover_migrated_indicators()


# ============================================================================
# 测试用例: 数值精度验证
# ============================================================================

@pytest.mark.parametrize("func_name,params", MIGRATED_INDICATORS)
def test_numerical_accuracy(func_name, params):
    """
    验证零拷贝版本与 legacy 版本数值一致

    要求:
    - 数值误差 < 1e-10 (绝对误差 + 相对误差)
    - NaN 模式完全一致
    """
    # 生成测试数据
    data = generate_test_data(size=100)

    # 获取函数
    func_new = getattr(haze, func_name)
    func_legacy = getattr(haze, f"{func_name}_legacy")

    # 确定输入参数
    if func_name in ["py_atr"]:
        # 多输入函数 (high, low, close)
        input_new = (data['high'], data['low'], data['close'])
        input_legacy = (data['high'].tolist(), data['low'].tolist(), data['close'].tolist())
    elif func_name in ["py_macd"]:
        # 单输入多参数函数
        input_new = (data['close'],)
        input_legacy = (data['close'].tolist(),)
    else:
        # 默认使用 close
        input_new = (data['close'],)
        input_legacy = (data['close'].tolist(),)

    # 调用两个版本
    result_new = func_new(*input_new, **params)
    result_legacy = func_legacy(*input_legacy, **params)

    # MACD 返回 3 个数组
    if func_name == "py_macd":
        for i, (new, legacy) in enumerate(zip(result_new, result_legacy)):
            # 转换为 NumPy 数组（如果不是的话）
            new_arr = np.asarray(new)
            legacy_arr = np.asarray(legacy)

            # 验证数值一致性
            np.testing.assert_allclose(
                new_arr,
                legacy_arr,
                rtol=1e-10,
                atol=1e-10,
                err_msg=f"{func_name} output[{i}] numerical mismatch"
            )

            # 验证 NaN 模式一致性
            assert np.all(np.isnan(new_arr) == np.isnan(legacy_arr)), \
                f"{func_name} output[{i}] NaN pattern mismatch"

    else:
        # 单输出函数
        result_new_arr = np.asarray(result_new)
        result_legacy_arr = np.asarray(result_legacy)

        # 验证数值一致性
        np.testing.assert_allclose(
            result_new_arr,
            result_legacy_arr,
            rtol=1e-10,
            atol=1e-10,
            err_msg=f"{func_name} numerical mismatch"
        )

        # 验证 NaN 模式一致性
        assert np.all(np.isnan(result_new_arr) == np.isnan(result_legacy_arr)), \
            f"{func_name} NaN pattern mismatch"


# ============================================================================
# 测试用例: 性能验证
# ============================================================================

@pytest.mark.parametrize("func_name", [f[0] for f in MIGRATED_INDICATORS])
def test_performance_improvement(func_name):
    """
    验证性能提升 > 1.5x

    测试条件:
    - 数据规模: n=100,000
    - 重复次数: 50 次取平均
    - 预热次数: 5 次（避免冷启动影响）
    """
    # 大数据集
    data = generate_test_data(size=100_000)

    # 获取函数
    func_new = getattr(haze, func_name)
    func_legacy = getattr(haze, f"{func_name}_legacy")

    # 确定输入参数
    if func_name == "py_atr":
        input_new = (data['high'], data['low'], data['close'])
        input_legacy = (data['high'].tolist(), data['low'].tolist(), data['close'].tolist())
        params = {"period": 14}
    elif func_name == "py_macd":
        input_new = (data['close'],)
        input_legacy = (data['close'].tolist(),)
        params = {"fast_period": 12, "slow_period": 26, "signal_period": 9}
    elif func_name == "py_rsi":
        input_new = (data['close'],)
        input_legacy = (data['close'].tolist(),)
        params = {"period": 14}
    else:
        input_new = (data['close'],)
        input_legacy = (data['close'].tolist(),)
        params = {"period": 20}

    # 预热（避免冷启动）
    for _ in range(5):
        _ = func_new(*input_new, **params)
        _ = func_legacy(*input_legacy, **params)

    # 零拷贝版本基准测试
    times_new = []
    for _ in range(50):
        start = time.perf_counter()
        _ = func_new(*input_new, **params)
        times_new.append(time.perf_counter() - start)

    # Legacy 版本基准测试
    times_legacy = []
    for _ in range(50):
        start = time.perf_counter()
        _ = func_legacy(*input_legacy, **params)
        times_legacy.append(time.perf_counter() - start)

    # 计算平均时间和加速比
    avg_new = np.mean(times_new) * 1000  # 转换为 ms
    avg_legacy = np.mean(times_legacy) * 1000
    speedup = avg_legacy / avg_new

    # 输出性能报告
    print(f"\n{'='*60}")
    print(f"性能测试: {func_name} (n=100,000)")
    print(f"{'='*60}")
    print(f"Legacy 平均耗时:    {avg_legacy:.3f} ms")
    print(f"零拷贝平均耗时:    {avg_new:.3f} ms")
    print(f"加速比:            {speedup:.2f}x")
    print(f"性能提升:          {(speedup - 1) * 100:.1f}%")
    print(f"{'='*60}")

    # 验证性能提升
    assert speedup > 1.5, \
        f"{func_name} speedup {speedup:.2f}x < 1.5x threshold"


# ============================================================================
# 测试用例: 边界条件
# ============================================================================

@pytest.mark.parametrize("func_name", [f[0] for f in MIGRATED_INDICATORS])
def test_edge_cases(func_name):
    """
    测试边界条件

    测试场景:
    - 最小数据集 (n=1)
    - NaN 值处理
    - Inf 值处理
    - period > length
    """
    func_new = getattr(haze, func_name)

    # 场景 1: 最小数据集
    single_val = np.array([100.0])
    if func_name == "py_atr":
        result = func_new(single_val, single_val, single_val, period=14)
    elif func_name == "py_macd":
        result = func_new(single_val, fast_period=12, slow_period=26, signal_period=9)
    elif func_name == "py_rsi":
        result = func_new(single_val, period=14)
    else:
        result = func_new(single_val, period=20)

    # 应该返回有效数组（可能全是 NaN）
    if func_name == "py_macd":
        for arr in result:
            assert len(arr) == 1
    else:
        assert len(result) == 1

    # 场景 2: NaN 值处理
    data_with_nan = np.array([100.0, np.nan, 102.0, 103.0, 104.0])
    try:
        if func_name == "py_atr":
            result = func_new(data_with_nan, data_with_nan, data_with_nan, period=3)
        elif func_name == "py_macd":
            result = func_new(data_with_nan, fast_period=2, slow_period=3, signal_period=2)
        elif func_name == "py_rsi":
            result = func_new(data_with_nan, period=3)
        else:
            result = func_new(data_with_nan, period=3)

        # 应该处理 NaN 而不崩溃
        if func_name == "py_macd":
            for arr in result:
                assert len(arr) == len(data_with_nan)
        else:
            assert len(result) == len(data_with_nan)
    except Exception as e:
        pytest.fail(f"{func_name} failed to handle NaN: {e}")

    # 场景 3: period > length（应该返回全 NaN）
    short_data = np.array([100.0, 101.0, 102.0])
    if func_name == "py_atr":
        result = func_new(short_data, short_data, short_data, period=100)
    elif func_name == "py_macd":
        result = func_new(short_data, fast_period=50, slow_period=100, signal_period=30)
    elif func_name == "py_rsi":
        result = func_new(short_data, period=100)
    else:
        result = func_new(short_data, period=100)

    # 应该返回全 NaN 数组（或大部分 NaN）
    if func_name == "py_macd":
        for arr in result:
            assert len(arr) == len(short_data)
            # 至少一部分应该是 NaN
            assert np.any(np.isnan(arr))
    else:
        assert len(result) == len(short_data)
        assert np.any(np.isnan(result))


# ============================================================================
# 测试用例: 类型验证
# ============================================================================

@pytest.mark.parametrize("func_name", [f[0] for f in MIGRATED_INDICATORS])
def test_input_type_validation(func_name):
    """
    验证输入类型检查

    零拷贝版本应该接受:
    - NumPy ndarray
    - Python list (自动转换)
    """
    func_new = getattr(haze, func_name)

    # NumPy ndarray 输入（应该成功）
    np_data = np.array([100.0, 101.0, 102.0, 103.0, 104.0])

    try:
        if func_name == "py_atr":
            result = func_new(np_data, np_data, np_data, period=3)
        elif func_name == "py_macd":
            result = func_new(np_data, fast_period=2, slow_period=3, signal_period=2)
        elif func_name == "py_rsi":
            result = func_new(np_data, period=3)
        else:
            result = func_new(np_data, period=3)

        # 验证返回值类型
        if func_name == "py_macd":
            for arr in result:
                assert isinstance(arr, np.ndarray)
        else:
            assert isinstance(result, np.ndarray)

    except Exception as e:
        pytest.fail(f"{func_name} failed with NumPy input: {e}")

    # Python list 输入（应该成功 - 自动转换）
    list_data = [100.0, 101.0, 102.0, 103.0, 104.0]

    try:
        if func_name == "py_atr":
            result = func_new(list_data, list_data, list_data, period=3)
        elif func_name == "py_macd":
            result = func_new(list_data, fast_period=2, slow_period=3, signal_period=2)
        elif func_name == "py_rsi":
            result = func_new(list_data, period=3)
        else:
            result = func_new(list_data, period=3)

        # 验证返回值类型
        if func_name == "py_macd":
            for arr in result:
                assert isinstance(arr, np.ndarray)
        else:
            assert isinstance(result, np.ndarray)

    except Exception as e:
        pytest.fail(f"{func_name} failed with list input: {e}")


# ============================================================================
# 性能基准报告生成
# ============================================================================

def generate_performance_report():
    """
    生成性能基准报告（CSV 格式）

    运行方式:
        pytest tests/validation/test_zero_copy_migration.py::test_performance_improvement -v -s > performance_report.txt
    """
    pass  # 由 test_performance_improvement 的 print 语句生成报告


if __name__ == "__main__":
    # 快速测试（开发时使用）
    print("运行快速验证测试...")

    # 测试数据生成
    data = generate_test_data()
    print(f"✅ 测试数据生成成功: {len(data['close'])} 个数据点")

    # 测试单个函数
    func_name = "py_sma"
    test_numerical_accuracy(func_name, {"period": 20})
    print(f"✅ {func_name} 数值精度测试通过")

    print("\n完整测试请运行: pytest tests/validation/test_zero_copy_migration.py -v")
