# Haze-Library 类型存根使用指南

**创建日期**: 2025-12-26
**项目**: Haze-Library v0.1.0

---

## 快速开始

### 验证安装

```bash
# 1. 验证类型存根文件
python3 verify_type_stubs.py

# 2. 运行示例
python3 examples/type_hints_demo.py

# 3. 类型检查 (可选)
pip install mypy
mypy examples/type_hints_demo.py
```

---

## 文件结构

```
/Users/zhaoleon/Desktop/haze/haze/
├── src/haze_library/
│   ├── __init__.pyi           # 主接口类型存根 (1,213 行)
│   ├── haze_library.pyi       # 完整函数签名 (363 行, 222 函数)
│   ├── py.typed               # PEP 561 标记文件
│   └── ...
├── generate_pyi.py            # 自动生成脚本
├── verify_type_stubs.py       # 验证脚本
├── TYPE_STUBS_REPORT.md       # 详细报告
└── TYPE_STUBS_USAGE.md        # 本文件
```

---

## IDE 配置

### VS Code

1. **安装 Python 扩展**
   - 扩展 ID: `ms-python.python`
   - 包含 Pylance 类型检查器

2. **配置 settings.json**
   ```json
   {
     "python.analysis.typeCheckingMode": "basic",
     "python.analysis.autoImportCompletions": true,
     "python.analysis.completeFunctionParens": true
   }
   ```

3. **测试自动补全**
   - 打开任意 Python 文件
   - 输入: `from haze_library import py_`
   - 按 `Ctrl+Space` 查看所有函数

4. **查看函数签名**
   - 输入: `py_sma(`
   - 自动显示参数提示
   - 悬停鼠标查看文档

### PyCharm

1. **确保 Type Checking 开启**
   - Settings → Editor → Inspections
   - 勾选 "Type checker"

2. **导入模块**
   ```python
   from haze_library import py_sma, py_rsi
   ```

3. **自动补全**
   - 输入函数名
   - `Ctrl+Space` 触发补全
   - 查看参数提示

---

## 使用示例

### 基础用法

```python
from typing import List, Tuple
from haze_library import py_sma, py_rsi, py_macd

# 准备数据
close_prices: List[float] = [100.0, 101.0, 102.0, 103.0, 104.0]

# 简单移动平均 - IDE 提示: (values: List[float], period: int) -> List[float]
sma_20: List[float] = py_sma(close_prices, 20)

# RSI - IDE 提示: (close: List[float], period: Optional[int] = None) -> List[float]
rsi_14: List[float] = py_rsi(close_prices, 14)
rsi_default: List[float] = py_rsi(close_prices)  # period=14 (默认值)

# MACD - IDE 提示: (...) -> Tuple[List[float], List[float], List[float]]
macd_line, signal_line, histogram = py_macd(
    close_prices,
    fast_period=12,
    slow_period=26,
    signal_period=9
)
```

### 类型检查

```python
from haze_library import py_sma

close_prices = [100.0, 101.0, 102.0]

# ✅ 正确用法
result: List[float] = py_sma(close_prices, 5)

# ❌ 类型错误 - mypy/pylance 会标记
# wrong_type: str = py_sma(close_prices, 5)

# ❌ 参数类型错误
# py_sma(close_prices, "5")  # 期望 int, 得到 str

# ❌ 返回值解包错误
# single_value: float = py_macd(close_prices)  # 期望 float, 得到 Tuple
```

### Pandas 集成

```python
import pandas as pd
import haze_library

# 创建 DataFrame
df = pd.DataFrame({
    'close': [100.0, 101.0, 102.0, 103.0, 104.0]
})

# DataFrame accessor - IDE 自动补全
df['sma_20'] = df.ta.sma(20)      # <- 输入 df.ta. 后自动提示所有方法
df['rsi_14'] = df.ta.rsi(14)
df['ema_10'] = df.ta.ema(10)

# 多输出指标
upper, middle, lower = df.ta.bollinger_bands(20, 2.0)
df['bb_upper'] = upper
df['bb_middle'] = middle
df['bb_lower'] = lower
```

### NumPy 兼容

```python
import numpy as np
from haze_library import np_ta

# NumPy 数组
close = np.array([100.0, 101.0, 102.0, 103.0, 104.0])

# NumPy 接口 - 返回 numpy.ndarray
sma = np_ta.sma(close, 20)  # type: numpy.ndarray
rsi = np_ta.rsi(close, 14)
ema = np_ta.ema(close, 10)
```

---

