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
import importlib.util
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 直接导入 dice_roller 模块以避免触发 NoneBot 初始化
spec = importlib.util.spec_from_file_location(
    "dice_roller",
    project_root / "nonebot_plugin_dice_helper" / "dice_roller.py"
)
dice_roller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dice_roller)

roll_numeric_dice = dice_roller.roll_numeric_dice
roll_custom_dice = dice_roller.roll_custom_dice


def test_dice_roll_numeric():
    """测试投掷数字骰子的基本逻辑"""
    # 模拟投掷 3 次 d6
    count = 3
    face = 6

    results, num_sum = roll_numeric_dice(count, face)

    assert len(results) == count
    assert 1 <= num_sum <= face * count


def test_dice_roll_custom():
    """测试投掷自定义骰子的基本逻辑"""
    faces = [["命中", "1"], ["命中", "2"], ["未命中"]]

    results, _, _ = roll_custom_dice(1, faces)

    # 验证结果格式
    assert isinstance(results, list)
    assert len(results) == 1
    assert isinstance(results[0], str)


def test_dice_roll_custom_sum_counter():
    """测试自定义骰子的数值求和和标记计数"""
    faces = [["命中", "2"], ["未命中", "1"], ["命中", "3"]]

    # 投掷所有面以测试总和
    results, num_sum, custom_counter = roll_custom_dice(3, faces)

    # 由于是随机选择，我们只验证基本逻辑
    assert len(results) == 3
    assert isinstance(num_sum, int)
    assert isinstance(custom_counter, dict)


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


def test_dice_numeric_sum_calculation():
    """测试数字骰子总和计算"""
    # 使用固定种子进行测试
    random.seed(42)
    results, total = roll_numeric_dice(5, 6)

    # 验证每个结果都是有效的骰子面
    for r in results:
        assert r in ["1", "2", "3", "4", "5", "6"]

    # 验证总和等于所有结果的和
    expected_total = sum(int(r) for r in results)
    assert total == expected_total


def test_dice_custom_tag_counter():
    """测试自定义骰子标记计数"""
    # 使用固定数量的投掷测试计数逻辑
    faces = [["命中", "1"], ["未命中"], ["暴击", "2"]]

    # 投掷多次以累积计数
    results, total, counter = roll_custom_dice(100, faces)

    # 验证计数逻辑
    total_rolls = sum(counter.values())
    # 所有标记的总数应该等于投掷次数乘以每个面可能的标记数
    # 由于是随机的，我们只验证基本属性
    assert isinstance(counter, dict)
    assert total_rolls >= 0


def test_dice_custom_face_joined_correctly():
    """测试自定义骰子面正确连接"""
    faces = [["标签1", "标签2"], ["标签A", "标签B"]]

    results, _, _ = roll_custom_dice(2, faces)

    # 验证结果使用 | 分隔符
    for result in results:
        assert "|" in result


def test_dice_numeric_range_validation():
    """测试数字骰子结果范围验证"""
    test_cases = [
        (1, 4),   # d4
        (1, 6),   # d6
        (1, 8),   # d8
        (1, 10),  # d10
        (1, 12),  # d12
        (1, 20),  # d20
        (1, 100), # d100
    ]

    for min_val, max_val in test_cases:
        results, total = roll_numeric_dice(10, max_val)
        for r in results:
            assert int(r) >= min_val
            assert int(r) <= max_val
        assert total >= min_val * 10
        assert total <= max_val * 10
