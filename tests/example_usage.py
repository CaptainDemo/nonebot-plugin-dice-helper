#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试使用示例

演示如何编写和运行简单的骰子相关测试
"""

import sys
from pathlib import Path
import importlib.util
import random

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))


def example_basic_dice_roll():
    """示例：基本的骰子投掷测试"""
    print("示例 1: 基本的骰子投掷")
    print("-" * 40)

    # 直接导入 dice_roller 模块以避免触发 NoneBot 初始化
    spec = importlib.util.spec_from_file_location(
        "dice_roller",
        project_root / "src" / "nonebot_plugin_dice_helper" / "dice_roller.py"
    )
    dice_roller = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dice_roller)

    roll_numeric_dice = dice_roller.roll_numeric_dice

    # 投掷一个 d6 骰子
    results, total = roll_numeric_dice(1, 6)

    print(f"投掷 d6: 结果 = {results[0]}, 总和 = {total}")
    assert 1 <= total <= 6, "骰子结果应该在 1 到 6 之间"
    print("[OK] 测试通过\n")


def example_parse_dice_args():
    """示例：解析骰子参数"""
    print("示例 2: 解析骰子参数")
    print("-" * 40)

    # 直接导入 dice_roller 模块
    spec = importlib.util.spec_from_file_location(
        "dice_roller",
        project_root / "src" / "nonebot_plugin_dice_helper" / "dice_roller.py"
    )
    dice_roller = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dice_roller)

    parse_roll_args = dice_roller.parse_roll_args

    # 测试示例
    test_cases = [
        ["d6"],
        ["3d6"],
        ["2d6", "3命中骰", "d4"],
    ]

    for case in test_cases:
        result = parse_roll_args(case)
        print(f"输入: {case}")
        print(f"输出: {result}")
        print("[OK] 解析成功\n")


def example_custom_dice():
    """示例：自定义骰子管理"""
    print("示例 3: 自定义骰子管理")
    print("-" * 40)

    # 直接导入 dice_roller 模块
    spec = importlib.util.spec_from_file_location(
        "dice_roller",
        project_root / "src" / "nonebot_plugin_dice_helper" / "dice_roller.py"
    )
    dice_roller = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dice_roller)

    roll_custom_dice = dice_roller.roll_custom_dice

    # 定义自定义骰子面
    faces = [["命中"], ["未命中"]]

    # 投掷自定义骰子
    results, total, counter = roll_custom_dice(5, faces)

    print(f"投掷 5 次 '命中骰': {results}")
    print(f"标记统计: {counter}")
    print("[OK] 操作成功\n")


def example_format_results():
    """示例：格式化骰子结果"""
    print("示例 4: 格式化骰子结果")
    print("-" * 40)

    # 直接导入 dice_roller 模块
    spec = importlib.util.spec_from_file_location(
        "dice_roller",
        project_root / "src" / "nonebot_plugin_dice_helper" / "dice_roller.py"
    )
    dice_roller = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dice_roller)

    format_dice_results = dice_roller.format_dice_results

    # 模拟骰子结果
    dice_results = {
        "d6": ["3", "5", "2"],
        "命中骰": ["命中", "未命中"]
    }

    num_sum = 10
    custom_counter = {"命中": 1, "未命中": 1}

    result = format_dice_results(dice_results, num_sum, custom_counter)
    print(result)
    print("[OK] 格式化完成\n")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("NoneBot Dice Helper 测试示例")
    print("=" * 50)
    print()

    try:
        example_basic_dice_roll()
        example_parse_dice_args()
        example_custom_dice()
        example_format_results()

        print("=" * 50)
        print("所有示例运行成功！")
        print("=" * 50)

    except AssertionError as e:
        print(f"[FAIL] 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
