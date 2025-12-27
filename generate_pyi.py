#!/usr/bin/env python3
"""
Script to generate .pyi type stub file from Rust source code.
Extracts all #[pyfunction] declarations and their signatures.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

# Type mapping from Rust to Python
TYPE_MAPPING = {
    "f64": "float",
    "usize": "int",
    "i32": "int",
    "bool": "bool",
    "String": "str",
}

CUSTOM_TUPLE_MAPPING = {
    "Vec4F64": "tuple[list[float], list[float], list[float], list[float]]",
    "Vec5F64": "tuple[list[float], list[float], list[float], list[float], list[float]]",
    "Vec6F64": "tuple[list[float], list[float], list[float], list[float], list[float], list[float]]",
    "Vec7F64": "tuple[list[float], list[float], list[float], list[float], list[float], list[float], list[float]]",
    "Pivots9F64": "tuple[float, float, float, float, float, float, float, float, float]",
}

CUSTOM_CLASS_MAPPING = {
    "PyHarmonicPattern": "PyHarmonicPattern",
    "PySFGModel": "SFGModel",
    "PyOhlcvFrame": "OhlcvFrame",
    "Candle": "Candle",
    "IndicatorResult": "IndicatorResult",
    "MultiIndicatorResult": "MultiIndicatorResult",
}

PYCLASS_STUBS = """
class Candle:
    \"\"\"OHLCV Candle data structure.\"\"\"
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    def __init__(self, timestamp: int, open: float, high: float, low: float, close: float, volume: float) -> None: ...
    def to_dict(self) -> dict[str, float]: ...
    @property
    def typical_price(self) -> float: ...
    @property
    def median_price(self) -> float: ...
    @property
    def weighted_close(self) -> float: ...

class IndicatorResult:
    \"\"\"Single indicator result container.\"\"\"
    name: str
    values: list[float]
    metadata: dict[str, str]
    def __init__(self, name: str, values: list[float]) -> None: ...
    def add_metadata(self, key: str, value: str) -> None: ...
    @property
    def len(self) -> int: ...
    def is_empty(self) -> bool: ...

class MultiIndicatorResult:
    \"\"\"Multiple indicator result container.\"\"\"
    name: str
    series: dict[str, list[float]]
    metadata: dict[str, str]
    def __init__(self, name: str) -> None: ...
    def add_series(self, key: str, values: list[float]) -> None: ...
    def add_metadata(self, key: str, value: str) -> None: ...

class OhlcvFrame:
    \"\"\"Cached OHLCV frame for fast repeated computations.\"\"\"
    def __init__(
        self,
        timestamps: list[int],
        open: list[float],
        high: list[float],
        low: list[float],
        close: list[float],
        volume: list[float],
    ) -> None: ...
    def len(self) -> int: ...
    def __len__(self) -> int: ...
    def is_empty(self) -> bool: ...
    def clear_cache(self) -> None: ...
    def cached_indicators(self) -> list[str]: ...
    def get_cached(self, name: str) -> list[float] | None: ...
    def compute_common_indicators(self) -> dict[str, list[float]]: ...
    def sma(self, period: int) -> list[float]: ...
    def ema(self, period: int) -> list[float]: ...
    def wma(self, period: int) -> list[float]: ...
    def hma(self, period: int) -> list[float]: ...
    def atr(self, period: int) -> list[float]: ...
    def true_range(self) -> list[float]: ...
    def bollinger_bands(self, period: int, std_dev: float) -> tuple[list[float], list[float], list[float]]: ...
    def rsi(self, period: int) -> list[float]: ...
    def macd(self, fast: int, slow: int, signal: int) -> tuple[list[float], list[float], list[float]]: ...
    def stochastic(self, k_period: int, d_period: int) -> tuple[list[float], list[float]]: ...
    def cci(self, period: int) -> list[float]: ...
    def williams_r(self, period: int) -> list[float]: ...
    def supertrend(self, period: int, multiplier: float) -> tuple[list[float], list[float], list[float], list[float]]: ...
    def adx(self, period: int) -> tuple[list[float], list[float], list[float]]: ...
    def obv(self) -> list[float]: ...
    def vwap(self, period: int) -> list[float]: ...
    def mfi(self, period: int) -> list[float]: ...

class PyHarmonicPattern:
    \"\"\"Harmonic pattern detection result.\"\"\"
    pattern_type: str
    pattern_type_zh: str
    is_bullish: bool
    state: str
    x_index: int
    x_price: float
    a_index: int
    a_price: float
    b_index: int
    b_price: float
    c_index: int | None
    c_price: float | None
    d_index: int | None
    d_price: float | None
    prz_high: float | None
    prz_low: float | None
    prz_center: float | None
    probability: float
    target_prices: list[float]
    stop_loss: float | None

