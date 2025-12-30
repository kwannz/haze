#!/usr/bin/env python3
"""
零拷贝自动集成工具

功能:
1. 自动重命名原函数为 _legacy
2. 自动插入零拷贝新版本
3. 自动添加模块注册
4. 完整备份和安全回滚

使用示例:
    python scripts/auto_integrate_zero_copy.py --pattern 1to1 --batch 10 --dry-run
    python scripts/auto_integrate_zero_copy.py --pattern 1to1 --all --execute
"""

import re
import argparse
import shutil
from pathlib import Path
from typing import List, Tuple
from datetime import datetime


class AutoIntegrator:
    """零拷贝自动集成器"""

    def __init__(self, lib_rs_path: str, migration_output_dir: str):
        self.lib_rs_path = Path(lib_rs_path)
        self.migration_output_dir = Path(migration_output_dir)
        self.backup_path = None
        self.lib_rs_content = ""
        self.modifications = []

    def backup_lib_rs(self) -> Path:
        """创建 lib.rs 备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.lib_rs_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)

        backup_path = backup_dir / f"lib.rs.backup_{timestamp}"
        shutil.copy2(self.lib_rs_path, backup_path)

        self.backup_path = backup_path
        print(f"✅ 备份已创建: {backup_path}")
        return backup_path

    def load_lib_rs(self):
        """加载 lib.rs 内容"""
        self.lib_rs_content = self.lib_rs_path.read_text(encoding='utf-8')
        print(f"✅ 加载 lib.rs: {len(self.lib_rs_content)} 字符")

    def find_function_location(self, func_name: str) -> Tuple[int, int]:
        """
        查找函数在 lib.rs 中的位置

        Returns:
            (start_pos, end_pos) - 函数的起始和结束位置
        """
        # 匹配从 #[cfg 或 #[pyfunction 到函数结束的 }
        pattern = rf'(#\[cfg\(feature = "python"\)\]\s+)?#\[pyfunction[^\]]*\].*?^fn {func_name}\([^{{]*\{{.*?^\}}'

        match = re.search(pattern, self.lib_rs_content, re.MULTILINE | re.DOTALL)

        if match:
            return match.start(), match.end()
        else:
            return -1, -1

    def rename_to_legacy(self, func_name: str) -> bool:
        """
        重命名函数为 _legacy 版本

        步骤:
        1. 找到函数定义
        2. 修改 #[pyfunction] 为 #[pyfunction(name = "func_name_legacy")]
        3. 修改函数名为 func_name_legacy
        4. 添加 " - Legacy version" 到文档注释
        """
        start_pos, end_pos = self.find_function_location(func_name)

        if start_pos == -1:
            print(f"❌ 未找到函数: {func_name}")
            return False

        func_block = self.lib_rs_content[start_pos:end_pos]

        # 替换 #[pyfunction] 为 #[pyfunction(name = "func_name_legacy")]
        # 需要处理三种情况:
        # 1. #[pyfunction] - 无参数
        # 2. #[pyfunction(...)] - 有参数但无 name
        # 3. #[pyfunction(..., name = "xxx", ...)] - 已有 name 参数

        # 检查是否有参数
        pyfunction_match = re.search(r'#\[pyfunction(\([^)]*\))?\]', func_block)
        if not pyfunction_match:
            print(f"⚠️  未找到 #[pyfunction] 装饰器: {func_name}")
            return False

        old_decorator = pyfunction_match.group(0)

        # 情况1: #[pyfunction] 无参数
        if old_decorator == '#[pyfunction]':
            new_decorator = f'#[pyfunction(name = "{func_name}_legacy")]'
        else:
            # 有参数的情况 - 检查是否已有 name 参数
            params_content = pyfunction_match.group(1)[1:-1]  # 去掉括号

            if re.search(r'\bname\s*=', params_content):
                # 情况3: 已有 name 参数 - 替换它
                new_params = re.sub(
                    r'\bname\s*=\s*"[^"]*"',
                    f'name = "{func_name}_legacy"',
                    params_content
                )
                new_decorator = f'#[pyfunction({new_params})]'
            else:
                # 情况2: 无 name 参数 - 添加到开头
                new_decorator = f'#[pyfunction(name = "{func_name}_legacy", {params_content})]'

        # 替换装饰器
        func_block = func_block.replace(old_decorator, new_decorator, 1)

        # 替换函数名
        func_block = re.sub(
            rf'^fn {func_name}\(',
            f'fn {func_name}_legacy(',
            func_block,
            flags=re.MULTILINE
        )

        # 添加 " - Legacy version" 到第一个 /// 注释
        func_block = re.sub(
            r'(^/// Calculate [^\n]+)',
            r'\1 - Legacy version',
            func_block,
            count=1,
            flags=re.MULTILINE
        )

        # 替换回内容
        self.lib_rs_content = (
            self.lib_rs_content[:start_pos] +
            func_block +
            self.lib_rs_content[end_pos:]
        )

        self.modifications.append(f"✓ 重命名 {func_name} → {func_name}_legacy")
        return True

    def insert_zero_copy_version(self, func_name: str) -> bool:
        """
        在 _legacy 函数后插入零拷贝版本

        步骤:
        1. 找到 _legacy 函数的结束位置
        2. 读取生成的零拷贝代码
        3. 插入到 _legacy 函数之后
        """
        legacy_name = f"{func_name}_legacy"
        start_pos, end_pos = self.find_function_location(legacy_name)

        if start_pos == -1:
            print(f"❌ 未找到 legacy 函数: {legacy_name}")
            return False

        # 读取生成的零拷贝代码
        zero_copy_file = self.migration_output_dir / f"{func_name}.rs"

        if not zero_copy_file.exists():
            print(f"❌ 未找到生成的代码: {zero_copy_file}")
            return False

        zero_copy_code = zero_copy_file.read_text(encoding='utf-8')

        # 插入零拷贝版本（在 legacy 函数之后，添加空行）
        insert_code = f"\n{zero_copy_code}\n"

        self.lib_rs_content = (
            self.lib_rs_content[:end_pos] +
            insert_code +
            self.lib_rs_content[end_pos:]
        )

        self.modifications.append(f"✓ 插入零拷贝版本: {func_name}")
        return True

    def add_module_registration(self, func_name: str) -> bool:
        """
        自动添加模块注册

        在现有的 m.add_function(wrap_pyfunction!(func_name, m)?)?; 之后
        添加 m.add_function(wrap_pyfunction!(func_name_legacy, m)?)?;
        """
        # 查找现有的注册行
        pattern = rf'(    m\.add_function\(wrap_pyfunction!\({func_name}, m\)\?\)\?\;)'

        match = re.search(pattern, self.lib_rs_content)

        if not match:
            print(f"⚠️  未找到现有注册: {func_name}")
            return False

        # 在该行后面插入 legacy 注册
        legacy_registration = f'\n    m.add_function(wrap_pyfunction!({func_name}_legacy, m)?)?;  // Legacy API for backward compatibility'

        insert_pos = match.end()

        self.lib_rs_content = (
            self.lib_rs_content[:insert_pos] +
            legacy_registration +
            self.lib_rs_content[insert_pos:]
        )

        self.modifications.append(f"✓ 添加模块注册: {func_name}_legacy")
        return True

    def migrate_function(self, func_name: str) -> bool:
        """
        完整迁移单个函数

        步骤:
        1. 重命名为 _legacy
        2. 插入零拷贝版本
        3. 添加模块注册
        """
        print(f"\n🔄 开始迁移: {func_name}")

        # Step 1: 重命名为 legacy
        if not self.rename_to_legacy(func_name):
            return False

        # Step 2: 插入零拷贝版本
        if not self.insert_zero_copy_version(func_name):
            return False

        # Step 3: 添加模块注册
        if not self.add_module_registration(func_name):
            # 注册失败不是致命错误（可能已经注册过）
            pass

        print(f"✅ 完成迁移: {func_name}")
        return True

    def save_lib_rs(self):
        """保存修改后的 lib.rs"""
        self.lib_rs_path.write_text(self.lib_rs_content, encoding='utf-8')
        print(f"\n✅ 已保存 lib.rs: {len(self.lib_rs_content)} 字符")

    def print_summary(self):
        """打印修改摘要"""
        print(f"\n{'='*60}")
        print(f"修改摘要 ({len(self.modifications)} 项)")
        print(f"{'='*60}")
        for mod in self.modifications:
            print(f"  {mod}")
        print(f"{'='*60}")

    def restore_backup(self):
        """从备份恢复"""
        if self.backup_path and self.backup_path.exists():
            shutil.copy2(self.backup_path, self.lib_rs_path)
            print(f"✅ 已从备份恢复: {self.backup_path}")
        else:
            print(f"❌ 备份不存在: {self.backup_path}")


def get_functions_to_migrate(pattern: str, batch_size: int = None) -> List[str]:
    """
    获取要迁移的函数列表

    Args:
        pattern: "1to1", "nto1", "1ton", "ntom"
        batch_size: 限制数量（None = 全部）
    """
    migration_output = Path("/Users/zhaoleon/Desktop/haze/haze/migration_output/test")

    if not migration_output.exists():
        print(f"❌ 迁移输出目录不存在: {migration_output}")
        return []

    # 获取所有生成的 .rs 文件
    rs_files = sorted(migration_output.glob("*.rs"))

    # 提取函数名（去掉 .rs 后缀）
    func_names = [f.stem for f in rs_files]

    # 排除已迁移的函数（Week 1）
    already_migrated = ["py_sma", "py_ema", "py_rsi", "py_macd", "py_atr", "py_wma"]
    func_names = [f for f in func_names if f not in already_migrated]

    if batch_size:
        func_names = func_names[:batch_size]

    return func_names


def main():
    parser = argparse.ArgumentParser(description='零拷贝自动集成工具')
    parser.add_argument('--pattern', default='1to1', choices=['1to1', 'nto1', '1ton', 'ntom'],
                        help='函数模式')
    parser.add_argument('--batch', type=int, default=None,
                        help='批量处理数量（None = 全部）')
    parser.add_argument('--all', action='store_true',
                        help='迁移所有函数')
    parser.add_argument('--functions-file', type=str, default=None,
                        help='从文件读取函数列表（每行一个函数名）')
    parser.add_argument('--dry-run', action='store_true',
                        help='仅显示将要执行的操作，不实际修改')
    parser.add_argument('--execute', action='store_true',
                        help='执行迁移（确认标志）')
    parser.add_argument('--restore', action='store_true',
                        help='从最新备份恢复')

    args = parser.parse_args()

    lib_rs_path = "/Users/zhaoleon/Desktop/haze/haze/rust/src/lib.rs"
    migration_output_dir = "/Users/zhaoleon/Desktop/haze/haze/migration_output/test"

    integrator = AutoIntegrator(lib_rs_path, migration_output_dir)

    # 恢复备份
    if args.restore:
        integrator.backup_path = max(
            Path(lib_rs_path).parent.glob("backups/lib.rs.backup_*"),
            key=lambda p: p.stat().st_mtime
        )
        integrator.restore_backup()
        return

    # 获取要迁移的函数列表
    if args.functions_file:
        # 从文件读取函数列表
        functions_file = Path(args.functions_file)
        if not functions_file.exists():
            print(f"❌ 函数列表文件不存在: {functions_file}")
            return

        with open(functions_file, 'r', encoding='utf-8') as f:
            func_names = [line.strip() for line in f if line.strip()]

        print(f"✅ 从文件读取 {len(func_names)} 个函数: {functions_file}")
    elif args.all:
        func_names = get_functions_to_migrate(args.pattern, batch_size=None)
    else:
        func_names = get_functions_to_migrate(args.pattern, batch_size=args.batch or 10)

    if not func_names:
        print("❌ 没有找到要迁移的函数")
        return

    print(f"\n📋 计划迁移 {len(func_names)} 个函数:")
    for i, name in enumerate(func_names, 1):
        print(f"  {i}. {name}")

    if args.dry_run:
        print(f"\n🔍 dry-run 模式: 不会实际修改文件")
        return

    if not args.execute:
        print(f"\n⚠️  请添加 --execute 标志确认执行")
        return

    # 执行迁移
    print(f"\n{'='*60}")
    print(f"开始执行批量迁移")
    print(f"{'='*60}")

    # 创建备份
    integrator.backup_lib_rs()

    # 加载 lib.rs
    integrator.load_lib_rs()

    # 批量迁移
    success_count = 0
    failed_funcs = []

    for func_name in func_names:
        try:
            if integrator.migrate_function(func_name):
                success_count += 1
            else:
                failed_funcs.append(func_name)
        except Exception as e:
            print(f"❌ 迁移失败: {func_name} - {e}")
            failed_funcs.append(func_name)

    # 保存 lib.rs
    integrator.save_lib_rs()

    # 打印摘要
    integrator.print_summary()

    print(f"\n{'='*60}")
    print(f"迁移结果")
    print(f"{'='*60}")
    print(f"✅ 成功: {success_count}/{len(func_names)}")
    print(f"❌ 失败: {len(failed_funcs)}/{len(func_names)}")

    if failed_funcs:
        print(f"\n失败的函数:")
        for name in failed_funcs:
            print(f"  - {name}")

    print(f"\n💾 备份路径: {integrator.backup_path}")
    print(f"如需回滚: python scripts/auto_integrate_zero_copy.py --restore")


if __name__ == '__main__':
    main()
