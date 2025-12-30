#!/usr/bin/env python3
"""
零拷贝迁移自动化工具

功能:
1. 解析 lib.rs 中所有 #[pyfunction] 定义
2. 分类函数模式 (1→1, n→1, 1→n, n→m)
3. 自动生成零拷贝版本代码
4. 批量输出到临时文件供审查

使用示例:
    python scripts/migrate_to_zero_copy.py --analyze
    python scripts/migrate_to_zero_copy.py --generate 1to1 --output migration_output/phase1/
"""

import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class FunctionPattern(Enum):
    """函数模式分类"""
    SINGLE_TO_SINGLE = "1→1"  # 单输入单输出
    MULTI_TO_SINGLE = "n→1"   # 多输入单输出
    SINGLE_TO_MULTI = "1→n"   # 单输入多输出
    MULTI_TO_MULTI = "n→m"    # 多输入多输出
    SPECIAL = "special"       # 特殊类型


@dataclass
class Parameter:
    """参数信息"""
    name: str
    rust_type: str
    is_array: bool  # 是否是 Vec<f64> 类型


@dataclass
class FunctionInfo:
    """函数信息"""
    name: str  # py_sma
    params: List[Parameter]
    return_type: str  # Vec<f64> 或 (Vec<f64>, Vec<f64>)
    pattern: FunctionPattern
    original_code: str
    vec_inputs: int   # Vec<f64> 输入数量
    vec_outputs: int  # Vec<f64> 输出数量
    core_func: Optional[str] = None  # indicators::sma
    option_defaults: Optional[Dict[str, str]] = None  # Option 参数的默认值


