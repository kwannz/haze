#!/usr/bin/env python3
"""
生成 haze_library 类型存根文件 (.pyi)
从 Rust 源代码提取函数签名并生成 Python 类型注解
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

# Rust 类型到 Python 类型的映射
RUST_TO_PYTHON_TYPE = {
    'Vec<f64>': 'List[float]',
    'Vec<i64>': 'List[int]',
    'Vec<bool>': 'List[bool]',
    'f64': 'float',
    'i64': 'int',
    'usize': 'int',
    'bool': 'bool',
    'String': 'str',
    '&str': 'str',
}

def parse_rust_type(rust_type: str) -> str:
    """将 Rust 类型转换为 Python 类型注解"""
    rust_type = rust_type.strip()

    # 处理元组类型
    if rust_type.startswith('(') and rust_type.endswith(')'):
        inner = rust_type[1:-1]
        parts = [part.strip() for part in inner.split(',')]
        py_parts = [RUST_TO_PYTHON_TYPE.get(p, 'Any') for p in parts]
        return f"Tuple[{', '.join(py_parts)}]"

    # 处理简单类型
    return RUST_TO_PYTHON_TYPE.get(rust_type, 'Any')

def parse_parameter(param_str: str) -> Tuple[str, str, bool]:
    """解析参数定义,返回 (name, type, is_optional)"""
    param_str = param_str.strip()

    # 跳过空参数
    if not param_str:
        return None, None, False

    # 检查是否为 Option 类型
    is_optional = 'Option<' in param_str

    # 提取参数名和类型
    if ':' in param_str:
        name, type_part = param_str.split(':', 1)
        name = name.strip()
        type_part = type_part.strip()

        # 处理 Option 类型
        if is_optional:
            match = re.search(r'Option<(.+?)>', type_part)
            if match:
                inner_type = match.group(1)
                py_type = parse_rust_type(inner_type)
            else:
                py_type = 'Any'
        else:
            # 处理向量类型
            if type_part.startswith('Vec<'):
                py_type = parse_rust_type(type_part)
            else:
                py_type = parse_rust_type(type_part)

        return name, py_type, is_optional

    return None, None, False

def extract_functions_from_rust(rust_file: Path) -> Dict[str, dict]:
    """从 Rust 源文件提取所有 PyFunction 定义"""
    content = rust_file.read_text()

    functions = {}

    # 匹配 pyfunction 定义的模式
    pattern = r'#\[cfg\(feature = "python"\)\]\s*#\[pyfunction\]\s*fn (py_\w+)\((.*?)\)\s*->\s*PyResult<(.+?)>\s*\{'

    for match in re.finditer(pattern, content, re.DOTALL):
        func_name = match.group(1)
        params_str = match.group(2)
        return_type_str = match.group(3)

        # 解析参数
        params = []
        if params_str.strip():
            # 简单分割(不处理嵌套泛型中的逗号)
            param_parts = []
            depth = 0
            current = []
            for char in params_str:
                if char in '<(':
                    depth += 1
                elif char in '>)':
                    depth -= 1
                elif char == ',' and depth == 0:
                    param_parts.append(''.join(current))
                    current = []
                    continue
                current.append(char)
            if current:
                param_parts.append(''.join(current))

            for param in param_parts:
                name, py_type, is_optional = parse_parameter(param)
                if name:
                    params.append({
                        'name': name,
                        'type': py_type,
                        'optional': is_optional
                    })

        # 解析返回类型
        return_type = parse_rust_type(return_type_str)

        functions[func_name] = {
            'params': params,
            'return_type': return_type
        }

    return functions

def categorize_functions(functions: Dict[str, dict]) -> Dict[str, List[str]]:
    """根据函数名前缀和功能分类"""
    categories = {
        'Volatility': [],
        'Momentum': [],
        'Trend': [],
        'Volume': [],
        'Moving Averages': [],
        'Candlestick Patterns': [],
        'Statistical': [],
        'Price Transform': [],
        'Math Functions': [],
        'Fibonacci': [],
        'Pivot Points': [],
        'Ichimoku': [],
        'Cycle': [],
        'ML/AI Indicators': [],
        'Signal Functions': [],
        'Pattern Recognition': [],
        'Other': []
    }

    # 分类规则
    volatility = ['atr', 'natr', 'true_range', 'bollinger', 'keltner', 'donchian']
    momentum = ['rsi', 'macd', 'stochastic', 'stochrsi', 'cci', 'williams', 'awesome',
                'fisher', 'kdj', 'tsi', 'ultimate', 'mom', 'roc', 'apo', 'ppo', 'cmo']
    trend = ['supertrend', 'adx', 'aroon', 'psar', 'vortex', 'choppiness', 'qstick',
             'vhf', 'dx', 'plus_di', 'minus_di', 'sar', 'sarext']
    volume = ['obv', 'vwap', 'mfi', 'cmf', 'volume_profile', 'ad', 'pvt', 'nvi',
              'pvi', 'eom', 'adosc']
    ma = ['sma', 'ema', 'wma', 'dema', 'tema', 'hma', 'rma', 'zlma', 't3', 'kama',
          'frama', 'alma', 'vidya', 'pwma', 'sinwma', 'swma', 'vwma', 'trima', 'midpoint',
          'midprice', 'mama']
    candle = ['doji', 'hammer', 'hanging_man', 'engulfing', 'harami', 'piercing',
              'dark_cloud', 'star', 'soldiers', 'crows', 'shooting', 'marubozu',
              'spinning', 'tweezers', 'methods', 'takuri', 'pigeon', 'matching',
              'separating', 'thrusting', 'neck', 'advance_block', 'stalled', 'belthold',
              'baby', 'counterattack', 'highwave', 'hikkake', 'ladder', 'rickshaw',
              'river', 'xside', 'breakaway', 'sandwich', 'tristar', 'gap', 'kicking']
    stat = ['correlation', 'zscore', 'covariance', 'beta', 'standard_error',
            'linear_regression', 'correl', 'linearreg', 'var', 'tsf']
    price = ['avgprice', 'medprice', 'typprice', 'wclprice']
    math = ['max', 'min', 'sum', 'sqrt', 'ln', 'log10', 'exp', 'abs', 'ceil', 'floor',
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
            'add', 'sub', 'mult', 'div', 'minmax', 'minmaxindex', 'slope', 'percent_rank']
    fib = ['fib_retracement', 'fib_extension', 'fibonacci_pivots']
    pivot = ['standard_pivots', 'camarilla_pivots', 'pivot_buy_sell']
    ichimoku = ['ichimoku']
    cycle = ['ht_dcperiod', 'ht_dcphase', 'ht_phasor', 'ht_sine', 'ht_trendmode']
    ml = ['ai_supertrend', 'ai_momentum', 'dynamic_macd', 'atr2_signals',
          'detect_divergence', 'fvg_signals', 'volume_filter', 'pd_array',
          'breaker_block', 'general_parameters', 'linreg_supply']
    signal = ['combine_signals', 'calculate_stops']
    pattern = ['harmonics', 'swing_points']
    other_indicators = ['entropy', 'aberration', 'squeeze', 'qqe', 'cti', 'er',
                       'bias', 'psl', 'rvi', 'inertia', 'alligator', 'efi', 'kst',
                       'stc', 'tdfi', 'wae', 'smi', 'coppock', 'pgo', 'bop',
                       'ssl_channel', 'cfo']

    for func_name in functions.keys():
        # 移除 py_ 前缀
        clean_name = func_name.replace('py_', '')

        categorized = False
        for keyword in volatility:
            if keyword in clean_name:
                categories['Volatility'].append(func_name)
                categorized = True
                break

        if not categorized:
            for keyword in momentum:
                if keyword in clean_name:
                    categories['Momentum'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in trend:
                if keyword in clean_name:
                    categories['Trend'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in volume:
                if keyword in clean_name:
                    categories['Volume'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in ma:
                if keyword in clean_name:
                    categories['Moving Averages'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in candle:
                if keyword in clean_name:
                    categories['Candlestick Patterns'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in stat:
                if keyword in clean_name:
                    categories['Statistical'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in price:
                if keyword in clean_name:
                    categories['Price Transform'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in math:
                if keyword in clean_name:
                    categories['Math Functions'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in fib:
                if keyword in clean_name:
                    categories['Fibonacci'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in pivot:
                if keyword in clean_name:
                    categories['Pivot Points'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in ichimoku:
                if keyword in clean_name:
                    categories['Ichimoku'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in cycle:
                if keyword in clean_name:
                    categories['Cycle'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in ml:
                if keyword in clean_name:
                    categories['ML/AI Indicators'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in signal:
                if keyword in clean_name:
                    categories['Signal Functions'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in pattern:
                if keyword in clean_name:
                    categories['Pattern Recognition'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            for keyword in other_indicators:
                if keyword in clean_name:
                    categories['Other'].append(func_name)
                    categorized = True
                    break

        if not categorized:
            categories['Other'].append(func_name)

    return categories

def generate_function_stub(func_name: str, func_info: dict) -> str:
    """生成单个函数的类型存根"""
    params = func_info['params']
    return_type = func_info['return_type']

    # 构建参数列表
    param_strs = []
    for param in params:
        if param['optional']:
            param_strs.append(f"{param['name']}: Optional[{param['type']}] = None")
        else:
            param_strs.append(f"{param['name']}: {param['type']}")

    params_str = ', '.join(param_strs)

    # 生成函数签名
    stub = f"def {func_name}({params_str}) -> {return_type}: ..."

    return stub

def generate_pyi_file(functions: Dict[str, dict], output_file: Path):
    """生成完整的 .pyi 文件"""

    # 分类函数
    categories = categorize_functions(functions)

    # 生成文件内容
    lines = [
        '"""',
        'Haze-Library Type Stubs',
        '=' * 80,
        '',
        'Type annotations for haze_library Rust extension module.',
        'Provides IDE support for 225+ technical indicators.',
        '',
        'Auto-generated from Rust source code.',
        '"""',
        '',
        'from typing import Any, Dict, List, Optional, Tuple',
        '',
        '__version__: str',
        '__author__: str',
        '',
    ]

    # 添加分类的函数
    total_count = 0
    for category, func_names in categories.items():
        if not func_names:
            continue

        # 排序函数名
        func_names.sort()

        lines.append('')
        lines.append('# ' + '=' * 78)
        lines.append(f'# {category} ({len(func_names)} functions)')
        lines.append('# ' + '=' * 78)
        lines.append('')

        for func_name in func_names:
            stub = generate_function_stub(func_name, functions[func_name])
            lines.append(stub)
            total_count += 1

        lines.append('')

    # 添加类定义(如果有的话)
    lines.extend([
        '',
        '# ' + '=' * 78,
        '# Classes',
        '# ' + '=' * 78,
        '',
        'class Candle:',
        '    """OHLCV candle data structure."""',
        '    timestamp: int',
        '    open: float',
        '    high: float',
        '    low: float',
        '    close: float',
        '    volume: float',
        '    def __init__(self, timestamp: int, open: float, high: float, low: float, close: float, volume: float) -> None: ...',
        '    def to_dict(self) -> Dict[str, float]: ...',
        '    @property',
        '    def typical_price(self) -> float: ...',
        '    @property',
        '    def median_price(self) -> float: ...',
        '    @property',
        '    def weighted_close(self) -> float: ...',
        '    def __repr__(self) -> str: ...',
        '',
        'class IndicatorResult:',
        '    """Single indicator calculation result."""',
        '    name: str',
        '    values: List[float]',
        '    metadata: Dict[str, str]',
        '    def __init__(self, name: str, values: List[float]) -> None: ...',
        '    def add_metadata(self, key: str, value: str) -> None: ...',
        '    @property',
        '    def len(self) -> int: ...',
        '    def is_empty(self) -> bool: ...',
        '',
        'class MultiIndicatorResult:',
        '    """Multiple indicator calculation results."""',
        '    name: str',
        '    series: Dict[str, List[float]]',
        '    metadata: Dict[str, str]',
        '    def __init__(self, name: str) -> None: ...',
        '    def add_series(self, key: str, values: List[float]) -> None: ...',
        '    def add_metadata(self, key: str, value: str) -> None: ...',
        '',
        'class PyHarmonicPattern:',
        '    """Harmonic pattern recognition result."""',
        '    pattern_type: str',
        '    pattern_type_zh: str',
        '    is_bullish: bool',
        '    state: str',
        '    x_index: int',
        '    x_price: float',
        '    a_index: int',
        '    a_price: float',
        '    b_index: int',
        '    b_price: float',
        '    c_index: Optional[int]',
        '    c_price: Optional[float]',
        '    d_index: Optional[int]',
        '    d_price: Optional[float]',
        '    prz_high: Optional[float]',
        '    prz_low: Optional[float]',
        '    prz_center: Optional[float]',
        '    probability: float',
        '    target_prices: List[float]',
        '    stop_loss: Optional[float]',
        '',
    ])

    # 写入文件
    content = '\n'.join(lines)
    output_file.write_text(content)

    print(f"Generated {output_file}")
    print(f"Total functions: {total_count}")
    print("\nBreakdown by category:")
    for category, func_names in categories.items():
        if func_names:
            print(f"  {category}: {len(func_names)}")

def main():
    # 文件路径
    project_root = Path(__file__).parent
    rust_src = project_root / 'rust' / 'src' / 'lib.rs'
    output_pyi = project_root / 'src' / 'haze_library' / 'haze_library.pyi'

    print(f"Parsing Rust source: {rust_src}")

    # 提取函数
    functions = extract_functions_from_rust(rust_src)

    print(f"Found {len(functions)} functions")

    # 生成 .pyi 文件
    generate_pyi_file(functions, output_pyi)

if __name__ == '__main__':
    main()