class SFGModel:
    \"\"\"Python-accessible ML model wrapper.\"\"\"
    def is_trained(self) -> bool: ...
    def features_dim(self) -> int: ...
    def predict(self, features: list[float], n_samples: int) -> list[float]: ...
"""


def map_rust_type_to_python(rust_type: str, has_default: bool = False) -> str:
    """Map Rust type to Python type annotation."""
    rust_type = rust_type.strip()

    # Handle Option<T>
    if rust_type.startswith("Option<"):
        inner_match = re.search(r"Option<(.+)>$", rust_type)
        if inner_match:
            inner_type = inner_match.group(1).strip()
            base_type = map_rust_type_to_python(inner_type)
            if has_default:
                return base_type
            return f"{base_type} | None"

    # Custom class types
    if rust_type in CUSTOM_CLASS_MAPPING:
        return CUSTOM_CLASS_MAPPING[rust_type]

    # Custom tuple aliases
    if rust_type in CUSTOM_TUPLE_MAPPING:
        return CUSTOM_TUPLE_MAPPING[rust_type]

    # Handle Vec<T>
    if rust_type.startswith("Vec<") and rust_type.endswith(">"):
        inner_type = rust_type[4:-1].strip()
        return f"list[{map_rust_type_to_python(inner_type)}]"

    # Direct mapping
    if rust_type in TYPE_MAPPING:
        return TYPE_MAPPING[rust_type]

    # Handle tuple types
    if rust_type.startswith("(") and rust_type.endswith(")"):
        inner = rust_type[1:-1]
        parts = []
        depth = 0
        current = []
        for char in inner:
            if char == "<":
                depth += 1
            elif char == ">":
                depth -= 1
            elif char == "," and depth == 0:
                parts.append("".join(current).strip())
                current = []
                continue
            current.append(char)
        if current:
            parts.append("".join(current).strip())

        python_parts = [map_rust_type_to_python(p) for p in parts]
        return f"tuple[{', '.join(python_parts)}]"

    # Custom struct types - fallback
    if any(x in rust_type for x in ["Pivots", "Ichimoku"]):
        return "dict[str, float | list[float]]"

    return "float"


def extract_function_signature(block: str) -> Optional[Dict]:
    """Extract function signature from a #[pyfunction] block."""
    # Extract function name
    fn_match = re.search(r"fn (py_\w+)\s*\(", block)
    if not fn_match:
        return None

    fn_name = fn_match.group(1)

    # Extract full function signature
    fn_sig_match = re.search(r"fn py_\w+\s*\((.*?)\)\s*->\s*([^{]+)", block, re.DOTALL)
    if not fn_sig_match:
        return None

    params_str = fn_sig_match.group(1)
    return_type_str = fn_sig_match.group(2).strip()

    # Extract text_signature for defaults
    text_sig_match = re.search(r'text_signature = "([^"]+)"', block)
    defaults = {}
    if text_sig_match:
        text_sig = text_sig_match.group(1)
        sig_params = re.search(r"\(([^)]*)\)", text_sig)
        if sig_params:
            for param in sig_params.group(1).split(","):
                param = param.strip()
                if "=" in param:
                    name, default = param.split("=", 1)
                    defaults[name.strip()] = default.strip()

    # Parse parameters
    params = []
    if params_str.strip():
        depth = 0
        current = []
        params_list = []
        for char in params_str:
            if char == "<":
                depth += 1
            elif char == ">":
                depth -= 1
            elif char == "," and depth == 0:
                params_list.append("".join(current).strip())
                current = []
                continue
            current.append(char)
        if current:
            params_list.append("".join(current).strip())

        for param in params_list:
            param = param.strip()
            if not param or param.startswith("_"):
                continue

            if ":" in param:
                parts = param.split(":", 1)
                param_name = parts[0].strip()
                rust_type = parts[1].strip()

                has_default = param_name in defaults
                python_type = map_rust_type_to_python(rust_type, has_default)

                if has_default:
                    params.append((param_name, python_type, defaults[param_name]))
                else:
                    params.append((param_name, python_type, None))

    # Parse return type
    return_type = "None"
    if "PyResult<" in return_type_str:
        inner_match = re.search(r"PyResult<(.+)>$", return_type_str)
        if inner_match:
            inner_type = inner_match.group(1).strip()
            return_type = map_rust_type_to_python(inner_type)

    # Extract first line of docstring
    doc_match = re.search(r"/// (.+?)(?=\n///\s*\n|\nfn|\n#)", block, re.DOTALL)
    doc = doc_match.group(1).strip() if doc_match else f"Calculate {fn_name}"
    doc_first_line = doc.split("\n")[0]

    return {
        "name": fn_name,
        "params": params,
        "return_type": return_type,
        "doc": doc_first_line,
    }