## 函数分类快速参考

### 波动率指标 (8 个)

```python
from haze_library import (
    py_atr,           # Average True Range
    py_natr,          # Normalized ATR
    py_true_range,    # True Range
    py_bollinger_bands,   # Bollinger Bands
    py_keltner_channel,   # Keltner Channel
    py_donchian_channel,  # Donchian Channel
)

# 示例
atr = py_atr(high, low, close, period=14)
upper, middle, lower = py_bollinger_bands(close, period=20, std_multiplier=2.0)
```

### 动量指标 (22 个)

```python
from haze_library import (
    py_rsi,           # Relative Strength Index
    py_macd,          # MACD
    py_stochastic,    # Stochastic Oscillator
    py_stochrsi,      # Stochastic RSI
    py_cci,           # Commodity Channel Index
    py_williams_r,    # Williams %R
    py_kdj,           # KDJ
    py_tsi,           # True Strength Index
    py_mom,           # Momentum
    py_roc,           # Rate of Change
)

# 示例
rsi = py_rsi(close, 14)
macd, signal, hist = py_macd(close, 12, 26, 9)
k, d = py_stochastic(high, low, close, 14, 3)
```

### 趋势指标 (15 个)

```python
from haze_library import (
    py_supertrend,    # SuperTrend
    py_adx,           # Average Directional Index
    py_aroon,         # Aroon Indicator
    py_psar,          # Parabolic SAR
    py_vortex,        # Vortex Indicator
    py_choppiness,    # Choppiness Index
)

# 示例
st, direction, lb, ub = py_supertrend(high, low, close, 10, 3.0)
adx, plus_di, minus_di = py_adx(high, low, close, 14)
```

### 成交量指标 (14 个)

```python
from haze_library import (
    py_obv,           # On-Balance Volume
    py_vwap,          # VWAP
    py_mfi,           # Money Flow Index
    py_cmf,           # Chaikin Money Flow
    py_ad,            # Accumulation/Distribution
    py_pvt,           # Price Volume Trend
)

# 示例
obv = py_obv(close, volume)
vwap = py_vwap(high, low, close, volume)
mfi = py_mfi(high, low, close, volume, 14)
```

### 移动平均线 (22 个)

```python
from haze_library import (
    py_sma,           # Simple MA
    py_ema,           # Exponential MA
    py_wma,           # Weighted MA
    py_dema,          # Double Exponential MA
    py_tema,          # Triple Exponential MA
    py_hma,           # Hull MA
    py_rma,           # Wilder's MA
    py_zlma,          # Zero Lag MA
    py_t3,            # Tillson T3
    py_kama,          # Kaufman Adaptive MA
    py_frama,         # Fractal Adaptive MA
)

# 示例
sma = py_sma(close, 20)
ema = py_ema(close, 20)
kama = py_kama(close, 10, 2, 30)
```

### 蜡烛图形态 (54 个)

```python
from haze_library import (
    py_doji,                    # Doji
    py_hammer,                  # Hammer
    py_bullish_engulfing,       # Bullish Engulfing
    py_bearish_engulfing,       # Bearish Engulfing
    py_morning_star,            # Morning Star
    py_evening_star,            # Evening Star
    py_three_white_soldiers,    # Three White Soldiers
    py_three_black_crows,       # Three Black Crows
)

# 示例 - 返回 1.0 (看涨), -1.0 (看跌), 0.0 (无形态)
doji_signals = py_doji(open, high, low, close)
hammer_signals = py_hammer(open, high, low, close)
```

---

## 高级用法

### 批量计算

```python
from haze_library import (
    py_sma, py_ema, py_rsi,
    py_macd, py_bollinger_bands
)

def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """计算多个指标"""
    close = df['close'].tolist()

    # 移动平均线
    df['sma_20'] = py_sma(close, 20)
    df['ema_20'] = py_ema(close, 20)

    # 动量指标
    df['rsi_14'] = py_rsi(close, 14)

    # MACD
    macd, signal, hist = py_macd(close)
    df['macd'] = macd
    df['macd_signal'] = signal
    df['macd_hist'] = hist

    # Bollinger Bands
    upper, middle, lower = py_bollinger_bands(close, 20, 2.0)
    df['bb_upper'] = upper
    df['bb_middle'] = middle
    df['bb_lower'] = lower

    return df
```

### 策略回测

