#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试使用示例

演示如何编写和运行简单的骰子相关测试
"""

import sys
import random
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def example_basic_dice_roll():
    """示例：基本的骰子投掷测试"""
    print("示例 1: 基本的骰子投掷")
    print("-" * 40)

    # 投掷一个 d6 骰子
    dice = "d6"
    face = int(dice[1:])
    result = random.randint(1, face)

    print(f"投掷 {dice}: 结果 = {result}")
    assert 1 <= result <= 6, "骰子结果应该在 1 到 6 之间"
    print("[OK] 测试通过\n")


def example_parse_dice_args():
    """示例：解析骰子参数"""
    print("示例 2: 解析骰子参数")
    print("-" * 40)

    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
        """将参数解析为 [(数量, 骰子名), ...]"""
        result: List[Tuple[int, str]] = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            m = re.fullmatch(r"(\d+)(.+)", part)
            if m:
                count = int(m.group(1))
                dice = m.group(2)
                result.append((count, dice))
                continue
            result.append((1, part))
        return result

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

    class SimpleDiceManager:
        def __init__(self):
            self.dice = {}

        def add_dice(self, name: str, faces: list[list[str]]) -> bool:
            if name in self.dice:
                return False
            self.dice[name] = faces
            return True

        def roll_dice(self, name: str) -> str:
            if name not in self.dice:
                raise ValueError(f"骰子 '{name}' 不存在")
            face = random.choice(self.dice[name])
            return "|".join(face)

    manager = SimpleDiceManager()

    # 添加自定义骰子
    success = manager.add_dice("命中骰", [["命中"], ["未命中"]])
    print(f"添加 '命中骰': {'成功' if success else '失败'}")

    # 投掷骰子
    result = manager.roll_dice("命中骰")
    print(f"投掷 '命中骰': {result}")
    print("✓ 操作成功\n")


def example_format_results():
    """示例：格式化骰子结果"""
    print("示例 4: 格式化骰子结果")
    print("-" * 40)

    # 模拟骰子结果
    dice_results = {
        "d6": ["3", "5", "2"],
        "命中骰": ["命中", "未命中"]
    }

    num_sum = 0
    custom_counter = {}

    for dice, values in dice_results.items():
        if dice.startswith("d"):
            # 数字骰子
            for v in values:
                num_sum += int(v)
        else:
            # 自定义骰子
            for v in values:
                if not v.isdigit():
                    custom_counter[v] = custom_counter.get(v, 0) + 1

    # 构建结果文本
    lines = ["骰子结果"]
    for dice, values in dice_results.items():
        lines.append(f"{dice} ×{len(values)}：" + "，".join(values))

    total_parts = []
    if num_sum:
        total_parts.append(str(num_sum))
    for k, v in custom_counter.items():
        total_parts.append(f"{v}{k}")

    lines.append("合计" + ("，".join(total_parts) if total_parts else "无"))

    result = "\n".join(lines)
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
        sys.exit(1)


if __name__ == "__main__":
    main()
