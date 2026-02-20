"""骰子投掷逻辑模块"""
import random
import re
from typing import Tuple, List, Dict


def roll_numeric_dice(count: int, face: int) -> Tuple[List[str], int]:
    """
    投掷数字骰子

    Args:
        count: 投掷次数
        face: 骰子面数

    Returns:
        (结果列表, 总和)
    """
    results = []
    total = 0
    for _ in range(count):
        r = random.randint(1, face)
        results.append(str(r))
        total += r
    return results, total


def roll_custom_dice(
    count: int, faces: List[List[str]]
) -> Tuple[List[str], int, Dict[str, int]]:
    """
    投掷自定义骰子

    Args:
        count: 投掷次数
        faces: 骰子面列表

    Returns:
        (结果列表, 数字总和, 标记计数)
    """
    results = []
    total = 0
    counter: Dict[str, int] = {}

    for _ in range(count):
        face = random.choice(faces)
        text_face = "|".join(face)
        results.append(text_face)

        for item in face:
            if item.isdigit():
                total += int(item)
            else:
                counter[item] = counter.get(item, 0) + 1

    return results, total, counter


def format_dice_results(
    dice_results: Dict[str, List[str]], num_sum: int, custom_counter: Dict[str, int]
) -> str:
    """
    格式化骰子结果

    Args:
        dice_results: 各骰子的结果
        num_sum: 数字总和
        custom_counter: 标记计数

    Returns:
        格式化的结果字符串
    """
    lines = ["骰子结果"]

    for dice, values in dice_results.items():
        lines.append(f"{dice} ×{len(values)}：" + "，".join(values))

    total_parts = []
    if num_sum:
        total_parts.append(str(num_sum))
    for k, v in custom_counter.items():
        total_parts.append(f"{v}{k}")

    lines.append("合计" + ("，".join(total_parts) if total_parts else "无"))

    return "\n".join(lines)


def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
    """
    将参数解析为 [(数量, 骰子名), ...]

    支持格式：
      - 2d6
      - d6
      - 3命中骰
      - 命中骰

    Args:
        parts: 参数列表

    Returns:
        [(数量, 骰子名), ...]
    """
    result: List[Tuple[int, str]] = []

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 尝试匹配"数字 + 骰子名"
        m = re.fullmatch(r"(\d+)(.+)", part)
        if m:
            count = int(m.group(1))
            dice = m.group(2)
            result.append((count, dice))
            continue

        # 没有数字，默认 1
        result.append((1, part))

    return result