def extract_functions(rust_file: Path) -> List[Dict]:
    """Extract all Python functions from Rust source."""
    content = rust_file.read_text()

    # Find all #[pyfunction] blocks
    pattern = r"#\[pyfunction\].*?(?=\n#\[pyfunction\]|\nstruct|\npub struct|\Z)"
    matches = re.finditer(pattern, content, re.DOTALL)

    functions = []
    for match in matches:
        block = match.group(0)
        sig = extract_function_signature(block)
        if sig:
            functions.append(sig)

    return functions


def categorize_functions(functions: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize functions by their purpose."""
    categories = {
        "Volatility Indicators": [],
        "Momentum Indicators": [],
        "Trend Indicators": [],
        "Volume Indicators": [],
        "Overlap/MA Indicators": [],
        "Pattern Recognition": [],
        "Statistical Functions": [],
        "Price Transforms": [],
        "Math Operators": [],
        "Utility Functions": [],
        "Advanced Indicators": [],
        "Hilbert Transform": [],
    }

    volatility = [
        "atr",
        "natr",
        "true_range",
        "bollinger",
        "keltner",
        "donchian",
        "chandelier",
        "historical_volatility",
        "ulcer",
        "mass_index",
        "aberration",
    ]

    momentum = [
        "rsi",
        "macd",
        "stochastic",
        "stochrsi",
        "cci",
        "williams",
        "awesome_oscillator",
        "fisher_transform",
        "mom",
        "roc",
        "tsi",
        "ultimate_oscillator",
        "kdj",
        "vortex",
        "qstick",
        "cmo",
        "cti",
        "er",
        "bias",
        "psl",
        "rvi",
        "inertia",
        "kst",
        "stc",
        "tdfi",
        "smi",
        "coppock",
        "pgo",
        "cfo",
        "qqe",
        "entropy",
    ]

    trend = [
        "adx",
        "aroon",
        "psar",
        "supertrend",
        "trix",
        "dpo",
        "dx",
        "plus_di",
        "minus_di",
        "slope",
        "choppiness",
        "vhf",
        "alligator",
    ]

    volume = [
        "obv",
        "vwap",
        "force_index",
        "volume_oscillator",
        "mfi",
        "cmf",
        "volume_profile",
        "ad",
        "pvt",
        "nvi",
        "pvi",
        "eom",
        "adosc",
        "volume_filter",
        "efi",
        "vwma",
        "bop",
    ]

    overlap = [
        "sma",
        "ema",
        "rma",
        "wma",
        "hma",
        "dema",
        "tema",
        "zlma",
        "frama",
        "t3",
        "kama",
        "trima",
        "sar",
        "sarext",
        "mama",
        "alma",
        "vidya",
        "pwma",
        "sinwma",
        "swma",
        "ssl_channel",
    ]

    patterns = [
        "doji",
        "hammer",
        "inverted_hammer",
        "hanging_man",
        "bullish_engulfing",
        "bearish_engulfing",
        "bullish_harami",
        "bearish_harami",
        "piercing_pattern",
        "dark_cloud_cover",
        "morning_star",
        "evening_star",
        "three_white_soldiers",
        "three_black_crows",
        "shooting_star",
        "marubozu",
        "spinning_top",
        "dragonfly_doji",
        "gravestone_doji",
        "long_legged_doji",
        "tweezers",
        "rising_three_methods",
        "falling_three_methods",
        "harami_cross",
        "morning_doji_star",
        "evening_doji_star",
        "three_inside",
        "three_outside",
        "abandoned_baby",
        "kicking",
        "long_line",
        "short_line",
        "doji_star",
        "identical_three_crows",
        "stick_sandwich",
        "tristar",
        "upside_gap_two_crows",
        "gap_sidesidewhite",
        "takuri",
        "homing_pigeon",
        "matching_low",
        "separating_lines",
        "thrusting",
        "inneck",
        "onneck",
        "advance_block",
        "stalled_pattern",
        "belthold",
        "concealing_baby_swallow",
        "counterattack",
        "highwave",
        "hikkake",
        "hikkake_mod",
        "ladder_bottom",
        "mat_hold",
        "rickshaw_man",
        "unique_3_river",
        "xside_gap_3_methods",
        "closing_marubozu",
        "breakaway",
        "harmonics",
        "harmonics_patterns",
        "swing_points",
    ]

    statistical = [
        "linear_regression",
        "correlation",
        "zscore",
        "covariance",
        "beta",
        "standard_error",
        "stderr",
        "correl",
        "linearreg",
        "linearreg_slope",
        "linearreg_angle",
        "linearreg_intercept",
        "var",
        "tsf",
        "percent_rank",
    ]

    price_transforms = ["avgprice", "medprice", "typprice", "wclprice", "midpoint", "midprice"]

    math_ops = [
        "max",
        "min",
        "sum",
        "sqrt",
        "ln",
        "log10",
        "exp",
        "abs",
        "ceil",
        "floor",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sinh",
        "cosh",
        "tanh",
        "add",
        "sub",
        "mult",
        "div",
        "minmax",
        "minmaxindex",
    ]

    advanced = [
        "ai_supertrend",
        "ai_momentum_index",
        "dynamic_macd",
        "atr2_signals",
        "ai_supertrend_ml",
        "atr2_signals_ml",
        "ai_momentum_index_ml",
        "pivot_buy_sell",
        "detect_divergence",
        "fvg_signals",
        "combine_signals",
        "calculate_stops",
        "pd_array_signals",
        "breaker_block_signals",
        "general_parameters_signals",
        "linreg_supply_demand_signals",
        "squeeze",
        "wae",
    ]

    hilbert = ["ht_dcperiod", "ht_dcphase", "ht_phasor", "ht_sine", "ht_trendmode"]

    utility = ["fib_retracement", "fib_extension", "ichimoku_cloud", "standard_pivots", "fibonacci_pivots", "camarilla_pivots", "apo", "ppo"]

    for fn_data in functions:
        fn_name = fn_data["name"]
        name_lower = fn_name.lower().replace("py_", "")

        categorized = False
        for pattern in volatility:
            if pattern in name_lower:
                categories["Volatility Indicators"].append(fn_data)
                categorized = True
                break

        if not categorized:
            for pattern in momentum:
                if pattern in name_lower:
                    categories["Momentum Indicators"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in trend:
                if pattern in name_lower:
                    categories["Trend Indicators"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in volume:
                if pattern in name_lower:
                    categories["Volume Indicators"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in overlap:
                if pattern in name_lower:
                    categories["Overlap/MA Indicators"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in patterns:
                if pattern in name_lower:
                    categories["Pattern Recognition"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in statistical:
                if pattern in name_lower:
                    categories["Statistical Functions"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in price_transforms:
                if pattern in name_lower:
                    categories["Price Transforms"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in math_ops:
                if pattern in name_lower:
                    categories["Math Operators"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in advanced:
                if pattern in name_lower:
                    categories["Advanced Indicators"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in hilbert:
                if pattern in name_lower:
                    categories["Hilbert Transform"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            for pattern in utility:
                if pattern in name_lower:
                    categories["Utility Functions"].append(fn_data)
                    categorized = True
                    break

        if not categorized:
            categories["Utility Functions"].append(fn_data)

    return categories


def generate_pyi(categories: Dict) -> str:
    """Generate the .pyi file content."""
    output = []

    # Header
    output.append('"""Type stubs for haze_library.haze_library')
    output.append("")
    output.append("Auto-generated from Rust source code.")
    output.append("This module provides technical analysis indicators implemented in Rust.")
    output.append('"""')
    output.append("")

    if PYCLASS_STUBS.strip():
        output.extend(PYCLASS_STUBS.strip().splitlines())
        output.append("")

    # Generate functions by category
    for category, fn_list in categories.items():
        if not fn_list:
            continue

        output.append(f"# {category}")
        output.append("")

        for fn_data in sorted(fn_list, key=lambda x: x["name"]):
            param_parts = []
            for param_name, param_type, default in fn_data["params"]:
                if default:
                    param_parts.append(f"{param_name}: {param_type} = {default}")
                else:
                    param_parts.append(f"{param_name}: {param_type}")

            params_str = ", ".join(param_parts)
            output.append(
                f'def {fn_data["name"]}({params_str}) -> {fn_data["return_type"]}: ...'
            )

        output.append("")

    return "\n".join(output)


def main():
    """Main function."""
    rust_file = Path(__file__).parent / "rust" / "src" / "lib.rs"
    output_file = Path(__file__).parent / "src" / "haze_library" / "haze_library.pyi"

    print(f"Reading Rust source: {rust_file}")
    functions = extract_functions(rust_file)
    print(f"Found {len(functions)} functions")

    print("Categorizing functions...")
    categories = categorize_functions(functions)

    for category, fns in categories.items():
        if fns:
            print(f"  {category}: {len(fns)} functions")

    print("Generating .pyi file...")
    pyi_content = generate_pyi(categories)

    print(f"Writing to: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(pyi_content)

    print("Done!")
    print(f"\nTotal functions: {len(functions)}")


if __name__ == "__main__":
    main()