class ZeroCopyMigrator:
    """零拷贝代码生成器"""

    def __init__(self, lib_rs_path: str):
        self.lib_rs_path = Path(lib_rs_path)
        self.lib_rs_content = self.lib_rs_path.read_text(encoding='utf-8')
        self.functions: List[FunctionInfo] = []

    def extract_all_functions(self) -> List[FunctionInfo]:
        """
        提取所有未迁移的 #[pyfunction] 函数定义 (使用 Vec<f64> 的函数)

        匹配模式:
        #[pyfunction]
        #[pyo3(...)] (可选)
        fn py_sma(
            values: Vec<f64>,
            period: usize
        ) -> PyResult<Vec<f64>> {
            ...
        }
        """
        # 匹配 #[pyfunction] 到函数体开始的 {
        # 关键：查找使用 Vec<f64> 的函数（未迁移）
        pattern = r'#\[pyfunction(?:\([^\)]*\))?\].*?fn\s+(py_\w+)\s*\((.*?)\)\s*->\s*(PyResult<[^{]+?)\s*\{'

        matches = re.finditer(pattern, self.lib_rs_content, re.MULTILINE | re.DOTALL)

        functions = []
        for match in matches:
            func_name = match.group(1)
            params_str = match.group(2)
            return_type = match.group(3).strip()

            # 跳过 _legacy 函数（我们只处理待迁移的原始函数）
            if '_legacy' in func_name:
                continue

            # 解析参数
            params = self._parse_parameters(params_str)

            # 分类模式
            vec_inputs = sum(1 for p in params if p.is_array)
            vec_outputs = self._count_vec_outputs(return_type)

            pattern = self._classify_pattern(vec_inputs, vec_outputs)

            # 提取核心函数调用
            core_func = self._extract_core_function(func_name, match.start())

            # 提取 Option 参数的默认值
            option_defaults = self.extract_default_values(func_name)

            func_info = FunctionInfo(
                name=func_name,
                params=params,
                return_type=return_type,
                pattern=pattern,
                original_code=match.group(0),
                vec_inputs=vec_inputs,
                vec_outputs=vec_outputs,
                core_func=core_func,
                option_defaults=option_defaults if option_defaults else None
            )

            functions.append(func_info)

        self.functions = functions
        return functions

    def _parse_parameters(self, params_str: str) -> List[Parameter]:
        """
        解析参数列表

        示例:
        "values: Vec<f64>, period: usize" →
        [Parameter('values', 'Vec<f64>', True), Parameter('period', 'usize', False)]
        """
        params = []

        # 分割参数（处理复杂类型如 Option<usize>）
        # 简单实现：按逗号分割，但需要处理嵌套的 <>
        param_parts = []
        current = []
        depth = 0

        for char in params_str + ',':
            if char == '<':
                depth += 1
                current.append(char)
            elif char == '>':
                depth -= 1
                current.append(char)
            elif char == ',' and depth == 0:
                if current:
                    param_parts.append(''.join(current).strip())
                current = []
            else:
                current.append(char)

        for part in param_parts:
            if ':' not in part:
                continue

            param_name, param_type = part.split(':', 1)
            param_name = param_name.strip()
            param_type = param_type.strip()

            # 检查是否是 Vec<f64> 类型
            is_array = 'Vec<f64>' in param_type

            params.append(Parameter(param_name, param_type, is_array))

        return params

    def _count_vec_outputs(self, return_type: str) -> int:
        """
        统计返回值中的 Vec<f64> 数量

        示例:
        "PyResult<Vec<f64>>" → 1
        "PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)>" → 3
        """
        # 直接统计 Vec<f64> 出现次数
        # 这样可以正确处理各种格式:
        # - PyResult<Vec<f64>> → 1
        # - PyResult<(Vec<f64>, Vec<f64>)> → 2
        # - (Vec<f64>, Vec<f64>, Vec<f64>) → 3
        count = return_type.count('Vec<f64>')
        return count

    def _classify_pattern(self, vec_inputs: int, vec_outputs: int) -> FunctionPattern:
        """分类函数模式"""
        if vec_inputs == 0 or vec_outputs == 0:
            return FunctionPattern.SPECIAL

        if vec_inputs == 1 and vec_outputs == 1:
            return FunctionPattern.SINGLE_TO_SINGLE
        elif vec_inputs > 1 and vec_outputs == 1:
            return FunctionPattern.MULTI_TO_SINGLE
        elif vec_inputs == 1 and vec_outputs > 1:
            return FunctionPattern.SINGLE_TO_MULTI
        else:
            return FunctionPattern.MULTI_TO_MULTI

    def _extract_core_function(self, func_name: str, start_pos: int) -> Optional[str]:
        """
        提取核心算法函数调用

        在函数体中查找类似 indicators::sma 或 utils::ema 的调用
        """
        # 查找函数体（从 { 到配对的 }）
        # 简化实现：查找前 500 个字符
        snippet = self.lib_rs_content[start_pos:start_pos + 1000]

        # 查找 indicators:: 或 utils:: 调用
        match = re.search(r'(indicators|utils)::(\w+)', snippet)
        if match:
            module = match.group(1)
            func = match.group(2)
            return f"{module}::{func}"

        return None

    def extract_default_values(self, func_name: str) -> Dict[str, str]:
        """
        从原函数中提取 Option 参数的默认值

        示例:
        fn py_alma(..., period.unwrap_or(9), offset.unwrap_or(0.85), ...)
        → {'period': '9', 'offset': '0.85', 'sigma': '6.0'}

        Returns:
            Dict[param_name, default_value_str]
        """
        # 查找函数定义的开始位置
        func_pattern = rf'fn\s+{func_name}\s*\('
        match = re.search(func_pattern, self.lib_rs_content)
        if not match:
            return {}

        # 从函数定义开始，使用花括号计数找到函数体
        start_pos = match.start()
        # 找到第一个 {
        brace_start = self.lib_rs_content.find('{', start_pos)
        if brace_start == -1:
            return {}

        # 使用花括号计数找到匹配的 }
        brace_count = 1
        pos = brace_start + 1
        while pos < len(self.lib_rs_content) and brace_count > 0:
            if self.lib_rs_content[pos] == '{':
                brace_count += 1
            elif self.lib_rs_content[pos] == '}':
                brace_count -= 1
            pos += 1

        if brace_count != 0:
            return {}

        # 提取函数体（从 { 到 } 之间）
        func_body = self.lib_rs_content[brace_start+1:pos-1]

        # 提取所有 .unwrap_or(...) 模式
        # 支持格式:
        # - period.unwrap_or(14)
        # - period.unwrap_or(14usize)
        # - offset.unwrap_or(0.85)
        # - std_multiplier.unwrap_or(2.0)
        defaults = {}

        unwrap_pattern = r'(\w+)\.unwrap_or\(([\w.]+?)\)'
        for match in re.finditer(unwrap_pattern, func_body):
            param_name = match.group(1)
            default_value = match.group(2)

            # 清理默认值（去除类型后缀如 usize, f64）
            default_value = re.sub(r'(usize|f64|f32|i32|i64)$', '', default_value)

            defaults[param_name] = default_value

        return defaults

    def generate_zero_copy_code(self, func_info: FunctionInfo) -> str:
        """
        生成零拷贝版本代码

        根据函数模式选择不同的模板
        """
        if func_info.pattern == FunctionPattern.SINGLE_TO_SINGLE:
            return self._generate_1to1(func_info)
        elif func_info.pattern == FunctionPattern.MULTI_TO_SINGLE:
            return self._generate_nto1(func_info)
        elif func_info.pattern == FunctionPattern.SINGLE_TO_MULTI:
            return self._generate_1ton(func_info)
        elif func_info.pattern == FunctionPattern.MULTI_TO_MULTI:
            return self._generate_ntom(func_info)
        else:
            return f"// SPECIAL PATTERN - 需要人工处理\n// {func_info.name}\n"

    def _generate_1to1(self, func_info: FunctionInfo) -> str:
        """生成 1→1 模式代码"""
        # 准备参数列表
        new_params = []
        slice_conversions = []
        call_params = []

        for param in func_info.params:
            if param.is_array:
                # Vec<f64> → PyReadonlyArray1
                new_params.append(f"    {param.name}: numpy::PyReadonlyArray1<'py, f64>,")
                slice_conversions.append(
                    f"    let {param.name}_slice = {param.name}.as_slice().expect(\"Failed to get array slice\");"
                )
                call_params.append(f"{param.name}_slice")
            else:
                # 保持原样 (Option<usize>, usize 等)
                new_params.append(f"    {param.name}: {param.rust_type},")

                # 检查是否是 Option 类型且有默认值
                if 'Option<' in param.rust_type and func_info.option_defaults:
                    default_val = func_info.option_defaults.get(param.name)
                    if default_val:
                        # 生成 param.unwrap_or(default)
                        call_params.append(f"{param.name}.unwrap_or({default_val})")
                    else:
                        call_params.append(param.name)
                else:
                    call_params.append(param.name)

        # 确定第一个数组参数名（用于获取长度）
        first_array = next((p.name for p in func_info.params if p.is_array), 'values')

        # 生成代码
        template = f'''// === 迁移后 (零拷贝版本) ===
#[cfg(feature = "python")]
#[pyfunction]
fn {func_info.name}<'py>(
    py: Python<'py>,
{chr(10).join(new_params)}
) -> pyo3::Py<numpy::PyArray1<f64>> {{
    use crate::ffi::zero_copy;

{chr(10).join(slice_conversions)}

    let len = {first_array}_slice.len();

    // 调用核心算法
    let result = {func_info.core_func or "/* TODO: 补充核心函数调用 */"}({', '.join(call_params)}).ok();

    zero_copy::to_pyarray_or_nan(py, result, len)
        .expect("Failed to create NumPy array")
        .unbind()
}}
'''
        return template

    def _generate_nto1(self, func_info: FunctionInfo) -> str:
        """生成 n→1 模式代码 (含长度验证)"""
        new_params = []
        slice_conversions = []
        call_params = []
        array_params = []

        for param in func_info.params:
            if param.is_array:
                new_params.append(f"    {param.name}: numpy::PyReadonlyArray1<'py, f64>,")
                slice_conversions.append(
                    f"    let {param.name}_slice = {param.name}.as_slice().expect(\"Failed to get array slice\");"
                )
                call_params.append(f"{param.name}_slice")
                array_params.append(param.name)
            else:
                new_params.append(f"    {param.name}: {param.rust_type},")
                call_params.append(param.name)

        # 生成长度验证代码
        first_array = array_params[0]
        length_checks = [
            f"    let len = {first_array}_slice.len();"
        ]
        for arr in array_params[1:]:
            length_checks.append(
                f"    if {arr}_slice.len() != len {{\n"
                f"        return Err(PyValueError::new_err(\"Input arrays must have same length\"));\n"
                f"    }}"
            )

        template = f'''// === 迁移后 (零拷贝版本) - 多输入单输出 ===
#[cfg(feature = "python")]
#[pyfunction]
fn {func_info.name}<'py>(
    py: Python<'py>,
{chr(10).join(new_params)}
) -> PyResult<pyo3::Py<numpy::PyArray1<f64>>> {{
    use crate::ffi::zero_copy;
    use pyo3::exceptions::PyValueError;

{chr(10).join(slice_conversions)}

{chr(10).join(length_checks)}

    // 调用核心算法
    let result = {func_info.core_func or "/* TODO: 补充核心函数调用 */"}({', '.join(call_params)}).ok();

    Ok(zero_copy::to_pyarray_or_nan(py, result, len)
        .expect("Failed to create NumPy array")
        .unbind())
}}
'''
        return template

    def _generate_1ton(self, func_info: FunctionInfo) -> str:
        """生成 1→n 模式代码 (多输出)"""
        outputs = func_info.vec_outputs

        # 使用对应的 to_pyarrayN_or_nan
        helper_func = f"to_pyarray{outputs}_or_nan" if outputs > 1 else "to_pyarray_or_nan"

        # 生成参数
        new_params = []
        slice_conversions = []
        call_params = []

        for param in func_info.params:
            if param.is_array:
                new_params.append(f"    {param.name}: numpy::PyReadonlyArray1<'py, f64>,")
                slice_conversions.append(
                    f"    let {param.name}_slice = {param.name}.as_slice().expect(\"Failed to get array slice\");"
                )
                call_params.append(f"{param.name}_slice")
            else:
                new_params.append(f"    {param.name}: {param.rust_type},")
                call_params.append(param.name)

        first_array = next((p.name for p in func_info.params if p.is_array), 'values')

        # 生成返回类型
        return_type = ', '.join([f"pyo3::Py<numpy::PyArray1<f64>>"] * outputs)
        if outputs > 1:
            return_type = f"({return_type})"

        # 生成解包代码
        if outputs == 2:
            unpack = "(arr1, arr2)"
            unbind = "(arr1.unbind(), arr2.unbind())"
        elif outputs == 3:
            unpack = "(arr1, arr2, arr3)"
            unbind = "(arr1.unbind(), arr2.unbind(), arr3.unbind())"
        elif outputs == 4:
            unpack = "(arr1, arr2, arr3, arr4)"
            unbind = "(arr1.unbind(), arr2.unbind(), arr3.unbind(), arr4.unbind())"
        elif outputs == 5:
            unpack = "(arr1, arr2, arr3, arr4, arr5)"
            unbind = "(arr1.unbind(), arr2.unbind(), arr3.unbind(), arr4.unbind(), arr5.unbind())"
        else:
            unpack = "arr"
            unbind = "arr.unbind()"

        template = f'''// === 迁移后 (零拷贝版本) - 单输入多输出 ===
#[cfg(feature = "python")]
#[pyfunction]
fn {func_info.name}<'py>(
    py: Python<'py>,
{chr(10).join(new_params)}
) -> {return_type} {{
    use crate::ffi::zero_copy;

{chr(10).join(slice_conversions)}

    let len = {first_array}_slice.len();

    // 调用核心算法
    let result = {func_info.core_func or "/* TODO: 补充核心函数调用 */"}({', '.join(call_params)}).ok();

    let {unpack} = zero_copy::{helper_func}(py, result, len)
        .expect("Failed to create NumPy arrays");

    {unbind}
}}
'''
        return template

    def _generate_ntom(self, func_info: FunctionInfo) -> str:
        """生成 n→m 模式代码 (多输入多输出 - 最复杂)"""
        # 结合 n→1 和 1→n 的逻辑
        return self._generate_1ton(func_info)  # 复用 1→n 模板

    def generate_batch(self, pattern_filter: str, output_dir: str) -> List[FunctionInfo]:
        """
        批量生成代码

        Args:
            pattern_filter: "1→1", "n→1", "1→n", "n→m"
            output_dir: 输出目录
        """
        if not self.functions:
            self.extract_all_functions()

        # 过滤函数
        pattern_map = {
            "1to1": FunctionPattern.SINGLE_TO_SINGLE,
            "nto1": FunctionPattern.MULTI_TO_SINGLE,
            "1ton": FunctionPattern.SINGLE_TO_MULTI,
            "ntom": FunctionPattern.MULTI_TO_MULTI,
        }

        target_pattern = pattern_map.get(pattern_filter)
        if not target_pattern:
            print(f"❌ 未知模式: {pattern_filter}")
            return []

        filtered = [f for f in self.functions if f.pattern == target_pattern]

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for func_info in filtered:
            code = self.generate_zero_copy_code(func_info)

            output_file = output_path / f"{func_info.name}.rs"
            output_file.write_text(code, encoding='utf-8')

        print(f"✅ 生成 {len(filtered)} 个函数 (模式: {target_pattern.value})")
        print(f"📁 输出目录: {output_dir}")

        return filtered

    def analyze(self) -> None:
        """分析所有函数并生成统计报告"""
        if not self.functions:
            self.extract_all_functions()

        # 统计
        total = len(self.functions)
        pattern_stats = {}

        for func in self.functions:
            pattern = func.pattern.value
            if pattern not in pattern_stats:
                pattern_stats[pattern] = []
            pattern_stats[pattern].append(func.name)

        print(f"\n📊 函数分析报告")
        print(f"=" * 60)
        print(f"总函数数: {total}")
        print(f"\n按模式分类:")
        for pattern, funcs in sorted(pattern_stats.items()):
            print(f"  {pattern}: {len(funcs)} 个 ({len(funcs)/total*100:.1f}%)")
            # 显示前 5 个示例
            for name in funcs[:5]:
                print(f"    - {name}")
            if len(funcs) > 5:
                print(f"    ... ({len(funcs) - 5} 个更多)")
        print(f"=" * 60)


def main():
    parser = argparse.ArgumentParser(description='零拷贝迁移自动化工具')
    parser.add_argument('--lib-rs', default='/Users/zhaoleon/Desktop/haze/haze/rust/src/lib.rs',
                        help='lib.rs 文件路径')
    parser.add_argument('--analyze', action='store_true',
                        help='分析所有函数')
    parser.add_argument('--generate', choices=['1to1', 'nto1', '1ton', 'ntom'],
                        help='生成指定模式的代码')
    parser.add_argument('--output', default='migration_output/',
                        help='输出目录')

    args = parser.parse_args()

    migrator = ZeroCopyMigrator(args.lib_rs)

    if args.analyze:
        migrator.analyze()
    elif args.generate:
        migrator.generate_batch(args.generate, args.output)
    else:
        print("请使用 --analyze 或 --generate 参数")
        parser.print_help()


if __name__ == '__main__':
    main()