```python
from typing import List
from haze_library import py_rsi, py_macd

def rsi_macd_strategy(
    close: List[float]
) -> List[int]:
    """
    RSI + MACD 组合策略

    Returns:
        信号列表: 1 (买入), -1 (卖出), 0 (持有)
    """
    # 计算指标
    rsi = py_rsi(close, 14)
    macd, signal, _ = py_macd(close, 12, 26, 9)

    # 生成信号
    signals = [0] * len(close)

    for i in range(len(close)):
        # 买入信号: RSI < 30 且 MACD 金叉
        if (rsi[i] < 30 and
            macd[i] > signal[i] and
            i > 0 and macd[i-1] <= signal[i-1]):
            signals[i] = 1

        # 卖出信号: RSI > 70 且 MACD 死叉
        elif (rsi[i] > 70 and
              macd[i] < signal[i] and
              i > 0 and macd[i-1] >= signal[i-1]):
            signals[i] = -1

    return signals
```

---

## 性能优化建议

### 1. 批量计算

```python
# ❌ 低效 - 多次调用
for period in [5, 10, 20, 50]:
    sma = py_sma(close, period)

# ✅ 高效 - 一次准备数据
close_data = df['close'].tolist()
sma_5 = py_sma(close_data, 5)
sma_10 = py_sma(close_data, 10)
sma_20 = py_sma(close_data, 20)
```

### 2. 避免重复转换

```python
# ❌ 低效 - 重复转换
for indicator in indicators:
    result = indicator(df['close'].tolist(), period)

# ✅ 高效 - 转换一次
close_list = df['close'].tolist()
for indicator in indicators:
    result = indicator(close_list, period)
```

### 3. 使用 NumPy 接口

```python
# ✅ NumPy 接口更快 (对于已有 NumPy 数组的情况)
import numpy as np
from haze_library import np_ta

close_array = df['close'].values  # 已经是 numpy.ndarray
sma = np_ta.sma(close_array, 20)  # 避免 list 转换
```

---

## 故障排除

### 问题 1: IDE 没有类型提示

**解决方案**:
1. 检查 `.pyi` 文件存在:
   ```bash
   ls -la src/haze_library/*.pyi
   ```

2. 检查 `py.typed` 标记文件:
   ```bash
   ls -la src/haze_library/py.typed
   ```

3. 重启 IDE 或重新加载 Python 扩展

4. 检查 Python 路径:
   ```python
   import sys
   print(sys.path)
   ```

### 问题 2: mypy 找不到类型存根

**解决方案**:
1. 确保项目已安装:
   ```bash
   pip install -e .
   ```

2. 添加 `MYPYPATH` 环境变量:
   ```bash
   export MYPYPATH=/Users/zhaoleon/Desktop/haze/haze/src
   ```

3. 使用 `--follow-imports=skip`:
   ```bash
   mypy --follow-imports=skip your_file.py
   ```

### 问题 3: 函数废弃警告

**原因**: 使用了 `py_` 前缀的函数

**解决方案**: 使用无前缀版本
```python
# ❌ 旧式 (已废弃)
from haze_library import py_sma

# ✅ 新式 (推荐)
from haze_library import sma
```

---

## 参考链接

- **项目主页**: `/Users/zhaoleon/Desktop/haze/haze`
- **详细报告**: `TYPE_STUBS_REPORT.md`
- **验证脚本**: `verify_type_stubs.py`
- **示例代码**: `examples/type_hints_demo.py`
- **生成脚本**: `generate_pyi.py`

---

## 贡献指南

### 添加新函数时

1. 在 Rust 中实现函数
2. 运行生成脚本:
   ```bash
   python3 generate_pyi.py
   ```
3. 验证类型存根:
   ```bash
   python3 verify_type_stubs.py
   ```
4. 测试 IDE 支持

### 更新文档字符串

编辑 `generate_enhanced_pyi.py` 中的 `FUNCTION_DOCS` 字典:

```python
FUNCTION_DOCS = {
    'py_new_indicator': '''Calculate New Indicator.

    Args:
        data: Input data
        period: Calculation period

    Returns:
        Indicator values
    ''',
}
```

然后运行:
```bash
python3 generate_enhanced_pyi.py
```

---

## 总结

✅ **已完成**:
- 222 个函数的完整类型签名
- IDE 自动补全支持
- 参数提示和文档
- mypy 类型检查支持
- PEP 561 合规

🚀 **下一步**:
- 在 IDE 中测试类型提示
- 集成到 CI/CD 流程
- 生成 API 文档
- 添加更多示例代码

---

**最后更新**: 2025-12-26
**作者**: Claude Code with Haze Team
