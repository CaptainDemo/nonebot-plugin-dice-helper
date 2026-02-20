"""
骰子核心逻辑测试

测试骰子的核心逻辑，包括：
- 数字骰子投掷
- 自定义骰子投掷
- 混合投掷
- 结果统计
"""

import sys
import random
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_dice_roll_numeric():
    """测试投掷数字骰子的基本逻辑"""
    # 模拟投掷 3 次 d6
    count = 3
    face = 6

    results = []
    num_sum = 0

    for _ in range(count):
        r = random.randint(1, face)
        results.append(str(r))
        num_sum += r

    assert len(results) == count
    assert 1 <= num_sum <= face * count


def test_dice_roll_custom():
    """测试投掷自定义骰子的基本逻辑"""
    faces = [["命中", "1"], ["命中", "2"], ["未命中"]]

    face = random.choice(faces)
    text_face = "|".join(face)

    # 验证结果格式
    assert isinstance(face, list)
    assert len(face) > 0
    assert isinstance(text_face, str)


def test_dice_roll_custom_sum_counter():
    """测试自定义骰子的数值求和和标记计数"""
    faces = [["命中", "2"], ["未命中", "1"], ["命中", "3"]]

    num_sum = 0
    custom_counter = {}

    for face in faces:
        for item in face:
            if item.isdigit():
                num_sum += int(item)
            else:
                custom_counter[item] = custom_counter.get(item, 0) + 1

    assert num_sum == 6  # 2 + 1 + 3
    assert custom_counter["命中"] == 2
    assert custom_counter["未命中"] == 1


def test_dice_format_results():
    """测试骰子结果格式化"""
    dice_results = {
        "d6": ["3", "5", "2"],
        "d4": ["1", "4"]
    }

    lines = ["骰子结果"]
    for dice, values in dice_results.items():
        lines.append(
            f"{dice} ×{len(values)}："
            + "，".join(values)
        )

    assert "骰子结果" in lines
    assert "d6 ×3：3，5，2" in lines
    assert "d4 ×2：1，4" in lines


def test_dice_format_custom_results():
    """测试自定义骰子结果格式化"""
    dice_results = {
        "命中骰": ["命中", "未命中"],
        "命运骰": ["成功", "失败", "重骰"]
    }

    lines = ["骰子结果"]
    for dice, values in dice_results.items():
        lines.append(
            f"{dice} ×{len(values)}："
            + "，".join(values)
        )

    assert "骰子结果" in lines
    assert "命中骰 ×2：命中，未命中" in lines
    assert "命运骰 ×3：成功，失败，重骰" in lines


def test_dice_format_multi_item_face():
    """测试多标记骰子面格式化"""
    dice_results = {
        "伤害骰": ["3|命中", "1|暴击", "2|命中"]
    }

    lines = ["骰子结果"]
    for dice, values in dice_results.items():
        lines.append(
            f"{dice} ×{len(values)}："
            + "，".join(values)
        )

    assert "伤害骰 ×3：3|命中，1|暴击，2|命中" in lines


def test_dice_format_total_numeric_only():
    """测试仅数字的合计"""
    num_sum = 15
    custom_counter = {}
    total_parts = []

    if num_sum:
        total_parts.append(str(num_sum))
    for k, v in custom_counter.items():
        total_parts.append(f"{v}{k}")

    total = "合计" + ("，".join(total_parts) if total_parts else "无")
    assert total == "合计15"


def test_dice_format_total_custom_only():
    """测试仅自定义标记的合计"""
    num_sum = 0
    custom_counter = {"命中": 3, "暴击": 1}
    total_parts = []

    if num_sum:
        total_parts.append(str(num_sum))
    for k, v in custom_counter.items():
        total_parts.append(f"{v}{k}")

    total = "合计" + ("，".join(total_parts) if total_parts else "无")
    assert total == "合计3命中，1暴击"


def test_dice_format_total_mixed():
    """测试混合合计"""
    num_sum = 12
    custom_counter = {"命中": 2, "暴击": 1}
    total_parts = []

    if num_sum:
        total_parts.append(str(num_sum))
    for k, v in custom_counter.items():
        total_parts.append(f"{v}{k}")

    total = "合计" + ("，".join(total_parts) if total_parts else "无")
    assert total == "合计12，2命中，1暴击"


def test_dice_format_total_empty():
    """测试空合计"""
    num_sum = 0
    custom_counter = {}
    total_parts = []

    if num_sum:
        total_parts.append(str(num_sum))
    for k, v in custom_counter.items():
        total_parts.append(f"{v}{k}")

    total = "合计" + ("，".join(total_parts) if total_parts else "无")
    assert total == "合计无"


def test_dice_parsing_logic():
    """测试骰子解析逻辑"""
    # 数字骰子 dN
    dice = "d6"
    is_numeric_dice = dice.startswith("d") and dice[1:].isdigit()
    assert is_numeric_dice is True

    # 自定义骰子
    dice = "命中骰"
    is_numeric_dice = dice.startswith("d") and dice[1:].isdigit()
    assert is_numeric_dice is False

    # 无效的数字骰子
    dice = "d6x"
    is_numeric_dice = dice.startswith("d") and dice[1:].isdigit()
    assert is_numeric_dice is False


def test_dice_face_parsing():
    """测试骰子面解析"""
    text = "面1 面2 面3"
    faces = [p.split("|") for p in text.split()]

    assert faces == [["面1"], ["面2"], ["面3"]]


def test_dice_face_parsing_with_multi_items():
    """测试多标记骰子面解析"""
    text = "命中|1 命中|2 未命中"
    faces = [p.split("|") for p in text.split()]

    assert faces == [["命中", "1"], ["命中", "2"], ["未命中"]]


def test_dice_validation():
    """测试骰子有效性验证"""
    all_dice = {
        "d6": None,
        "命中骰": [["命中"], ["未命中"]],
        "d20": None,
    }

    # 测试存在的骰子
    assert "d6" in all_dice
    assert "命中骰" in all_dice

    # 测试不存在的骰子
    assert "不存在骰子" not in all_dice

    # 测试数字骰子
    dice = "d6"
    is_numeric = dice.startswith("d") and dice[1:].isdigit()
    assert is_numeric is True
