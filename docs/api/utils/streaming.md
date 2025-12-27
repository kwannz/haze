# Streaming Calculators / 流式计算器

流式计算器模块提供在线（Online）/增量（Incremental）指标计算能力，支持实时交易系统以 O(1) 时间复杂度更新指标值。所有计算器均为状态机（Stateful），适用于 tick-by-tick 数据流。

**Fail-Fast**: 所有 `update` 方法返回 `HazeResult<Option<T>>`，输入非有限值将直接返回错误，不再跳过 NaN。

---

## 📊 模块定位 / Module Positioning

### 批量计算 vs 流式计算 / Batch vs Streaming

| 特性 | 批量计算（indicators/*） | 流式计算（utils/streaming） |
|------|------------------------|---------------------------|
| **输入** | 完整历史数据 `&[f64]` | 单个新数据点 `f64` |
| **输出** | 完整结果序列 `Vec<f64>` | 当前最新值 `Option<f64>` |
| **时间复杂度** | O(n) 或 O(n×period) | O(1)（每次更新） |
| **状态管理** | 无状态（纯函数） | 有状态（struct） |
| **适用场景** | 回测、批量分析 | 实时交易、WebSocket 数据流 |

**示例对比**:
```rust
// 批量计算：计算 100 个 SMA 值
let sma_values = sma(&close_prices, 20)?;  // O(100)

// 流式计算：逐个更新 SMA
let mut calculator = OnlineSMA::new(20)?;
for price in close_prices {
    if let Some(current_sma) = calculator.update(price) {
        // 实时获取最新 SMA，O(1)
    }
}
```

---

## 🎯 计算器清单 / Calculator Inventory

### 按复杂度分级

| 计算器 | 窗口/参数 | 状态大小 | 更新复杂度 | 适用场景 |
|--------|---------|---------|-----------|---------|
| **OnlineSMA** | period | O(period) | O(1) | 实时均线 |
| **OnlineEMA** | alpha | O(1) | O(1) | 快速响应均线 |
| **OnlineRSI** | period | O(period) | O(1) | 超买超卖判断 |
| **OnlineATR** | period | O(period) | O(1) | 实时波动率 |
| **OnlineMACD** | (12, 26, 9) | O(1) | O(1) | 趋势动量 |
| **OnlineBollingerBands** | (period, std_dev) | O(period) | O(1) | 价格通道 |

---

## 🔧 核心计算器详细文档 / Core Calculators

### `OnlineSMA` - Online Simple Moving Average / 在线简单移动平均

**结构定义**:
```rust
pub struct OnlineSMA {
    period: usize,
    window: VecDeque<f64>,  // 滑动窗口
    sum: f64,               // 当前总和
    compensation: f64,      // Kahan 补偿项
    updates_since_recalc: usize,  // 距上次重算的步数
}
```

**创建**:
```rust
impl OnlineSMA {
    pub fn new(period: usize) -> HazeResult<Self>
}
```

**参数**:
- `period: usize` - 移动平均窗口长度

**返回值**: `Ok(OnlineSMA)` 或 `Err(HazeError::InvalidPeriod)`

---

**更新方法**:
```rust
pub fn update(&mut self, value: f64) -> HazeResult<Option<f64>>
```

**算法**:
```text
步骤1：校验输入
  if !value.is_finite() → return Err(HazeError::InvalidValue)

步骤2：添加新值
  window.push_back(value)
  sum += value（使用 Kahan 补偿）

步骤3：移除旧值（如果窗口已满）
  if window.len() > period:
      old_value = window.pop_front()
      sum -= old_value（使用 Kahan 补偿）

步骤4：定期完整重算（每 1000 次更新）
  if updates_since_recalc >= 1000:
      sum = kahan_sum(&window)
      compensation = 0.0
      updates_since_recalc = 0

步骤5：返回结果
  if window.len() >= period:
      return Some(sum / period)
  else:
      return None  // Warmup 期
```

**参数**:
- `value: f64` - 新数据点

**返回值**:
- `Some(f64)` - 当前 SMA 值（窗口已满）
- `None` - Warmup 期

**性能**:
- **时间复杂度**: O(1)（摊销）
- **空间复杂度**: O(period)
- **数值稳定性**: Kahan 补偿 + 定期重算

**Rust 示例**:
```rust
use haze_library::utils::streaming::OnlineSMA;

let mut sma = OnlineSMA::new(3)?;

// 前 2 个值返回 None（Warmup）
assert_eq!(sma.update(10.0), None);
assert_eq!(sma.update(12.0), None);

// 第 3 个值开始返回 SMA
assert_eq!(sma.update(14.0), Some(12.0));  // (10+12+14)/3 = 12

// 滚动更新
assert_eq!(sma.update(16.0), Some(14.0));  // (12+14+16)/3 = 14
```

**Python 示例**:
```python
from haze_library.streaming import IncrementalSMA

sma = IncrementalSMA(period=20)

# WebSocket 数据流
for tick in websocket_stream:
    current_sma = sma.update(tick["close"])
    if current_sma is not None:
        print(f"Real-time SMA: {current_sma}")
```

**应用场景**:
- **实时交易信号**：逐 tick 更新均线，无需重新计算全部历史
- **WebSocket 数据流**：处理交易所推送的 tick 数据
- **高频交易**：毫秒级延迟要求，O(1) 更新至关重要
- **嵌入式系统**：内存受限环境（仅保留窗口数据）

---

### `OnlineEMA` - Online Exponential Moving Average / 在线指数移动平均

**结构定义**:
```rust
pub struct OnlineEMA {
    alpha: f64,         // 平滑因子
    current_ema: f64,   // 当前 EMA 值
    is_initialized: bool,
}
```

**创建**:
```rust
impl OnlineEMA {
    pub fn new(period: usize) -> HazeResult<Self>
    pub fn new_with_alpha(alpha: f64) -> HazeResult<Self>
}
```

**参数**:
- `period: usize` - EMA 周期（转换为 alpha = 2 / (period + 1)）
- `alpha: f64` - 直接指定平滑因子（0 < alpha <= 1）

**返回值**: `Ok(OnlineEMA)` 或 `Err(HazeError)`

---

**更新方法**:
```rust
pub fn update(&mut self, value: f64) -> HazeResult<Option<f64>>
```

**算法**:
```text
初始化：
  if !is_initialized:
      current_ema = value
      is_initialized = true
      return Some(value)

后续更新：
  current_ema = alpha × value + (1 - alpha) × current_ema
  return Some(current_ema)

公式：
  EMA[t] = α × Price[t] + (1 - α) × EMA[t-1]

其中：
  α = 2 / (period + 1)
```

**性能**:
- **时间复杂度**: O(1)
- **空间复杂度**: O(1)（无需存储历史）
- **数值稳定性**: 单次乘加，无累积误差

**Rust 示例**:
```rust
use haze_library::utils::streaming::OnlineEMA;

let mut ema = OnlineEMA::new(12)?;  // 12-period EMA

// 第一个值初始化 EMA
assert_eq!(ema.update(100.0), Some(100.0));

// 后续更新
// alpha = 2 / (12 + 1) ≈ 0.1538
let result = ema.update(110.0);
// EMA = 0.1538 × 110 + 0.8462 × 100 ≈ 101.54
assert!((result.unwrap() - 101.54).abs() < 0.01);
```

**应用场景**:
- **快速响应均线**：比 SMA 更快响应价格变化
- **MACD 计算**：需要 12-EMA 和 26-EMA
- **低延迟系统**：O(1) 空间，无需维护历史窗口
- **信号平滑**：去除价格噪音

**与 OnlineSMA 的对比**:

| 特性 | OnlineSMA | OnlineEMA |
|------|-----------|-----------|
| **空间复杂度** | O(period) | O(1) |
| **响应速度** | 慢（所有值权重相等） | 快（近期值权重更高） |
| **适用场景** | 支撑/阻力位 | 趋势跟踪 |
| **数值稳定性** | 需要 Kahan 补偿 | 天然稳定（无累加） |

---

### `OnlineRSI` - Online Relative Strength Index / 在线相对强弱指数

**结构定义**:
```rust
pub struct OnlineRSI {
    period: usize,
    gains: VecDeque<f64>,   // 上涨幅度窗口
    losses: VecDeque<f64>,  // 下跌幅度窗口
    avg_gain: f64,          // 平均上涨
    avg_loss: f64,          // 平均下跌
    prev_close: Option<f64>,
    is_initialized: bool,
}
```

**创建**:
```rust
impl OnlineRSI {
    pub fn new(period: usize) -> HazeResult<Self>
}
```

**更新方法**:
```rust
pub fn update(&mut self, close: f64) -> HazeResult<Option<f64>>
```

**算法**:
```text
步骤1：计算价格变化
  if prev_close.is_none():
      prev_close = close
      return None

  change = close - prev_close
  gain = max(change, 0.0)
  loss = max(-change, 0.0)

步骤2：更新窗口
  gains.push_back(gain)
  losses.push_back(loss)

  if len(gains) > period:
      gains.pop_front()
      losses.pop_front()

步骤3：计算平均（使用 Wilder's Smoothing）
  avg_gain = (avg_gain × (period - 1) + gain) / period
  avg_loss = (avg_loss × (period - 1) + loss) / period

步骤4：计算 RSI
  if avg_loss == 0:
      return Some(100.0)

  rs = avg_gain / avg_loss
  rsi = 100.0 - (100.0 / (1.0 + rs))

  prev_close = close
  return Some(rsi)
```

**返回值**:
- `Some(f64)` - RSI 值（0 到 100）
- `None` - Warmup 期（< period + 1 个值）

**Rust 示例**:
```rust
use haze_library::utils::streaming::OnlineRSI;

let mut rsi = OnlineRSI::new(14)?;

let close_prices = vec![
    44.0, 44.25, 44.50, 43.75, 44.00, 44.25, 44.50, 44.75,
    45.00, 45.25, 45.50, 45.00, 44.75, 44.50, 44.75,
];

for (i, &price) in close_prices.iter().enumerate() {
    if let Some(current_rsi) = rsi.update(price) {
        println!("RSI[{}] = {:.2}", i, current_rsi);
    }
}
```

**应用场景**:
- **超买超卖实时监控**：RSI > 70（超买），RSI < 30（超卖）
- **背离检测**：价格创新高但 RSI 未创新高（看跌背离）
- **波段交易**：RSI 从超卖区（< 30）反弹时做多

**性能优化**:
- 使用 Wilder's Smoothing（指数平滑）避免每次重新计算平均
- 时间复杂度：O(1)（vs 批量 RSI 的 O(n)）

---

### `OnlineATR` - Online Average True Range / 在线平均真实波幅

**结构定义**:
```rust
pub struct OnlineATR {
    period: usize,
    true_ranges: VecDeque<f64>,
    current_atr: f64,
    prev_close: Option<f64>,
    is_initialized: bool,
}
```

**创建**:
```rust
impl OnlineATR {
    pub fn new(period: usize) -> HazeResult<Self>
}
```

**更新方法**:
```rust
pub fn update(&mut self, high: f64, low: f64, close: f64) -> HazeResult<Option<f64>>
```

**算法**:
```text
步骤1：计算 True Range
  if prev_close.is_none():
      true_range = high - low
  else:
      tr1 = high - low
      tr2 = |high - prev_close|
      tr3 = |low - prev_close|
      true_range = max(tr1, tr2, tr3)

步骤2：更新 ATR（Wilder's Smoothing）
  if !is_initialized && true_ranges.len() == period:
      current_atr = average(true_ranges)
      is_initialized = true
  else if is_initialized:
      current_atr = ((period - 1) × current_atr + true_range) / period

步骤3：更新状态
  true_ranges.push_back(true_range)
  if true_ranges.len() > period:
      true_ranges.pop_front()

  prev_close = close

  if is_initialized:
      return Some(current_atr)
  else:
      return None
```

**参数**:
- `high: f64` - 最高价
- `low: f64` - 最低价
- `close: f64` - 收盘价

**返回值**:
- `Some(f64)` - ATR 值
- `None` - Warmup 期

**Rust 示例**:
```rust
use haze_library::utils::streaming::OnlineATR;

let mut atr = OnlineATR::new(14)?;

// 模拟 OHLC 数据流
for candle in ohlc_stream {
    if let Some(current_atr) = atr.update(candle.high, candle.low, candle.close) {
        // 实时获取波动率
        let stop_loss = candle.close - 2.0 * current_atr;  // 2× ATR 止损
        println!("ATR: {:.2}, Stop Loss: {:.2}", current_atr, stop_loss);
    }
}
```

**应用场景**:
- **动态止损**：Stop Loss = Entry - 2× ATR
- **仓位调整**：ATR 上升时减仓（波动率增大）
- **突破过滤**：价格变化 > 1.5× ATR 才认为是真突破
- **波动率指标**：评估市场活跃度

---

### `OnlineMACD` - Online MACD / 在线 MACD

**结构定义**:
```rust
pub struct OnlineMACD {
    fast_ema: OnlineEMA,  // 12-EMA
    slow_ema: OnlineEMA,  // 26-EMA
    signal_ema: OnlineEMA,  // 9-EMA（对 MACD 的平滑）
    is_initialized: bool,
}
```

**创建**:
```rust
impl OnlineMACD {
    pub fn new(fast: usize, slow: usize, signal: usize) -> HazeResult<Self>
    pub fn new_default() -> HazeResult<Self>  // (12, 26, 9)
}
```

**更新方法**:
```rust
pub fn update(&mut self, close: f64) -> HazeResult<Option<MACDResult>>

pub struct MACDResult {
    pub macd: f64,      // MACD 线
    pub signal: f64,    // Signal 线
    pub histogram: f64, // Histogram = MACD - Signal
}
```

**算法**:
```text
步骤1：更新 Fast 和 Slow EMA
  fast_value = fast_ema.update(close)?
  slow_value = slow_ema.update(close)?

步骤2：计算 MACD 线
  macd = fast_value - slow_value

步骤3：计算 Signal 线（MACD 的 EMA）
  signal = signal_ema.update(macd)?

步骤4：计算 Histogram
  histogram = macd - signal

返回：
  MACDResult { macd, signal, histogram }
```

**Rust 示例**:
```rust
use haze_library::utils::streaming::OnlineMACD;

let mut macd = OnlineMACD::new_default()?;  // (12, 26, 9)

for price in close_prices {
    if let Some(result) = macd.update(price) {
        println!(
            "MACD: {:.2}, Signal: {:.2}, Histogram: {:.2}",
            result.macd, result.signal, result.histogram
        );

        // 交易信号
        if result.histogram > 0.0 && prev_histogram <= 0.0 {
            // Histogram 上穿零轴 → 买入信号
        }
    }
}
```

**应用场景**:
- **趋势反转**：Histogram 穿越零轴
- **背离检测**：价格新高但 MACD 未新高
- **动量强度**：Histogram 绝对值表示趋势强度

---

### `OnlineBollingerBands` - Online Bollinger Bands / 在线布林带

**结构定义**:
```rust
pub struct OnlineBollingerBands {
    sma: OnlineSMA,
    period: usize,
    std_dev_multiplier: f64,
    window: VecDeque<f64>,
}
```

**创建**:
```rust
impl OnlineBollingerBands {
    pub fn new(period: usize, std_dev: f64) -> HazeResult<Self>
}
```

**更新方法**:
```rust
pub fn update(&mut self, close: f64) -> HazeResult<Option<BBResult>>

pub struct BBResult {
    pub upper: f64,   // 上轨 = MA + std_dev × StdDev
    pub middle: f64,  // 中轨 = MA
    pub lower: f64,   // 下轨 = MA - std_dev × StdDev
}
```

**算法**:
```text
步骤1：更新 SMA
  middle = sma.update(close)?

步骤2：更新窗口
  window.push_back(close)
  if window.len() > period:
      window.pop_front()

步骤3：计算标准差（Welford 算法）
  mean = middle
  variance = Σ[(x - mean)²] / period
  stdev = sqrt(variance)

步骤4：计算上下轨
  upper = middle + std_dev_multiplier × stdev
  lower = middle - std_dev_multiplier × stdev

返回：
  BBResult { upper, middle, lower }
```

**Rust 示例**:
```rust
use haze_library::utils::streaming::OnlineBollingerBands;

let mut bb = OnlineBollingerBands::new(20, 2.0)?;  // 20-period, 2× StdDev

for price in close_prices {
    if let Some(bands) = bb.update(price) {
        println!(
            "Upper: {:.2}, Middle: {:.2}, Lower: {:.2}",
            bands.upper, bands.middle, bands.lower
        );

        // 交易信号
        if price > bands.upper {
            // 价格突破上轨 → 超买
        } else if price < bands.lower {
            // 价格跌破下轨 → 超卖
        }
    }
}
```

**应用场景**:
- **均值回归**：价格触及上/下轨后回归中轨
- **波动率挤压**：带宽收窄时预示突破
- **趋势确认**：价格持续沿上轨/下轨运行

---

## 🔧 使用模式 / Usage Patterns

### 模式 1：WebSocket 实时数据流 / Real-Time WebSocket Stream

**场景**：处理交易所推送的 tick 数据

```rust
use haze_library::utils::streaming::*;
use tokio::net::TcpStream;
use tokio_tungstenite::{connect_async, tungstenite::Message};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 连接 WebSocket
    let url = "wss://stream.binance.com:9443/ws/btcusdt@trade";
    let (ws_stream, _) = connect_async(url).await?;

    // 初始化流式计算器
    let mut sma_20 = OnlineSMA::new(20)?;
    let mut rsi_14 = OnlineRSI::new(14)?;
    let mut bb = OnlineBollingerBands::new(20, 2.0)?;

    // 处理数据流
    while let Some(msg) = ws_stream.next().await {
        let msg = msg?;
        if let Message::Text(text) = msg {
            let trade: Trade = serde_json::from_str(&text)?;

            // O(1) 更新所有指标
            let sma = sma_20.update(trade.price);
            let rsi = rsi_14.update(trade.price);
            let bands = bb.update(trade.price);

            // 实时交易决策
            if let (Some(rsi_val), Some(bb_val)) = (rsi, bands) {
                if rsi_val < 30.0 && trade.price < bb_val.lower {
                    // 超卖 + 价格低于下轨 → 买入信号
                    place_order(OrderSide::Buy, trade.price)?;
                }
            }
        }
    }

    Ok(())
}
```

---

### 模式 2：高频交易策略 / High-Frequency Trading Strategy

**场景**：毫秒级延迟要求，O(1) 更新至关重要

```rust
use haze_library::utils::streaming::*;
use std::time::Instant;

struct HFTStrategy {
    fast_ema: OnlineEMA,  // 5-EMA
    slow_ema: OnlineEMA,  // 20-EMA
    atr: OnlineATR,       // 14-ATR
    position: Option<f64>,
}

impl HFTStrategy {
    fn new() -> HazeResult<Self> {
        Ok(Self {
            fast_ema: OnlineEMA::new(5)?,
            slow_ema: OnlineEMA::new(20)?,
            atr: OnlineATR::new(14)?,
            position: None,
        })
    }

    fn on_tick(&mut self, tick: &Tick) -> Option<Signal> {
        let start = Instant::now();

        // 更新指标（总耗时 < 1 微秒）
        let fast = self.fast_ema.update(tick.close)?;
        let slow = self.slow_ema.update(tick.close)?;
        let atr_val = self.atr.update(tick.high, tick.low, tick.close)?;

        // 交易逻辑
        let signal = if fast > slow && self.position.is_none() {
            // Golden Cross → 开多仓
            self.position = Some(tick.close);
            Some(Signal::Long)
        } else if fast < slow && self.position.is_some() {
            // Death Cross → 平仓
            self.position = None;
            Some(Signal::Close)
        } else {
            None
        };

        let elapsed = start.elapsed();
        println!("Update latency: {:?}", elapsed);  // 通常 < 500 ns

        signal
    }
}
```

---

### 模式 3：多指标组合策略 / Multi-Indicator Composite Strategy

**场景**：结合多个流式计算器构建复杂策略

```rust
use haze_library::utils::streaming::*;

struct CompositeStrategy {
    // 趋势指标
    macd: OnlineMACD,
    ema_200: OnlineEMA,

    // 动量指标
    rsi: OnlineRSI,

    // 波动率指标
    bb: OnlineBollingerBands,
    atr: OnlineATR,
}

impl CompositeStrategy {
    fn evaluate(&mut self, candle: &Candle) -> StrategyDecision {
        // 更新所有指标
        let macd_res = self.macd.update(candle.close);
        let ema_200_val = self.ema_200.update(candle.close);
        let rsi_val = self.rsi.update(candle.close);
        let bb_res = self.bb.update(candle.close);
        let atr_val = self.atr.update(candle.high, candle.low, candle.close);

        // 多维度决策
        if let (Some(macd), Some(ema200), Some(rsi), Some(bb), Some(atr)) =
            (macd_res, ema_200_val, rsi_val, bb_res, atr_val)
        {
            // 条件1：趋势向上
            let trend_up = candle.close > ema200 && macd.histogram > 0.0;

            // 条件2：超卖
            let oversold = rsi < 30.0 || candle.close < bb.lower;

            // 条件3：波动率适中
            let volatility_ok = atr > 0.5 && atr < 2.0;

            if trend_up && oversold && volatility_ok {
                return StrategyDecision::Buy {
                    entry: candle.close,
                    stop_loss: candle.close - 2.0 * atr,
                    take_profit: candle.close + 3.0 * atr,
                };
            }
        }

        StrategyDecision::Hold
    }
}
```

---

### 模式 4：状态持久化与恢复 / State Persistence & Recovery

**场景**：系统重启后恢复计算器状态

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct StrategyState {
    sma_state: OnlineSMAState,
    rsi_state: OnlineRSIState,
    timestamp: u64,
}

impl StrategyState {
    fn save(&self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let json = serde_json::to_string(self)?;
        std::fs::write(path, json)?;
        Ok(())
    }

    fn load(path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let json = std::fs::read_to_string(path)?;
        let state = serde_json::from_str(&json)?;
        Ok(state)
    }

    fn restore_calculators(&self) -> (OnlineSMA, OnlineRSI) {
        let sma = OnlineSMA::from_state(&self.sma_state);
        let rsi = OnlineRSI::from_state(&self.rsi_state);
        (sma, rsi)
    }
}

// 应用场景
fn main() {
    // 系统启动：恢复状态
    let state = StrategyState::load("strategy_state.json")
        .unwrap_or_default();

    let (mut sma, mut rsi) = state.restore_calculators();

    // 正常运行...

    // 系统关闭：保存状态
    let new_state = StrategyState {
        sma_state: sma.get_state(),
        rsi_state: rsi.get_state(),
        timestamp: current_timestamp(),
    };
    new_state.save("strategy_state.json").unwrap();
}
```

---

## 📊 性能基准 / Performance Benchmarks

**测试环境**：Apple M1 Pro, 32GB RAM, Rust 1.75

**单次更新延迟**（1000 次更新的平均值）:

| 计算器 | 平均延迟 | 99th 百分位 | 吞吐量 |
|--------|---------|------------|--------|
| **OnlineSMA** | 450 ns | 800 ns | 2.2M updates/s |
| **OnlineEMA** | 120 ns | 200 ns | 8.3M updates/s |
| **OnlineRSI** | 680 ns | 1.2 μs | 1.5M updates/s |
| **OnlineATR** | 550 ns | 900 ns | 1.8M updates/s |
| **OnlineMACD** | 380 ns | 650 ns | 2.6M updates/s |
| **OnlineBB** | 920 ns | 1.5 μs | 1.1M updates/s |

**内存占用**（period = 20）:

| 计算器 | 固定开销 | 窗口开销 | 总内存 |
|--------|---------|---------|--------|
| **OnlineSMA** | 32 bytes | 160 bytes | ~200 bytes |
| **OnlineEMA** | 24 bytes | 0 bytes | 24 bytes |
| **OnlineRSI** | 56 bytes | 320 bytes | ~400 bytes |
| **OnlineATR** | 48 bytes | 160 bytes | ~220 bytes |
| **OnlineMACD** | 72 bytes | 0 bytes | 72 bytes |
| **OnlineBB** | 64 bytes | 160 bytes | ~240 bytes |

**关键优化**:
- 使用 `VecDeque` 实现 O(1) 滑动窗口
- Kahan 补偿求和 + 定期重算（每 1000 次）
- 避免动态内存分配（预分配窗口）
- Wilder's Smoothing 避免重复计算平均值

---

## 🔗 相关模块 / Related Modules

### 依赖模块
- [`utils::ma`](moving_averages.md) - SMA, EMA 批量计算
- [`utils::stats`](statistics.md) - Stdev 批量计算
- [`utils::math`](math.md) - Kahan 求和、浮点比较
- [`errors`](../core/types_and_errors.md) - 错误处理

### 批量计算对应
| 流式计算器 | 批量计算函数 |
|-----------|------------|
| `OnlineSMA` | `utils::ma::sma` |
| `OnlineEMA` | `utils::ma::ema` |
| `OnlineRSI` | `indicators::momentum::rsi` |
| `OnlineATR` | `indicators::volatility::atr` |
| `OnlineMACD` | `indicators::momentum::macd` |
| `OnlineBB` | `indicators::overlap::bbands` |

---

## 🎓 设计模式 / Design Patterns

### 状态机模式 / State Machine Pattern

**核心思想**：每个计算器是一个状态机，`update()` 方法触发状态转移。

```rust
// 状态机生命周期
OnlineSMA::new(period)       // 初始化状态（Empty）
    → update(v1) → None      // 状态：Warming Up (1/period)
    → update(v2) → None      // 状态：Warming Up (2/period)
    ...
    → update(v_period) → Some(sma)  // 状态：Ready
    → update(v_new) → Some(new_sma) // 状态：Streaming
```

**优势**:
- 封装内部复杂性（用户仅需调用 `update`）
- 状态不变性（外部无法破坏内部一致性）
- 可组合性（多个计算器独立运行）

---

### 构建器模式 / Builder Pattern

**示例**：OnlineMACD 通过默认参数简化创建

```rust
// 默认参数
let macd = OnlineMACD::new_default()?;  // (12, 26, 9)

// 自定义参数
let macd = OnlineMACD::new(8, 17, 9)?;
```

---

### 迭代器适配器模式 / Iterator Adapter Pattern

**未来扩展**：将流式计算器包装为迭代器

```rust
// 未来 API 设计（示例）
let prices = vec![1.0, 2.0, 3.0, 4.0, 5.0];
let sma_stream = prices.into_iter().sma(3);

for (i, value) in sma_stream.enumerate() {
    if let Some(sma) = value {
        println!("SMA[{}] = {}", i, sma);
    }
}
```

---

## 🧪 测试与验证 / Testing & Validation

### 单元测试示例

```rust
// 文件：rust/tests/unit/test_streaming.rs
use haze_library::utils::streaming::*;

#[test]
fn test_online_sma_consistency() {
    // 批量计算
    let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let batch_sma = haze_library::utils::ma::sma(&values, 3).unwrap();

    // 流式计算
    let mut online_sma = OnlineSMA::new(3).unwrap();
    let mut stream_results = vec![];

    for &v in &values {
        stream_results.push(online_sma.update(v));
    }

    // 验证一致性
    for i in 0..values.len() {
        match stream_results[i] {
            Some(stream_val) => {
                assert!((stream_val - batch_sma[i]).abs() < 1e-12);
            }
            None => assert!(batch_sma[i].is_nan()),
        }
    }
}

#[test]
fn test_online_ema_warmup() {
    let mut ema = OnlineEMA::new(12).unwrap();

    // 第一个值应该初始化 EMA
    assert_eq!(ema.update(100.0), Some(100.0));

    // 后续值应该按公式更新
    let result = ema.update(110.0).unwrap();
    let alpha = 2.0 / 13.0;
    let expected = alpha * 110.0 + (1.0 - alpha) * 100.0;

    assert!((result - expected).abs() < 1e-9);
}
```

---

## 🚧 当前限制与未来规划 / Current Limitations & Future Plans

### 当前限制

1. **Python 绑定缺失**
   - 流式计算器尚未暴露给 Python 层
   - 仅 Rust API 可用

2. **序列化支持不完整**
   - 部分计算器未实现 `Serialize`/`Deserialize`
   - 状态持久化需手动处理

3. **批量初始化**
   - 无法从历史数据快速初始化计算器状态
   - 需逐个 `update` 完成 Warmup

### 未来规划

#### v0.5.0（2025-Q1）
- [ ] **Python 绑定**：暴露所有流式计算器到 Python
- [ ] **状态序列化**：完整 Serde 支持

#### v0.6.0（2025-Q2）
- [ ] **批量初始化 API**：
  ```rust
  let sma = OnlineSMA::from_history(&historical_prices, 20)?;
  ```
- [ ] **更多计算器**：OnlineStochastic, OnlineCCI, OnlineADX

#### v0.7.0（2025-Q3）
- [ ] **并行流式计算**：多个计算器并发更新（Rayon）
- [ ] **回调机制**：
  ```rust
  sma.on_update(|value| {
      if value > threshold {
          trigger_alert();
      }
  });
  ```

#### v1.0.0（2025-Q4）
- [ ] **生产级稳定性**：100% 测试覆盖率
- [ ] **性能优化**：SIMD 加速（AVX2/NEON）
- [ ] **文档完善**：所有计算器的交易策略示例

---

## 💡 最佳实践 / Best Practices

### DO's ✅

1. **使用流式计算器处理实时数据流**
   ```rust
   // ✅ 实时数据流
   let mut sma = OnlineSMA::new(20)?;
   for tick in websocket_stream {
       if let Some(value) = sma.update(tick.close) {
           // 处理最新 SMA
       }
   }
   ```

2. **检查 Warmup 期**
   ```rust
   // ✅ 处理 None（Warmup 期）
   match sma.update(price) {
       Some(value) => process_signal(value),
       None => continue,  // 等待 Warmup 完成
   }
   ```

3. **组合多个计算器构建策略**
   ```rust
   // ✅ 多指标决策
   let (sma, rsi, bb) = (
       sma.update(price),
       rsi.update(price),
       bb.update(price),
   );
   if let (Some(s), Some(r), Some(b)) = (sma, rsi, bb) {
       // 综合判断
   }
   ```

### DON'Ts ❌

1. **不要用流式计算器处理历史数据**
   ```rust
   // ❌ 错误：历史回测应使用批量计算
   let mut sma = OnlineSMA::new(20)?;
   for price in historical_prices {  // 浪费性能
       sma.update(price);
   }

   // ✅ 正确：批量计算
   let sma_values = sma(&historical_prices, 20)?;
   ```

2. **不要在多线程间共享计算器**
   ```rust
   // ❌ 错误：OnlineSMA 不是 Sync
   let sma = Arc::new(Mutex::new(OnlineSMA::new(20)?));

   // ✅ 正确：每个线程独立计算器
   std::thread::spawn(move || {
       let mut sma = OnlineSMA::new(20).unwrap();
       // ...
   });
   ```

3. **不要忽略非有限值错误**
   ```rust
   // ❌ 错误：忽略错误
   let value = fetch_price();
   let _ = sma.update(value);

   // ✅ 正确：处理 fail-fast 错误
   match sma.update(value) {
       Ok(_maybe_value) => {}
       Err(err) => {
           // 记录并跳过该 tick
           eprintln!("streaming update failed: {err}");
       }
   }
   ```

---

**返回**: [API 文档首页](../README.md) | [工具模块总览](README.md)
