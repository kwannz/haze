# Haze-Library 指标实现计划

## 参考库分析

### pandas-ta-kw (212 指标)
- **Volatility** (14): ATR, True Range, Bollinger Bands, Donchian, Keltner Channel, NATR, RVI 等
- **Trend** (19): ADX, Aroon, PSAR, QStick, VHF, Vortex 等
- **Momentum** (46): RSI, MACD, Stochastic, StochRSI, CCI, AO, Fisher, KDJ, Williams %R 等
- **Volume** (~17): 待统计
- **Overlap** (~37): SMA, EMA, WMA, HMA, VWAP 等

### ta-lib (164 C 函数)
- 经典技术分析函数库
- 高精度浮点计算

### pyharmonics
- XABCD 谐波模式（Gartley, Bat, Crab 等 10 种）
- ABCD 模式（28 种变体）
- 背离检测

## 实施策略（分阶段）

### Phase 1: 基础设施 (0.5 天)
- Rust 基础类型（Candle, OHLCV）
- 工具函数（SMA, EMA, 基础统计）

### Phase 2: Volatility 指标 (1 天)
优先级：
1. **True Range** - 所有波动率指标的基础
2. **ATR** (Average True Range) - 最常用
3. **Bollinger Bands** - 高频使用
4. **Donchian Channel**
5. **Keltner Channel**
6. **NATR** (Normalized ATR)

### Phase 3: Momentum 指标 (2 天)
优先级：
1. **RSI** (Relative Strength Index) - 最常用
2. **MACD** (Moving Average Convergence Divergence) - 核心指标
3. **Stochastic Oscillator** - 经典指标
4. **StochRSI** - RSI 变体
5. **CCI** (Commodity Channel Index)
6. **Williams %R**
7. **Fisher Transform**
8. **Awesome Oscillator (AO)**
9. **MOM** (Momentum)
10. **ROC** (Rate of Change)

### Phase 4: Trend 指标 (1.5 天)
优先级：
1. **ADX** (Average Directional Index) - 趋势强度
2. **SuperTrend** - 交易信号
3. **Aroon** - 趋势识别
4. **PSAR** (Parabolic SAR) - 止损点
5. **Vortex Indicator**
6. **Choppiness Index**

### Phase 5: Overlap/MA 指标 (1 天)
优先级：
1. **SMA** (Simple Moving Average) - 基础
2. **EMA** (Exponential MA) - 最常用
3. **WMA** (Weighted MA)
4. **HMA** (Hull MA) - 低延迟
5. **VWAP** (Volume Weighted Average Price) - 日内交易
6. **TEMA** (Triple EMA)
7. **DEMA** (Double EMA)
8. **ZLMA** (Zero Lag MA)

### Phase 6: Volume 指标 (1 天)
优先级：
1. **Volume Profile** - 价格区间成交量
2. **OBV** (On-Balance Volume)
3. **VWAP** (已在 Overlap 实现)
4. **CMF** (Chaikin Money Flow)
5. **MFI** (Money Flow Index)
6. **AD** (Accumulation/Distribution)

### Phase 7: Harmonics 模式 (1.5 天)
优先级：
1. **Swing Points Detection** - 转折点识别
2. **XABCD Patterns** (10 种):
   - Gartley
   - Bat
   - Butterfly
   - Crab
   - Shark
3. **ABCD Patterns** - 简化模式
4. **Fibonacci Retracements**

### Phase 8: 高级指标 (2 天)
- **Ichimoku Cloud**
- **Market Structure** (高低点识别)
- **Linear Regression** (趋势拟合)
- **Pivot Points** (支撑阻力)

### Phase 9: 性能优化 (1 天)
- SIMD 向量化（x86 AVX2）
- Rayon 并行计算
- 缓存优化

### Phase 10: 测试与验证 (1 天)
- 单元测试（每个指标）
- 精度对比测试（vs ta-lib/pandas-ta）
- 性能基准测试

## 总预计时间：~12 天

## 实现优先级（核心 20 指标）

### Tier 1 (必须立即实现，2 天)
1. True Range
2. ATR
3. RSI
4. MACD
5. EMA
6. SMA
7. Bollinger Bands
8. Stochastic

### Tier 2 (高优先级，3 天)
9. SuperTrend
10. ADX
11. Williams %R
12. CCI
13. VWAP
14. Volume Profile
15. Aroon
16. PSAR

### Tier 3 (中优先级，3 天)
17. Harmonics (XABCD)
18. Fibonacci
19. Ichimoku
20. Pivot Points

## 代码结构

```
rust/src/
├── lib.rs                 # PyO3 入口
├── types.rs               # Candle, OHLCV 类型
├── utils/
│   ├── mod.rs
│   ├── ma.rs             # 移动平均工具
│   └── stats.rs          # 统计工具
├── indicators/
│   ├── mod.rs
│   ├── volatility.rs     # ATR, BB, DC, KC
│   ├── momentum.rs       # RSI, MACD, Stoch, CCI
│   ├── trend.rs          # ADX, SuperTrend, Aroon
│   ├── volume.rs         # VP, OBV, VWAP
│   ├── overlap.rs        # SMA, EMA, WMA
│   └── harmonics.rs      # XABCD patterns
└── tests/
    ├── volatility_tests.rs
    ├── momentum_tests.rs
    └── bench.rs          # 性能基准
```

## 下一步行动
1. 创建 Rust 基础架构
2. 实现 Tier 1 核心指标（True Range → ATR → RSI → MACD → EMA/SMA → BB → Stoch）
3. 编写单元测试验证精度
4. 开始 Tier 2 指标实现
