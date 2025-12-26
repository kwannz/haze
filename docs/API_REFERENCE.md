# Haze-Library API Reference

**Complete Technical Indicator API Documentation**

**Version**: 1.0 | **Total Indicators**: 215 | **Last Updated**: 2025-12-26

---

## Table of Contents

1. [Moving Averages (16 indicators)](#moving-averages)
2. [Momentum Indicators (17 indicators)](#momentum-indicators)
3. [Trend Indicators (14 indicators)](#trend-indicators)
4. [Volatility Indicators (10 indicators)](#volatility-indicators)
5. [Volume Indicators (11 indicators)](#volume-indicators)
6. [Candlestick Patterns (61 indicators)](#candlestick-patterns)
7. [Statistical Functions (13 indicators)](#statistical-functions)
8. [Price Transform (4 indicators)](#price-transform)
9. [Math Operations (25 functions)](#math-operations)
10. [Overlap Studies (6 indicators)](#overlap-studies)
11. [Cycle Indicators (5 indicators)](#cycle-indicators)
12. [Fibonacci & Pivot Points (8 indicators)](#fibonacci--pivot-points)
13. [pandas-ta Exclusive (25 indicators)](#pandas-ta-exclusive-indicators)
14. [ML-Enhanced Signals (4 indicators)](#ml-enhanced-signals)
15. [Harmonic Patterns (3 indicators)](#harmonic-patterns)
16. [Market Structure (3 indicators)](#market-structure)

---

## Moving Averages

### `py_sma(values, period)`

**Category**: Moving Average / Overlap

**Description**: Simple Moving Average - arithmetic mean of prices over a specified period.

**Parameters**:
- `values` (List[float]): Price data (typically close prices)
- `period` (int): Lookback period

**Returns**: List[float] - SMA values (first `period-1` values are NaN)

**Complexity**: O(n)

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 101.5, 103.0]
sma = haze.py_sma(close, period=3)
# Result: [NaN, NaN, 101.0, 101.5, 102.17]
```

**Related**: [py_ema](#py_emavalues-period), [py_wma](#py_wmavalues-period)

---

### `py_ema(values, period)`

**Category**: Moving Average / Overlap

**Description**: Exponential Moving Average - weighted average giving more importance to recent prices. Uses smoothing factor alpha = 2/(period+1).

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period

**Returns**: List[float] - EMA values

**Algorithm**:
```
alpha = 2 / (period + 1)
EMA[0..period-1] = SMA(period)  # Initial seed
EMA[i] = alpha * value[i] + (1 - alpha) * EMA[i-1]
```

**Complexity**: O(n)

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
ema = haze.py_ema(close, period=3)
```

**Related**: [py_dema](#py_demavalues-period), [py_tema](#py_temavalues-period)

---

### `py_wma(values, period)`

**Category**: Moving Average / Overlap

**Description**: Weighted Moving Average - linear weighted average where recent prices have higher weights.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period

**Returns**: List[float] - WMA values

**Algorithm**:
```
weights = [1, 2, 3, ..., period]
WMA = sum(value[i] * weight[i]) / sum(weights)
```

**Complexity**: O(n * period)

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
wma = haze.py_wma(close, period=3)
```

---

### `py_rma(values, period)`

**Category**: Moving Average / Overlap

**Description**: Wilder's Moving Average (RMA) - smoothed moving average used in RSI, ATR calculations. Uses alpha = 1/period.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period

**Returns**: List[float] - RMA values

**Algorithm**:
```
alpha = 1 / period
RMA[i] = alpha * value[i] + (1 - alpha) * RMA[i-1]
```

**Common Usage**: ATR, RSI internal calculations

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
rma = haze.py_rma(close, period=14)
```

---

### `py_hma(values, period)`

**Category**: Moving Average / Overlap

**Description**: Hull Moving Average - low-lag moving average designed by Alan Hull.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period

**Returns**: List[float] - HMA values

**Algorithm**:
```
half_period = period / 2
sqrt_period = sqrt(period)
HMA = WMA(2 * WMA(half_period) - WMA(period), sqrt_period)
```

**Characteristics**: Faster response, reduced lag compared to SMA/EMA

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0]
hma = haze.py_hma(close, period=9)
```

---

### `py_dema(values, period)`

**Category**: Moving Average / Overlap

**Description**: Double Exponential Moving Average - reduces lag of standard EMA.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period

**Returns**: List[float] - DEMA values

**Algorithm**:
```
DEMA = 2 * EMA(period) - EMA(EMA(period))
```

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
dema = haze.py_dema(close, period=10)
```

**Related**: [py_tema](#py_temavalues-period)

---

### `py_tema(values, period)`

**Category**: Moving Average / Overlap

**Description**: Triple Exponential Moving Average - further reduces lag compared to DEMA.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period

**Returns**: List[float] - TEMA values

**Algorithm**:
```
TEMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))
```

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
tema = haze.py_tema(close, period=10)
```

---

### `py_zlma(values, period)`

**Category**: Moving Average / Overlap

**Description**: Zero Lag Moving Average - attempts to eliminate EMA lag by adjusting for price momentum.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period

**Returns**: List[float] - ZLMA values

**Algorithm**:
```
lag = (period - 1) / 2
adjusted_data = 2 * values - values[lag_ago]
ZLMA = EMA(adjusted_data, period)
```

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
zlma = haze.py_zlma(close, period=10)
```

---

### `py_t3(values, period, v_factor=0.7)`

**Category**: Moving Average / Overlap

**Description**: Tillson T3 Moving Average - six-times smoothed EMA with reduced noise.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int): Lookback period
- `v_factor` (float, optional): Smoothing factor (default: 0.7)

**Returns**: List[float] - T3 values

**Algorithm**: Uses 6 layers of EMA with special coefficients based on v_factor.

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
t3 = haze.py_t3(close, period=5, v_factor=0.7)
```

---

### `py_kama(values, period=10, fast_period=2, slow_period=30)`

**Category**: Moving Average / Overlap

**Description**: Kaufman's Adaptive Moving Average - adjusts smoothing based on market volatility.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Efficiency ratio period (default: 10)
- `fast_period` (int, optional): Fast EMA period (default: 2)
- `slow_period` (int, optional): Slow EMA period (default: 30)

**Returns**: List[float] - KAMA values

**Algorithm**:
```
ER = |Price Change| / Sum(|Daily Changes|)  # Efficiency Ratio
SC = [ER * (Fast_SC - Slow_SC) + Slow_SC]^2  # Smoothing Constant
KAMA[i] = KAMA[i-1] + SC * (Price[i] - KAMA[i-1])
```

**Use Case**: Adapts to trending/ranging markets automatically

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
kama = haze.py_kama(close, period=10, fast_period=2, slow_period=30)
```

---

### `py_frama(values, period=16)`

**Category**: Moving Average / Overlap

**Description**: Fractal Adaptive Moving Average - uses fractal dimension to adjust smoothing.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Lookback period (must be even, default: 16)

**Returns**: List[float] - FRAMA values

**Note**: Period must be an even number.

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
frama = haze.py_frama(close, period=16)
```

---

### `py_alma(values, period=9, offset=0.85, sigma=6.0)`

**Category**: Moving Average / Overlap

**Description**: Arnaud Legoux Moving Average - uses Gaussian distribution weights.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Lookback period (default: 9)
- `offset` (float, optional): Gaussian offset 0-1 (default: 0.85, higher = smoother)
- `sigma` (float, optional): Gaussian standard deviation (default: 6.0)

**Returns**: List[float] - ALMA values

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
alma = haze.py_alma(close, period=9, offset=0.85, sigma=6.0)
```

---

### `py_vidya(close, period=14)`

**Category**: Moving Average / Overlap

**Description**: Variable Index Dynamic Average - adapts to volatility using standard deviation.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - VIDYA values

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
vidya = haze.py_vidya(close, period=14)
```

---

### `py_pwma(values, period=5)`

**Category**: Moving Average / Overlap

**Description**: Pascal's Weighted Moving Average - uses Pascal's triangle coefficients as weights.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Lookback period (default: 5)

**Returns**: List[float] - PWMA values

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
pwma = haze.py_pwma(close, period=5)
```

---

### `py_sinwma(values, period=14)`

**Category**: Moving Average / Overlap

**Description**: Sine Weighted Moving Average - uses sine curve as weight distribution.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - SINWMA values

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
sinwma = haze.py_sinwma(close, period=14)
```

---

### `py_swma(values, period=7)`

**Category**: Moving Average / Overlap

**Description**: Symmetric Weighted Moving Average - uses symmetric triangular weights.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Lookback period (default: 7)

**Returns**: List[float] - SWMA values

**Example**:
```python
import haze_library as haze
close = [100.0, 101.0, 102.0, 103.0, 104.0]
swma = haze.py_swma(close, period=7)
```

---

## Momentum Indicators

### `py_rsi(close, period=14)`

**Category**: Momentum

**Description**: Relative Strength Index - measures momentum on a 0-100 scale. Values above 70 indicate overbought, below 30 indicate oversold.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - RSI values (0-100)

**Algorithm**:
```
gains = max(close[i] - close[i-1], 0)
losses = max(close[i-1] - close[i], 0)
avg_gain = RMA(gains, period)
avg_loss = RMA(losses, period)
RS = avg_gain / avg_loss
RSI = 100 - (100 / (1 + RS))
```

**Complexity**: O(n)

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5, 46.0, 45.8, 46.5]
rsi = haze.py_rsi(close, period=14)
```

**Interpretation**:
- RSI > 70: Overbought (potential sell signal)
- RSI < 30: Oversold (potential buy signal)
- Divergences: Price makes new high/low but RSI does not

**Related**: [py_stochrsi](#py_stochrsiclose-rsi_period14-stoch_period14-k_period3-d_period3)

---

### `py_macd(close, fast_period=12, slow_period=26, signal_period=9)`

**Category**: Momentum

**Description**: Moving Average Convergence Divergence - trend-following momentum indicator showing relationship between two EMAs.

**Parameters**:
- `close` (List[float]): Close prices
- `fast_period` (int, optional): Fast EMA period (default: 12)
- `slow_period` (int, optional): Slow EMA period (default: 26)
- `signal_period` (int, optional): Signal line period (default: 9)

**Returns**: Tuple[List[float], List[float], List[float]] - (MACD line, Signal line, Histogram)

**Algorithm**:
```
MACD = EMA(fast_period) - EMA(slow_period)
Signal = EMA(MACD, signal_period)
Histogram = MACD - Signal
```

**Complexity**: O(n)

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5, 46.0, 45.8, 46.5]
macd, signal, histogram = haze.py_macd(close, fast_period=12, slow_period=26, signal_period=9)
```

**Interpretation**:
- MACD crosses above Signal: Bullish
- MACD crosses below Signal: Bearish
- Histogram expanding: Trend strengthening
- Divergences: Key reversal signals

---

### `py_stochastic(high, low, close, k_period=14, d_period=3)`

**Category**: Momentum

**Description**: Stochastic Oscillator - compares closing price to price range over a period.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `k_period` (int, optional): %K period (default: 14)
- `d_period` (int, optional): %D smoothing period (default: 3)

**Returns**: Tuple[List[float], List[float]] - (%K, %D)

**Algorithm**:
```
%K = (Close - Lowest Low) / (Highest High - Lowest Low) * 100
%D = SMA(%K, d_period)
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
k, d = haze.py_stochastic(high, low, close, k_period=14, d_period=3)
```

**Interpretation**:
- Above 80: Overbought
- Below 20: Oversold
- %K crosses %D: Signal line crossover

---

### `py_stochrsi(close, rsi_period=14, stoch_period=14, k_period=3, d_period=3)`

**Category**: Momentum

**Description**: Stochastic RSI - applies Stochastic formula to RSI values for increased sensitivity.

**Parameters**:
- `close` (List[float]): Close prices
- `rsi_period` (int, optional): RSI period (default: 14)
- `stoch_period` (int, optional): Stochastic period (default: 14)
- `k_period` (int, optional): %K smoothing (default: 3)
- `d_period` (int, optional): %D smoothing (default: 3)

**Returns**: Tuple[List[float], List[float]] - (%K, %D)

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5, 46.0]
k, d = haze.py_stochrsi(close, rsi_period=14, stoch_period=14, k_period=3, d_period=3)
```

---

### `py_cci(high, low, close, period=20)`

**Category**: Momentum

**Description**: Commodity Channel Index - measures price deviation from statistical mean.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 20)

**Returns**: List[float] - CCI values

**Algorithm**:
```
TP = (High + Low + Close) / 3
CCI = (TP - SMA(TP)) / (0.015 * Mean Deviation)
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
cci = haze.py_cci(high, low, close, period=20)
```

**Interpretation**:
- CCI > +100: Strong uptrend
- CCI < -100: Strong downtrend

---

### `py_williams_r(high, low, close, period=14)`

**Category**: Momentum

**Description**: Williams %R - momentum indicator measuring overbought/oversold levels.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - Williams %R values (-100 to 0)

**Algorithm**:
```
%R = (Highest High - Close) / (Highest High - Lowest Low) * -100
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
willr = haze.py_williams_r(high, low, close, period=14)
```

**Interpretation**:
- Above -20: Overbought
- Below -80: Oversold

---

### `py_awesome_oscillator(high, low, fast_period=5, slow_period=34)`

**Category**: Momentum

**Description**: Awesome Oscillator (Bill Williams) - measures market momentum using median price SMAs.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `fast_period` (int): Fast SMA period (default: 5)
- `slow_period` (int): Slow SMA period (default: 34)

**Returns**: List[float] - AO values

**Algorithm**:
```
Median Price = (High + Low) / 2
AO = SMA(Median Price, fast) - SMA(Median Price, slow)
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
ao = haze.py_awesome_oscillator(high, low, fast_period=5, slow_period=34)
```

---

### `py_fisher_transform(high, low, close, period=9)`

**Category**: Momentum

**Description**: Fisher Transform - converts prices to Gaussian normal distribution for clearer turning points.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 9)

**Returns**: Tuple[List[float], List[float]] - (Fisher, Signal)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
fisher, signal = haze.py_fisher_transform(high, low, close, period=9)
```

---

### `py_kdj(high, low, close, k_period=9, d_period=3)`

**Category**: Momentum

**Description**: KDJ Indicator - Chinese variant of Stochastic with J line for increased sensitivity.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `k_period` (int, optional): K period (default: 9)
- `d_period` (int, optional): D period (default: 3)

**Returns**: Tuple[List[float], List[float], List[float]] - (K, D, J)

**Algorithm**:
```
RSV = (Close - Lowest Low) / (Highest High - Lowest Low) * 100
K = SMA(RSV, d_period)
D = SMA(K, d_period)
J = 3*K - 2*D
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
k, d, j = haze.py_kdj(high, low, close, k_period=9, d_period=3)
```

---

### `py_tsi(close, long_period=25, short_period=13, signal_period=13)`

**Category**: Momentum

**Description**: True Strength Index - double-smoothed momentum oscillator.

**Parameters**:
- `close` (List[float]): Close prices
- `long_period` (int, optional): Long smoothing period (default: 25)
- `short_period` (int, optional): Short smoothing period (default: 13)
- `signal_period` (int, optional): Signal line period (default: 13)

**Returns**: Tuple[List[float], List[float]] - (TSI, Signal)

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5, 46.0]
tsi, signal = haze.py_tsi(close, long_period=25, short_period=13, signal_period=13)
```

---

### `py_ultimate_oscillator(high, low, close, period1=7, period2=14, period3=28)`

**Category**: Momentum

**Description**: Ultimate Oscillator - multi-timeframe momentum indicator using three periods.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period1` (int, optional): Short period (default: 7)
- `period2` (int, optional): Medium period (default: 14)
- `period3` (int, optional): Long period (default: 28)

**Returns**: List[float] - UO values (0-100)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
uo = haze.py_ultimate_oscillator(high, low, close, period1=7, period2=14, period3=28)
```

---

### `py_mom(values, period=10)`

**Category**: Momentum

**Description**: Momentum - simple price change over period.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Lookback period (default: 10)

**Returns**: List[float] - Momentum values

**Algorithm**:
```
MOM = Close[i] - Close[i - period]
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
mom = haze.py_mom(close, period=10)
```

---

### `py_roc(values, period=10)`

**Category**: Momentum

**Description**: Rate of Change - percentage price change over period.

**Parameters**:
- `values` (List[float]): Price data
- `period` (int, optional): Lookback period (default: 10)

**Returns**: List[float] - ROC values (percentage)

**Algorithm**:
```
ROC = ((Close[i] - Close[i - period]) / Close[i - period]) * 100
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
roc = haze.py_roc(close, period=10)
```

---

### `py_apo(close, fast_period=12, slow_period=26)`

**Category**: Momentum

**Description**: Absolute Price Oscillator - difference between two EMAs.

**Parameters**:
- `close` (List[float]): Close prices
- `fast_period` (int): Fast EMA period (default: 12)
- `slow_period` (int): Slow EMA period (default: 26)

**Returns**: List[float] - APO values

**Algorithm**:
```
APO = EMA(fast_period) - EMA(slow_period)
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
apo = haze.py_apo(close, fast_period=12, slow_period=26)
```

---

### `py_ppo(close, fast_period=12, slow_period=26)`

**Category**: Momentum

**Description**: Percentage Price Oscillator - percentage difference between two EMAs.

**Parameters**:
- `close` (List[float]): Close prices
- `fast_period` (int): Fast EMA period (default: 12)
- `slow_period` (int): Slow EMA period (default: 26)

**Returns**: List[float] - PPO values (percentage)

**Algorithm**:
```
PPO = ((EMA(fast) - EMA(slow)) / EMA(slow)) * 100
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
ppo = haze.py_ppo(close, fast_period=12, slow_period=26)
```

---

### `py_cmo(close, period=14)`

**Category**: Momentum

**Description**: Chande Momentum Oscillator - measures momentum using gains vs losses ratio.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int): Lookback period (default: 14)

**Returns**: List[float] - CMO values (-100 to +100)

**Algorithm**:
```
CMO = ((Sum of Gains - Sum of Losses) / (Sum of Gains + Sum of Losses)) * 100
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
cmo = haze.py_cmo(close, period=14)
```

---

## Trend Indicators

### `py_supertrend(high, low, close, period=7, multiplier=3.0)`

**Category**: Trend

**Description**: SuperTrend - trend-following indicator using ATR for dynamic support/resistance.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): ATR period (default: 7)
- `multiplier` (float, optional): ATR multiplier (default: 3.0)

**Returns**: Tuple[List[float], List[float], List[float], List[float]] - (SuperTrend, Direction, Upper Band, Lower Band)
- Direction: 1.0 = Uptrend, -1.0 = Downtrend

**Algorithm**:
```
Basic Upper = (High + Low) / 2 + (multiplier * ATR)
Basic Lower = (High + Low) / 2 - (multiplier * ATR)
Final bands adjust based on previous values and trend direction
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
st, direction, upper, lower = haze.py_supertrend(high, low, close, period=7, multiplier=3.0)
```

**Trading Strategy**:
- Direction changes from -1 to 1: Buy signal
- Direction changes from 1 to -1: Sell signal

---

### `py_adx(high, low, close, period=14)`

**Category**: Trend

**Description**: Average Directional Index - measures trend strength regardless of direction.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: Tuple[List[float], List[float], List[float]] - (ADX, +DI, -DI)

**Algorithm**:
```
+DM = High[i] - High[i-1] if positive and > |-DM|
-DM = Low[i-1] - Low[i] if positive and > +DM
+DI = 100 * RMA(+DM) / ATR
-DI = 100 * RMA(-DM) / ATR
DX = |+DI - -DI| / (+DI + -DI) * 100
ADX = RMA(DX, period)
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
adx, plus_di, minus_di = haze.py_adx(high, low, close, period=14)
```

**Interpretation**:
- ADX > 25: Strong trend
- ADX < 20: Weak trend or ranging
- +DI > -DI: Uptrend
- -DI > +DI: Downtrend

---

### `py_aroon(high, low, period=25)`

**Category**: Trend

**Description**: Aroon Indicator - identifies trend direction and strength.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `period` (int, optional): Lookback period (default: 25)

**Returns**: Tuple[List[float], List[float], List[float]] - (Aroon Up, Aroon Down, Aroon Oscillator)

**Algorithm**:
```
Aroon Up = ((period - Days Since Highest High) / period) * 100
Aroon Down = ((period - Days Since Lowest Low) / period) * 100
Aroon Oscillator = Aroon Up - Aroon Down
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
aroon_up, aroon_down, aroon_osc = haze.py_aroon(high, low, period=25)
```

---

### `py_psar(high, low, close, af_init=0.02, af_increment=0.02, af_max=0.2)`

**Category**: Trend

**Description**: Parabolic SAR - trailing stop and reversal indicator.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `af_init` (float, optional): Initial acceleration factor (default: 0.02)
- `af_increment` (float, optional): AF increment (default: 0.02)
- `af_max` (float, optional): Maximum AF (default: 0.2)

**Returns**: Tuple[List[float], List[float]] - (SAR values, Trend direction)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
sar, direction = haze.py_psar(high, low, close, af_init=0.02, af_increment=0.02, af_max=0.2)
```

---

### `py_vortex(high, low, close, period=14)`

**Category**: Trend

**Description**: Vortex Indicator - identifies trend direction and strength using price range.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: Tuple[List[float], List[float]] - (VI+, VI-)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
vi_plus, vi_minus = haze.py_vortex(high, low, close, period=14)
```

**Interpretation**:
- VI+ > VI-: Uptrend
- VI- > VI+: Downtrend
- Crossovers signal trend changes

---

### `py_choppiness(high, low, close, period=14)`

**Category**: Trend

**Description**: Choppiness Index - measures market consolidation vs trending.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - Choppiness values (0-100)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
chop = haze.py_choppiness(high, low, close, period=14)
```

**Interpretation**:
- > 61.8: Choppy/consolidating market
- < 38.2: Trending market

---

### `py_qstick(open, close, period=14)`

**Category**: Trend

**Description**: QStick - measures buying/selling pressure using open-close relationship.

**Parameters**:
- `open` (List[float]): Open prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - QStick values

**Algorithm**:
```
QStick = SMA(Close - Open, period)
```

**Example**:
```python
import haze_library as haze
open_prices = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
qstick = haze.py_qstick(open_prices, close, period=14)
```

---

### `py_vhf(close, period=28)`

**Category**: Trend

**Description**: Vertical Horizontal Filter - determines if market is trending or ranging.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 28)

**Returns**: List[float] - VHF values

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
vhf = haze.py_vhf(close, period=28)
```

---

### `py_trix(close, period=15)`

**Category**: Trend

**Description**: TRIX - triple exponential average rate of change, filters noise.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 15)

**Returns**: List[float] - TRIX values

**Algorithm**:
```
TRIX = ROC(EMA(EMA(EMA(close))), 1)
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
trix = haze.py_trix(close, period=15)
```

---

### `py_dpo(close, period=20)`

**Category**: Trend

**Description**: Detrended Price Oscillator - removes long-term trends to identify cycles.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 20)

**Returns**: List[float] - DPO values

**Algorithm**:
```
DPO = Close[-(period/2 + 1)] - SMA(Close, period)
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
dpo = haze.py_dpo(close, period=20)
```

---

### `py_dx(high, low, close, period=14)`

**Category**: Trend

**Description**: Directional Movement Index - measures strength of directional movement.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - DX values

**Related**: [py_adx](#py_adxhigh-low-close-period14)

---

### `py_plus_di(high, low, close, period=14)`

**Category**: Trend

**Description**: Plus Directional Indicator - measures upward trend strength.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - +DI values

---

### `py_minus_di(high, low, close, period=14)`

**Category**: Trend

**Description**: Minus Directional Indicator - measures downward trend strength.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - -DI values

---

## Volatility Indicators

### `py_atr(high, low, close, period=14)`

**Category**: Volatility

**Description**: Average True Range - measures market volatility.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - ATR values

**Algorithm**:
```
TR = max(High - Low, |High - Close[prev]|, |Low - Close[prev]|)
ATR = RMA(TR, period)
```

**Complexity**: O(n)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
atr = haze.py_atr(high, low, close, period=14)
```

**Use Cases**:
- Position sizing
- Stop-loss calculation
- Volatility filtering

---

### `py_natr(high, low, close, period=14)`

**Category**: Volatility

**Description**: Normalized ATR - ATR as percentage of close price.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - NATR values (percentage)

**Algorithm**:
```
NATR = (ATR / Close) * 100
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
natr = haze.py_natr(high, low, close, period=14)
```

---

### `py_true_range(high, low, close, drift=1)`

**Category**: Volatility

**Description**: True Range - single-period volatility measure.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `drift` (int, optional): Lookback for previous close (default: 1)

**Returns**: List[float] - True Range values

---

### `py_bollinger_bands(close, period=20, std_multiplier=2.0)`

**Category**: Volatility

**Description**: Bollinger Bands - volatility bands around moving average.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): SMA period (default: 20)
- `std_multiplier` (float, optional): Standard deviation multiplier (default: 2.0)

**Returns**: Tuple[List[float], List[float], List[float]] - (Upper, Middle, Lower)

**Algorithm**:
```
Middle = SMA(close, period)
Upper = Middle + (std_multiplier * StdDev)
Lower = Middle - (std_multiplier * StdDev)
```

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5, 46.0]
upper, middle, lower = haze.py_bollinger_bands(close, period=20, std_multiplier=2.0)
```

**Interpretation**:
- Price at upper band: Potentially overbought
- Price at lower band: Potentially oversold
- Band squeeze: Low volatility, potential breakout

---

### `py_keltner_channel(high, low, close, period=20, atr_period=10, multiplier=2.0)`

**Category**: Volatility

**Description**: Keltner Channel - volatility bands using ATR instead of standard deviation.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): EMA period (default: 20)
- `atr_period` (int, optional): ATR period (default: 10)
- `multiplier` (float, optional): ATR multiplier (default: 2.0)

**Returns**: Tuple[List[float], List[float], List[float]] - (Upper, Middle, Lower)

**Algorithm**:
```
Middle = EMA(close, period)
Upper = Middle + (multiplier * ATR)
Lower = Middle - (multiplier * ATR)
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
upper, middle, lower = haze.py_keltner_channel(high, low, close, period=20, atr_period=10, multiplier=2.0)
```

---

### `py_donchian_channel(high, low, period=20)`

**Category**: Volatility

**Description**: Donchian Channel - highest high and lowest low over period.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `period` (int, optional): Lookback period (default: 20)

**Returns**: Tuple[List[float], List[float], List[float]] - (Upper, Middle, Lower)

**Algorithm**:
```
Upper = Highest High over period
Lower = Lowest Low over period
Middle = (Upper + Lower) / 2
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
upper, middle, lower = haze.py_donchian_channel(high, low, period=20)
```

---

### `py_chandelier_exit(high, low, close, period=22, atr_period=22, multiplier=3.0)`

**Category**: Volatility

**Description**: Chandelier Exit - trailing stop based on ATR from highest high/lowest low.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 22)
- `atr_period` (int, optional): ATR period (default: 22)
- `multiplier` (float, optional): ATR multiplier (default: 3.0)

**Returns**: Tuple[List[float], List[float]] - (Long Exit, Short Exit)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
long_exit, short_exit = haze.py_chandelier_exit(high, low, close, period=22, atr_period=22, multiplier=3.0)
```

---

### `py_historical_volatility(close, period=20)`

**Category**: Volatility

**Description**: Historical Volatility - annualized standard deviation of returns.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 20)

**Returns**: List[float] - Historical volatility values

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
hv = haze.py_historical_volatility(close, period=20)
```

---

### `py_ulcer_index(close, period=14)`

**Category**: Volatility

**Description**: Ulcer Index - measures downside volatility/risk.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - Ulcer Index values

**Example**:
```python
import haze_library as haze
close = [44.0, 44.5, 45.0, 44.8, 45.5]
ui = haze.py_ulcer_index(close, period=14)
```

---

### `py_mass_index(high, low, period=25, ema_period=9)`

**Category**: Volatility

**Description**: Mass Index - identifies trend reversals using high-low range expansion.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `period` (int, optional): Summation period (default: 25)
- `ema_period` (int, optional): EMA period (default: 9)

**Returns**: List[float] - Mass Index values

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
mi = haze.py_mass_index(high, low, period=25, ema_period=9)
```

**Interpretation**:
- "Reversal Bulge": MI rises above 27 then falls below 26.5

---

## Volume Indicators

### `py_obv(close, volume)`

**Category**: Volume

**Description**: On-Balance Volume - cumulative volume flow indicator.

**Parameters**:
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data

**Returns**: List[float] - OBV values

**Algorithm**:
```
if Close > Close[prev]: OBV = OBV[prev] + Volume
if Close < Close[prev]: OBV = OBV[prev] - Volume
if Close = Close[prev]: OBV = OBV[prev]
```

**Example**:
```python
import haze_library as haze
close = [45.0, 46.0, 45.5, 46.5, 47.0]
volume = [1000, 1200, 1100, 1300, 1250]
obv = haze.py_obv(close, volume)
```

---

### `py_vwap(high, low, close, volume, period=0)`

**Category**: Volume

**Description**: Volume Weighted Average Price - average price weighted by volume.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data
- `period` (int, optional): Period (0 = cumulative, default: 0)

**Returns**: List[float] - VWAP values

**Algorithm**:
```
Typical Price = (High + Low + Close) / 3
VWAP = Cumulative(TP * Volume) / Cumulative(Volume)
```

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
volume = [1000, 1200, 1100, 1300, 1250]
vwap = haze.py_vwap(high, low, close, volume, period=0)
```

---

### `py_mfi(high, low, close, volume, period=14)`

**Category**: Volume

**Description**: Money Flow Index - volume-weighted RSI.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data
- `period` (int, optional): Lookback period (default: 14)

**Returns**: List[float] - MFI values (0-100)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
volume = [1000, 1200, 1100, 1300, 1250]
mfi = haze.py_mfi(high, low, close, volume, period=14)
```

**Interpretation**:
- MFI > 80: Overbought
- MFI < 20: Oversold

---

### `py_cmf(high, low, close, volume, period=20)`

**Category**: Volume

**Description**: Chaikin Money Flow - measures buying/selling pressure.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data
- `period` (int, optional): Lookback period (default: 20)

**Returns**: List[float] - CMF values (-1 to +1)

**Example**:
```python
import haze_library as haze
high = [46.0, 47.0, 46.5, 47.5, 48.0]
low = [44.0, 45.0, 44.5, 45.5, 46.0]
close = [45.0, 46.0, 45.5, 46.5, 47.0]
volume = [1000, 1200, 1100, 1300, 1250]
cmf = haze.py_cmf(high, low, close, volume, period=20)
```

---

### `py_volume_profile(high, low, close, volume, num_bins=24)`

**Category**: Volume

**Description**: Volume Profile - volume distribution at price levels.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data
- `num_bins` (int, optional): Number of price bins (default: 24)

**Returns**: Tuple[List[float], List[float], float] - (Price levels, Volume at each level, POC)

---

### `py_ad(high, low, close, volume)`

**Category**: Volume

**Description**: Accumulation/Distribution Line - measures cumulative money flow.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data

**Returns**: List[float] - A/D Line values

**Algorithm**:
```
CLV = ((Close - Low) - (High - Close)) / (High - Low)
AD = AD[prev] + CLV * Volume
```

---

### `py_adosc(high, low, close, volume, fast_period=3, slow_period=10)`

**Category**: Volume

**Description**: Chaikin A/D Oscillator - EMA difference of A/D Line.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data
- `fast_period` (int): Fast EMA period (default: 3)
- `slow_period` (int): Slow EMA period (default: 10)

**Returns**: List[float] - ADOSC values

---

### `py_pvt(close, volume)`

**Category**: Volume

**Description**: Price Volume Trend - cumulative volume adjusted by price change.

**Parameters**:
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data

**Returns**: List[float] - PVT values

---

### `py_nvi(close, volume)`

**Category**: Volume

**Description**: Negative Volume Index - tracks price changes on down-volume days.

**Parameters**:
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data

**Returns**: List[float] - NVI values

---

### `py_pvi(close, volume)`

**Category**: Volume

**Description**: Positive Volume Index - tracks price changes on up-volume days.

**Parameters**:
- `close` (List[float]): Close prices
- `volume` (List[float]): Volume data

**Returns**: List[float] - PVI values

---

### `py_eom(high, low, volume, period=14)`

**Category**: Volume

**Description**: Ease of Movement - measures relationship between volume and price change.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `volume` (List[float]): Volume data
- `period` (int, optional): Smoothing period (default: 14)

**Returns**: List[float] - EOM values

---

### `py_volume_oscillator(volume, short_period=5, long_period=10)`

**Category**: Volume

**Description**: Volume Oscillator - difference between volume EMAs.

**Parameters**:
- `volume` (List[float]): Volume data
- `short_period` (int, optional): Short EMA period (default: 5)
- `long_period` (int, optional): Long EMA period (default: 10)

**Returns**: List[float] - Volume Oscillator values

---

## Candlestick Patterns

All candlestick pattern functions return a signal vector:
- `1.0`: Bullish pattern detected
- `-1.0`: Bearish pattern detected
- `0.0`: No pattern

### Single Candle Patterns

#### `py_doji(open, high, low, close, body_threshold=0.1)`

**Description**: Doji - indecision pattern with very small body.

**Parameters**:
- `open`, `high`, `low`, `close` (List[float]): OHLC data
- `body_threshold` (float, optional): Maximum body/range ratio (default: 0.1)

**Returns**: List[float] - Signal (1.0 = Doji detected)

---

#### `py_hammer(open, high, low, close)`

**Description**: Hammer - bullish reversal with long lower shadow.

**Returns**: List[float] - Signal (1.0 = Bullish Hammer)

---

#### `py_inverted_hammer(open, high, low, close)`

**Description**: Inverted Hammer - bullish reversal with long upper shadow.

**Returns**: List[float] - Signal (1.0 = Inverted Hammer)

---

#### `py_hanging_man(open, high, low, close)`

**Description**: Hanging Man - bearish reversal similar to hammer at top.

**Returns**: List[float] - Signal (-1.0 = Hanging Man)

---

#### `py_shooting_star(open, high, low, close)`

**Description**: Shooting Star - bearish reversal with long upper shadow.

**Returns**: List[float] - Signal (-1.0 = Shooting Star)

---

#### `py_marubozu(open, high, low, close)`

**Description**: Marubozu - strong candle with no shadows.

**Returns**: List[float] - Signal (1.0 = Bullish, -1.0 = Bearish)

---

#### `py_spinning_top(open, high, low, close)`

**Description**: Spinning Top - indecision with small body and equal shadows.

**Returns**: List[float] - Signal (1.0 = Spinning Top)

---

#### `py_dragonfly_doji(open, high, low, close, body_threshold=0.1)`

**Description**: Dragonfly Doji - bullish doji with long lower shadow.

**Returns**: List[float] - Signal (1.0 = Dragonfly Doji)

---

#### `py_gravestone_doji(open, high, low, close, body_threshold=0.1)`

**Description**: Gravestone Doji - bearish doji with long upper shadow.

**Returns**: List[float] - Signal (-1.0 = Gravestone Doji)

---

#### `py_long_legged_doji(open, high, low, close, body_threshold=0.1)`

**Description**: Long-Legged Doji - doji with long shadows both sides.

**Returns**: List[float] - Signal (1.0 = Long-Legged Doji)

---

### Two Candle Patterns

#### `py_bullish_engulfing(open, close)`

**Description**: Bullish Engulfing - large bullish candle engulfs previous bearish.

**Returns**: List[float] - Signal (1.0 = Bullish Engulfing)

---

#### `py_bearish_engulfing(open, close)`

**Description**: Bearish Engulfing - large bearish candle engulfs previous bullish.

**Returns**: List[float] - Signal (-1.0 = Bearish Engulfing)

---

#### `py_bullish_harami(open, close)`

**Description**: Bullish Harami - small bullish candle within previous bearish body.

**Returns**: List[float] - Signal (1.0 = Bullish Harami)

---

#### `py_bearish_harami(open, close)`

**Description**: Bearish Harami - small bearish candle within previous bullish body.

**Returns**: List[float] - Signal (-1.0 = Bearish Harami)

---

#### `py_piercing_pattern(open, low, close)`

**Description**: Piercing Pattern - bullish reversal closing above midpoint of previous.

**Returns**: List[float] - Signal (1.0 = Piercing Pattern)

---

#### `py_dark_cloud_cover(open, high, close)`

**Description**: Dark Cloud Cover - bearish reversal closing below midpoint of previous.

**Returns**: List[float] - Signal (-1.0 = Dark Cloud Cover)

---

#### `py_tweezers_top(open, high, close, tolerance=0.01)`

**Description**: Tweezers Top - bearish reversal with matching highs.

**Returns**: List[float] - Signal (-1.0 = Tweezers Top)

---

#### `py_tweezers_bottom(open, low, close, tolerance=0.01)`

**Description**: Tweezers Bottom - bullish reversal with matching lows.

**Returns**: List[float] - Signal (1.0 = Tweezers Bottom)

---

### Three Candle Patterns

#### `py_morning_star(open, high, low, close)`

**Description**: Morning Star - three-candle bullish reversal pattern.

**Returns**: List[float] - Signal (1.0 = Morning Star)

---

#### `py_evening_star(open, high, low, close)`

**Description**: Evening Star - three-candle bearish reversal pattern.

**Returns**: List[float] - Signal (-1.0 = Evening Star)

---

#### `py_three_white_soldiers(open, high, close)`

**Description**: Three White Soldiers - three consecutive bullish candles.

**Returns**: List[float] - Signal (1.0 = Three White Soldiers)

---

#### `py_three_black_crows(open, low, close)`

**Description**: Three Black Crows - three consecutive bearish candles.

**Returns**: List[float] - Signal (-1.0 = Three Black Crows)

---

### Additional Candlestick Patterns (47 more)

The library includes 61 total candlestick patterns, matching TA-Lib's complete set:

- `py_harami_cross` - Harami Cross
- `py_morning_doji_star` - Morning Doji Star
- `py_evening_doji_star` - Evening Doji Star
- `py_three_inside` - Three Inside Up/Down
- `py_three_outside` - Three Outside Up/Down
- `py_abandoned_baby` - Abandoned Baby
- `py_kicking` - Kicking Pattern
- `py_long_line` - Long Line Candle
- `py_short_line` - Short Line Candle
- `py_doji_star` - Doji Star
- `py_identical_three_crows` - Identical Three Crows
- `py_stick_sandwich` - Stick Sandwich
- `py_tristar` - Tristar Pattern
- `py_upside_gap_two_crows` - Upside Gap Two Crows
- `py_gap_sidesidewhite` - Side-by-Side White Lines
- `py_takuri` - Takuri Line
- `py_homing_pigeon` - Homing Pigeon
- `py_matching_low` - Matching Low
- `py_separating_lines` - Separating Lines
- `py_thrusting` - Thrusting Pattern
- `py_inneck` - In-Neck Pattern
- `py_onneck` - On-Neck Pattern
- `py_advance_block` - Advance Block
- `py_stalled_pattern` - Stalled Pattern
- `py_belthold` - Belt Hold
- `py_concealing_baby_swallow` - Concealing Baby Swallow
- `py_counterattack` - Counterattack
- `py_highwave` - High Wave Candle
- `py_hikkake` - Hikkake Pattern
- `py_hikkake_mod` - Modified Hikkake
- `py_ladder_bottom` - Ladder Bottom
- `py_mat_hold` - Mat Hold
- `py_rickshaw_man` - Rickshaw Man
- `py_unique_3_river` - Unique 3 River
- `py_xside_gap_3_methods` - Upside/Downside Gap Three Methods
- `py_closing_marubozu` - Closing Marubozu
- `py_breakaway` - Breakaway
- `py_rising_three_methods` - Rising Three Methods
- `py_falling_three_methods` - Falling Three Methods

---

## Statistical Functions

### `py_linear_regression(y_values, period)`

**Category**: Statistical

**Description**: Linear Regression - calculates slope, intercept, and predicted values.

**Parameters**:
- `y_values` (List[float]): Data series
- `period` (int): Lookback period

**Returns**: Tuple[List[float], List[float], List[float]] - (Slope, Intercept, Predicted Values)

---

### `py_correlation(x, y, period)`

**Category**: Statistical

**Description**: Pearson Correlation - measures linear relationship between two series.

**Parameters**:
- `x` (List[float]): First data series
- `y` (List[float]): Second data series
- `period` (int): Lookback period

**Returns**: List[float] - Correlation values (-1 to +1)

---

### `py_zscore(values, period)`

**Category**: Statistical

**Description**: Z-Score - number of standard deviations from mean.

**Parameters**:
- `values` (List[float]): Data series
- `period` (int): Lookback period

**Returns**: List[float] - Z-Score values

---

### `py_covariance(x, y, period)`

**Category**: Statistical

**Description**: Covariance - measures how two variables move together.

**Parameters**:
- `x` (List[float]): First data series
- `y` (List[float]): Second data series
- `period` (int): Lookback period

**Returns**: List[float] - Covariance values

---

### `py_beta(asset_returns, benchmark_returns, period)`

**Category**: Statistical

**Description**: Beta - measures asset volatility relative to benchmark.

**Parameters**:
- `asset_returns` (List[float]): Asset returns
- `benchmark_returns` (List[float]): Benchmark returns
- `period` (int): Lookback period

**Returns**: List[float] - Beta values

---

### `py_standard_error(y_values, period)`

**Category**: Statistical

**Description**: Standard Error - standard deviation of regression residuals.

**Parameters**:
- `y_values` (List[float]): Data series
- `period` (int): Lookback period

**Returns**: List[float] - Standard Error values

---

### `py_correl(x, y, period)`

**Category**: Statistical (TA-Lib compatible)

**Description**: Pearson Correlation Coefficient.

---

### `py_linearreg(values, period)`

**Category**: Statistical

**Description**: Linear Regression - predicted value at end of regression line.

---

### `py_linearreg_slope(values, period)`

**Category**: Statistical

**Description**: Linear Regression Slope.

---

### `py_linearreg_angle(values, period)`

**Category**: Statistical

**Description**: Linear Regression Angle (in degrees).

---

### `py_linearreg_intercept(values, period)`

**Category**: Statistical

**Description**: Linear Regression Intercept.

---

### `py_var(values, period)`

**Category**: Statistical

**Description**: Variance over period.

---

### `py_tsf(values, period)`

**Category**: Statistical

**Description**: Time Series Forecast - linear regression projected one period forward.

---

## Price Transform

### `py_avgprice(open, high, low, close)`

**Description**: Average Price = (Open + High + Low + Close) / 4

**Returns**: List[float] - Average prices

---

### `py_medprice(high, low)`

**Description**: Median Price = (High + Low) / 2

**Returns**: List[float] - Median prices

---

### `py_typprice(high, low, close)`

**Description**: Typical Price = (High + Low + Close) / 3

**Returns**: List[float] - Typical prices

---

### `py_wclprice(high, low, close)`

**Description**: Weighted Close Price = (High + Low + 2*Close) / 4

**Returns**: List[float] - Weighted close prices

---

## Math Operations

### Rolling Functions

- `py_max(values, period)` - Rolling maximum
- `py_min(values, period)` - Rolling minimum
- `py_sum(values, period)` - Rolling sum
- `py_minmax(values, period)` - Returns (min, max) tuple
- `py_minmaxindex(values, period)` - Returns (min_idx, max_idx) tuple

### Element-wise Functions

- `py_sqrt(values)` - Square root
- `py_ln(values)` - Natural logarithm
- `py_log10(values)` - Base-10 logarithm
- `py_exp(values)` - Exponential
- `py_abs(values)` - Absolute value
- `py_ceil(values)` - Ceiling
- `py_floor(values)` - Floor

### Trigonometric Functions

- `py_sin(values)` - Sine
- `py_cos(values)` - Cosine
- `py_tan(values)` - Tangent
- `py_asin(values)` - Arcsine
- `py_acos(values)` - Arccosine
- `py_atan(values)` - Arctangent
- `py_sinh(values)` - Hyperbolic sine
- `py_cosh(values)` - Hyperbolic cosine
- `py_tanh(values)` - Hyperbolic tangent

### Vector Operations

- `py_add(values1, values2)` - Element-wise addition
- `py_sub(values1, values2)` - Element-wise subtraction
- `py_mult(values1, values2)` - Element-wise multiplication
- `py_div(values1, values2)` - Element-wise division

---

## Overlap Studies

### `py_midpoint(values, period)`

**Description**: Midpoint of values over period.

**Returns**: List[float] - (Highest + Lowest) / 2

---

### `py_midprice(high, low, period)`

**Description**: Midpoint Price = (Highest High + Lowest Low) / 2

**Returns**: List[float] - Midprice values

---

### `py_trima(values, period)`

**Description**: Triangular Moving Average - double-smoothed SMA.

**Returns**: List[float] - TRIMA values

---

### `py_sar(high, low, close, af_init=0.02, af_increment=0.02, af_max=0.2)`

**Description**: Parabolic SAR (alias for py_psar).

---

### `py_sarext(high, low, ...extended_parameters...)`

**Description**: Parabolic SAR Extended with additional parameters.

---

### `py_mama(values, fast_limit=0.5, slow_limit=0.05)`

**Description**: MESA Adaptive Moving Average.

**Returns**: Tuple[List[float], List[float]] - (MAMA, FAMA)

---

## Cycle Indicators

### `py_ht_dcperiod(values)`

**Description**: Hilbert Transform - Dominant Cycle Period.

**Returns**: List[float] - Dominant cycle period values

---

### `py_ht_dcphase(values)`

**Description**: Hilbert Transform - Dominant Cycle Phase.

**Returns**: List[float] - Phase values

---

### `py_ht_phasor(values)`

**Description**: Hilbert Transform - Phasor Components.

**Returns**: Tuple[List[float], List[float]] - (In-Phase, Quadrature)

---

### `py_ht_sine(values)`

**Description**: Hilbert Transform - Sine Wave.

**Returns**: Tuple[List[float], List[float]] - (Sine, Lead Sine)

---

### `py_ht_trendmode(values)`

**Description**: Hilbert Transform - Trend vs Cycle Mode.

**Returns**: List[float] - Mode indicator (1=Trend, 0=Cycle)

---

## Fibonacci & Pivot Points

### `py_fib_retracement(start_price, end_price)`

**Description**: Calculate Fibonacci retracement levels.

**Parameters**:
- `start_price` (float): Starting price (trend start)
- `end_price` (float): Ending price (trend end)

**Returns**: List[Tuple[str, float]] - [(ratio, price_level), ...]

**Standard Levels**: 0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0

**Example**:
```python
import haze_library as haze
levels = haze.py_fib_retracement(100.0, 150.0)
# Returns: [('0.000', 150.0), ('0.236', 138.2), ('0.382', 130.9), ...]
```

---

### `py_fib_extension(start_price, end_price, retracement_price)`

**Description**: Calculate Fibonacci extension levels.

**Parameters**:
- `start_price` (float): A point (trend start)
- `end_price` (float): B point (trend end)
- `retracement_price` (float): C point (retracement level)

**Returns**: List[Tuple[str, float]] - [(ratio, price_level), ...]

**Standard Levels**: 1.272, 1.414, 1.618, 2.0, 2.618, 3.618

---

### `py_ichimoku_cloud(high, low, close, tenkan_period=9, kijun_period=26, senkou_b_period=52)`

**Description**: Ichimoku Cloud - comprehensive trend/support/resistance system.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices
- `tenkan_period` (int, optional): Conversion line period (default: 9)
- `kijun_period` (int, optional): Base line period (default: 26)
- `senkou_b_period` (int, optional): Leading span B period (default: 52)

**Returns**: Tuple[List[float], ...5] - (Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, Chikou Span)

**Example**:
```python
import haze_library as haze
tenkan, kijun, span_a, span_b, chikou = haze.py_ichimoku_cloud(high, low, close)
```

---

### `py_standard_pivots(high, low, close)`

**Description**: Classic Pivot Points calculation.

**Parameters**: Single period's high, low, close (floats)

**Returns**: Tuple[float, ...7] - (PP, R1, R2, R3, S1, S2, S3)

---

### `py_fibonacci_pivots(high, low, close)`

**Description**: Fibonacci-based Pivot Points.

**Returns**: Tuple[float, ...7] - (PP, R1, R2, R3, S1, S2, S3)

---

### `py_camarilla_pivots(high, low, close)`

**Description**: Camarilla Pivot Points (short-term trading).

**Returns**: Tuple[float, ...9] - (PP, R1, R2, R3, R4, S1, S2, S3, S4)

---

## pandas-ta Exclusive Indicators

### `py_entropy(close, period=10, bins=10)`

**Category**: pandas-ta Exclusive

**Description**: Shannon Entropy - measures price uncertainty/randomness.

**Parameters**:
- `close` (List[float]): Close prices
- `period` (int, optional): Lookback period (default: 10)
- `bins` (int, optional): Number of histogram bins (default: 10)

**Returns**: List[float] - Entropy values (higher = more uncertain)

---

### `py_aberration(high, low, close, period=20, atr_period=20)`

**Category**: pandas-ta Exclusive

**Description**: Keltner Channel variant measuring price deviation from mean.

**Returns**: List[float] - Aberration values

---

### `py_squeeze(high, low, close, bb_period=20, bb_std=2.0, kc_period=20, kc_atr_period=20, kc_mult=1.5)`

**Category**: pandas-ta Exclusive

**Description**: TTM Squeeze - volatility compression indicator.

**Returns**: Tuple[List[float], List[float], List[float]] - (Squeeze On, Squeeze Off, Momentum)

**Interpretation**:
- Squeeze On (1.0): Low volatility, potential breakout coming
- Squeeze Off (1.0): Breakout in progress

---

### `py_qqe(close, rsi_period=14, smooth=5, multiplier=4.236)`

**Category**: pandas-ta Exclusive

**Description**: Quantitative Qualitative Estimation - smoothed RSI with dynamic thresholds.

**Returns**: Tuple[List[float], List[float], List[float]] - (Fast Line, Slow Line, Signal)

---

### `py_cti(close, period=12)`

**Category**: pandas-ta Exclusive

**Description**: Correlation Trend Indicator - measures trend linearity.

**Returns**: List[float] - CTI values (-1 to +1)

---

### `py_er(close, period=10)`

**Category**: pandas-ta Exclusive

**Description**: Efficiency Ratio (Kaufman) - measures price movement efficiency.

**Returns**: List[float] - ER values (0 to 1)

---

### `py_bias(close, period=20)`

**Category**: pandas-ta Exclusive

**Description**: Bias - percentage deviation from moving average.

**Returns**: List[float] - Bias percentage

---

### `py_psl(close, period=12)`

**Category**: pandas-ta Exclusive

**Description**: Psychological Line - percentage of up days.

**Returns**: List[float] - PSL values (0-100)

**Interpretation**:
- > 75: Overbought
- < 25: Oversold

---

### `py_rvi(open, high, low, close, period=10, signal_period=4)`

**Category**: pandas-ta Exclusive

**Description**: Relative Vigor Index - momentum using open-close vs high-low.

**Returns**: Tuple[List[float], List[float]] - (RVI, Signal)

---

### `py_inertia(open, high, low, close, rvi_period=14, regression_period=20)`

**Category**: pandas-ta Exclusive

**Description**: Inertia - RVI variant with linear regression smoothing.

**Returns**: List[float] - Inertia values

---

### `py_alligator(high, low, jaw_period=13, teeth_period=8, lips_period=5)`

**Category**: pandas-ta Exclusive

**Description**: Bill Williams Alligator - three SMAs with forward offset.

**Returns**: Tuple[List[float], List[float], List[float]] - (Jaw, Teeth, Lips)

---

### `py_efi(close, volume, period=13)`

**Category**: pandas-ta Exclusive

**Description**: Elder's Force Index - measures buying/selling pressure.

**Returns**: List[float] - EFI values

---

### `py_kst(close, roc1=10, roc2=15, roc3=20, roc4=30, signal_period=9)`

**Category**: pandas-ta Exclusive

**Description**: Know Sure Thing - weighted ROC sum.

**Returns**: Tuple[List[float], List[float]] - (KST, Signal)

---

### `py_stc(close, fast=23, slow=50, cycle=10)`

**Category**: pandas-ta Exclusive

**Description**: Schaff Trend Cycle - double-stochasticized MACD.

**Returns**: List[float] - STC values (0-100)

---

### `py_tdfi(close, period=13, smooth=3)`

**Category**: pandas-ta Exclusive

**Description**: Trend Direction Force Index.

**Returns**: List[float] - TDFI values

---

### `py_wae(close, fast=20, slow=40, signal=9, bb_period=20, multiplier=2.0)`

**Category**: pandas-ta Exclusive

**Description**: Waddah Attar Explosion - volatility breakout indicator.

**Returns**: Tuple[List[float], List[float]] - (Explosion, Dead Zone)

---

### `py_smi(high, low, close, period=13, smooth1=25, smooth2=2)`

**Category**: pandas-ta Exclusive

**Description**: Stochastic Momentum Index.

**Returns**: List[float] - SMI values

---

### `py_coppock(close, period1=11, period2=14, wma_period=10)`

**Category**: pandas-ta Exclusive

**Description**: Coppock Curve - long-term momentum indicator.

**Returns**: List[float] - Coppock values

---

### `py_pgo(high, low, close, period=14)`

**Category**: pandas-ta Exclusive

**Description**: Pretty Good Oscillator.

**Returns**: List[float] - PGO values

---

### `py_vwma(close, volume, period=20)`

**Category**: pandas-ta Exclusive

**Description**: Volume Weighted Moving Average.

**Returns**: List[float] - VWMA values

---

### `py_bop(open, high, low, close)`

**Category**: pandas-ta Exclusive

**Description**: Balance of Power - measures buying vs selling pressure.

**Returns**: List[float] - BOP values (-1 to +1)

---

### `py_ssl_channel(high, low, close, period=10)`

**Category**: pandas-ta Exclusive

**Description**: SSL Channel - trend direction indicator.

**Returns**: Tuple[List[float], List[float]] - (SSL Up, SSL Down)

---

### `py_cfo(close, period=14)`

**Category**: pandas-ta Exclusive

**Description**: Chande Forecast Oscillator.

**Returns**: List[float] - CFO percentage

---

### `py_slope(values, period=14)`

**Category**: pandas-ta Exclusive

**Description**: Linear Regression Slope.

**Returns**: List[float] - Slope values

---

### `py_percent_rank(values, period=14)`

**Category**: pandas-ta Exclusive

**Description**: Percentile Rank - percentage of values below current.

**Returns**: List[float] - Percentile (0-100)

---

## ML-Enhanced Signals

### `py_ai_supertrend(high, low, close, period=10, multiplier=3.0)`

**Category**: ML-Enhanced

**Description**: AI-enhanced SuperTrend using machine learning for adaptive parameters.

**Returns**: Tuple[List[float], List[float]] - (SuperTrend, Direction)

---

### `py_ai_supertrend_ml(high, low, close, period=10, multiplier=3.0)`

**Category**: ML-Enhanced

**Description**: SuperTrend with SVR-based machine learning enhancement.

**Returns**: Tuple[List[float], List[float]] - (SuperTrend, Direction)

---

### `py_ai_momentum_index(high, low, close, period=14)`

**Category**: ML-Enhanced

**Description**: ML-enhanced momentum index.

**Returns**: List[float] - AI Momentum values

---

### `py_ai_momentum_index_ml(high, low, close, period=14)`

**Category**: ML-Enhanced

**Description**: Momentum index with linfa ML backend.

---

### `py_dynamic_macd(close, fast=12, slow=26, signal=9)`

**Category**: ML-Enhanced

**Description**: MACD with dynamic period adjustment.

---

### `py_atr2_signals(high, low, close, period=14, multiplier=2.0)`

**Category**: ML-Enhanced

**Description**: ATR-based trading signals.

---

### `py_atr2_signals_ml(high, low, close, period=14, multiplier=2.0)`

**Category**: ML-Enhanced

**Description**: ML-enhanced ATR signals.

---

### `py_pivot_buy_sell(high, low, close, left_bars=5, right_bars=5)`

**Category**: ML-Enhanced

**Description**: Pivot-based buy/sell signals with ML enhancement.

---

## Harmonic Patterns

### `py_harmonics(high, low, close)`

**Category**: Harmonic Patterns

**Description**: Detects XABCD harmonic patterns and returns signals.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `close` (List[float]): Close prices

**Returns**: Tuple[List[float], List[float], List[float], List[float]] - (Signals, PRZ Upper, PRZ Lower, Probability)
- Signals: 1.0 = Bullish pattern, -1.0 = Bearish pattern

**Pattern Types Detected**:
- Gartley (222 Pattern)
- Butterfly
- Bat
- Crab
- Deep Crab
- Shark
- Cypher
- ABCD
- Three Drives

---

### `py_harmonics_patterns(high, low, left_bars=5, right_bars=5, include_forming=True)`

**Category**: Harmonic Patterns

**Description**: Returns detailed harmonic pattern information.

**Parameters**:
- `high` (List[float]): High prices
- `low` (List[float]): Low prices
- `left_bars` (int, optional): Left swing detection bars (default: 5)
- `right_bars` (int, optional): Right swing detection bars (default: 5)
- `include_forming` (bool, optional): Include incomplete patterns (default: True)

**Returns**: List[HarmonicPattern] - Pattern objects with:
- `pattern_type`: Pattern name (e.g., "Gartley")
- `pattern_type_zh`: Chinese name
- `state`: "forming" or "completed"
- `prz_center`: Potential Reversal Zone center
- `prz_upper`: PRZ upper bound
- `prz_lower`: PRZ lower bound
- `completion_probability`: Pattern completion likelihood

---

### `py_swing_points(high, low, left_bars=5, right_bars=5)`

**Category**: Harmonic Patterns

**Description**: Detects swing high and swing low points.

**Returns**: Tuple[List[float], List[float]] - (Swing Highs, Swing Lows)

---

## Market Structure

### `py_detect_divergence(price, indicator, period=14)`

**Category**: Market Structure

**Description**: Detects bullish/bearish divergence between price and indicator.

**Returns**: List[float] - Divergence signals (1=Bullish, -1=Bearish)

---

### `py_fvg_signals(high, low, close)`

**Category**: Market Structure

**Description**: Fair Value Gap detection.

**Returns**: List[float] - FVG signals

---

### `py_volume_filter(close, volume, threshold=1.5)`

**Category**: Market Structure

**Description**: Filters signals based on volume threshold.

---

### `py_combine_signals(signals1, signals2, mode="and")`

**Category**: Signal Utility

**Description**: Combines multiple signal arrays.

**Parameters**:
- `mode`: "and", "or", or "majority"

---

### `py_calculate_stops(high, low, close, atr_multiplier=2.0)`

**Category**: Signal Utility

**Description**: Calculates stop-loss and take-profit levels.

---

### `py_pd_array_signals(high, low, close)`

**Category**: Market Structure

**Description**: Premium/Discount Array signals.

---

### `py_breaker_block_signals(high, low, close)`

**Category**: Market Structure

**Description**: Breaker Block detection.

---

### `py_general_parameters_signals(high, low, close)`

**Category**: Market Structure

**Description**: General market structure parameters.

---

### `py_linreg_supply_demand_signals(high, low, close)`

**Category**: Market Structure

**Description**: Linear regression-based supply/demand zones.

---

## Performance Notes

### Computational Complexity

| Indicator Type | Complexity | Notes |
|----------------|------------|-------|
| Simple MA | O(n) | Incremental calculation |
| EMA/RMA | O(n) | Single pass |
| Bollinger Bands | O(n) | Uses rolling statistics |
| RSI | O(n) | Single pass with RMA |
| MACD | O(n) | Three EMA calculations |
| Stochastic | O(n * period) | Rolling min/max |
| ADX | O(n) | Multiple smoothing steps |
| Candlestick Patterns | O(n) | Pattern-dependent lookback |
| Harmonic Patterns | O(n^2) | Swing point detection |

### Memory Usage

- All indicators return vectors with same length as input
- Early values are typically NaN (Not a Number) during warmup period
- Warmup period = indicator's period parameter

### Best Practices

1. **Pre-allocate data**: Convert pandas/numpy to list before calling
2. **Batch processing**: Calculate multiple indicators in parallel
3. **Minimize copies**: Use the returned list directly when possible

---

## Error Handling

All functions may raise:
- `ValueError`: Invalid period (e.g., period > data length)
- `TypeError`: Wrong input type

Example error handling:
```python
import haze_library as haze

try:
    rsi = haze.py_rsi(close_prices, period=14)
except ValueError as e:
    print(f"Invalid parameters: {e}")
except Exception as e:
    print(f"Calculation error: {e}")
```

---

## Version History

- **v1.0**: Initial release with 215 indicators
- Full TA-Lib compatibility
- pandas-ta exclusive indicators
- ML-enhanced signals
- Harmonic pattern detection

---

**Generated for Haze-Library v1.0**

For more information, visit the [GitHub repository](https://github.com/kwannz/haze).
