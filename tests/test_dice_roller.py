"""
骰子投掷逻辑模块测试

测试 dice_roller 模块的函数：
- parse_roll_args: 解析骰子投掷参数
- roll_numeric_dice: 投掷数字骰子
- roll_custom_dice: 投掷自定义骰子
- format_dice_results: 格式化骰子结果
"""

import sys
import random
import importlib.util
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

# 直接导入 dice_roller 模块以避免触发 NoneBot 初始化
spec = importlib.util.spec_from_file_location(
    "dice_roller",
    project_root / "src" / "nonebot_plugin_dice_helper" / "dice_roller.py"
)
dice_roller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dice_roller)

parse_roll_args = dice_roller.parse_roll_args
roll_numeric_dice = dice_roller.roll_numeric_dice
roll_custom_dice = dice_roller.roll_custom_dice
format_dice_results = dice_roller.format_dice_results


# =====================
# parse_roll_args 测试
# =====================

def test_parse_roll_args_empty_list():
    """测试空列表"""
    result = parse_roll_args([])
    assert result == []


def test_parse_roll_args_single_dice_without_count():
    """测试单个骰子不指定数量"""
    result = parse_roll_args(["d6"])
    assert result == [(1, "d6")]


def test_parse_roll_args_single_dice_with_count():
    """测试单个骰子指定数量"""
    result = parse_roll_args(["3d6"])
    assert result == [(3, "d6")]


def test_parse_roll_args_multiple_dice():
    """测试多个骰子"""
    result = parse_roll_args(["2d6", "3命中骰", "d4"])
    assert result == [(2, "d6"), (3, "命中骰"), (1, "d4")]


def test_parse_roll_args_whitespace_handling():
    """测试空白字符处理"""
    result = parse_roll_args(["  2d6  ", "  命中骰  "])
    assert result == [(2, "d6"), (1, "命中骰")]


def test_parse_roll_args_empty_parts():
    """测试空部分"""
    result = parse_roll_args(["", "  ", "d6", ""])
    assert result == [(1, "d6")]


def test_parse_roll_args_large_count():
    """测试大数量"""
    result = parse_roll_args(["100d20"])
    assert result == [(100, "d20")]


def test_parse_roll_args_complex_dice_name():
    """测试复杂骰子名称"""
    result = parse_roll_args(["2命运骰", "3特殊_骰子"])
    assert result == [(2, "命运骰"), (3, "特殊_骰子")]


# =====================
# roll_numeric_dice 测试
# =====================

def test_roll_numeric_dice_basic():
    """测试基本数字骰子投掷"""
    results, total = roll_numeric_dice(count=3, face=6)

    assert len(results) == 3
    assert 3 <= total <= 18  # 3 * 1 到 3 * 6
    for r in results:
        assert r in ["1", "2", "3", "4", "5", "6"]


def test_roll_numeric_dice_single():
    """测试单个骰子投掷"""
    results, total = roll_numeric_dice(count=1, face=20)

    assert len(results) == 1
    assert 1 <= total <= 20
    assert str(total) == results[0]


def test_roll_numeric_dice_zero_count():
    """测试零次投掷"""
    results, total = roll_numeric_dice(count=0, face=6)

    assert len(results) == 0
    assert total == 0


def test_roll_numeric_dice_large_count():
    """测试大量投掷"""
    count = 100
    face = 10
    results, total = roll_numeric_dice(count=count, face=face)

    assert len(results) == count
    assert count <= total <= count * face


def test_roll_numeric_dice_d4():
    """测试 d4 骰子"""
    results, total = roll_numeric_dice(count=5, face=4)

    assert len(results) == 5
    assert 5 <= total <= 20
    for r in results:
        assert r in ["1", "2", "3", "4"]


def test_roll_numeric_dice_d20():
    """测试 d20 骰子"""
    results, total = roll_numeric_dice(count=3, face=20)

    assert len(results) == 3
    assert 3 <= total <= 60
    for r in results:
        assert r in [str(i) for i in range(1, 21)]


# =====================
# roll_custom_dice 测试
# =====================

def test_roll_custom_dice_basic():
    """测试基本自定义骰子投掷"""
    faces = [["命中"], ["未命中"]]
    results, total, counter = roll_custom_dice(count=3, faces=faces)

    assert len(results) == 3
    assert total == 0
    assert "命中" in counter or "未命中" in counter


def test_roll_custom_dice_with_numbers():
    """测试带数字的自定义骰子"""
    faces = [["命中", "1"], ["命中", "2"], ["未命中"]]
    results, total, counter = roll_custom_dice(count=5, faces=faces)

    assert len(results) == 5
    assert total >= 0
    assert "命中" in counter or "未命中" in counter


def test_roll_custom_dice_zero_count():
    """测试零次投掷"""
    faces = [["命中"], ["未命中"]]
    results, total, counter = roll_custom_dice(count=0, faces=faces)

    assert len(results) == 0
    assert total == 0
    assert len(counter) == 0


def test_roll_custom_dice_single():
    """测试单次投掷"""
    faces = [["成功"], ["失败"]]
    results, total, counter = roll_custom_dice(count=1, faces=faces)

    assert len(results) == 1
    assert total == 0
    assert len(counter) == 1


def test_roll_custom_dice_multi_item_faces():
    """测试多标记骰子面"""
    faces = [["伤害", "1"], ["伤害", "2"], ["暴击", "3"]]
    results, total, counter = roll_custom_dice(count=10, faces=faces)

    assert len(results) == 10
    assert total >= 0
    assert "|" in results[0]  # 结果应包含分隔符


def test_roll_custom_dice_numeric_only():
    """测试仅数字的骰子"""
    faces = [["1"], ["2"], ["3"]]
    results, total, counter = roll_custom_dice(count=5, faces=faces)

    assert len(results) == 5
    assert 5 <= total <= 15
    assert len(counter) == 0  # 没有非数字标记


def test_roll_custom_dice_text_only():
    """测试仅文本的骰子"""
    faces = [["成功"], ["失败"]]
    results, total, counter = roll_custom_dice(count=10, faces=faces)

    assert len(results) == 10
    assert total == 0
    assert len(counter) == 2  # 应该有成功和失败两个计数
    assert counter["成功"] + counter["失败"] == 10


# =====================
# format_dice_results 测试
# =====================

def test_format_dice_results_numeric_only():
    """测试仅数字骰子的结果格式化"""
    dice_results = {
        "d6": ["3", "5", "2"],
        "d4": ["1", "4"]
    }
    num_sum = 15
    custom_counter = {}

    result = format_dice_results(dice_results, num_sum, custom_counter)

    assert "骰子结果" in result
    assert "d6 ×3：3，5，2" in result
    assert "d4 ×2：1，4" in result
    assert "合计15" in result


def test_format_dice_results_custom_only():
    """测试仅自定义骰子的结果格式化"""
    dice_results = {
        "命中骰": ["命中", "未命中", "命中"],
        "命运骰": ["成功", "失败"]
    }
    num_sum = 0
    custom_counter = {"命中": 2, "未命中": 1, "成功": 1, "失败": 1}

    result = format_dice_results(dice_results, num_sum, custom_counter)

    assert "骰子结果" in result
    assert "命中骰 ×3：命中，未命中，命中" in result
    assert "命运骰 ×2：成功，失败" in result
    assert "合计" in result
    assert "2命中" in result
    assert "1未命中" in result


def test_format_dice_results_mixed():
    """测试混合骰子的结果格式化"""
    dice_results = {
        "d6": ["3", "5"],
        "命中骰": ["命中", "未命中"]
    }
    num_sum = 8
    custom_counter = {"命中": 1, "未命中": 1}

    result = format_dice_results(dice_results, num_sum, custom_counter)

    assert "骰子结果" in result
    assert "d6 ×2：3，5" in result
    assert "命中骰 ×2：命中，未命中" in result
    assert "合计8，1命中，1未命中" in result


def test_format_dice_results_empty():
    """测试空结果的格式化"""
    dice_results = {}
    num_sum = 0
    custom_counter = {}

    result = format_dice_results(dice_results, num_sum, custom_counter)

    assert "骰子结果" in result
    assert "合计无" in result


def test_format_dice_results_multi_item_face():
    """测试多标记骰子面的结果格式化"""
    dice_results = {
        "伤害骰": ["3|命中", "1|暴击", "2|命中"]
    }
    num_sum = 6
    custom_counter = {"命中": 2, "暴击": 1}

    result = format_dice_results(dice_results, num_sum, custom_counter)

    assert "骰子结果" in result
    assert "伤害骰 ×3：3|命中，1|暴击，2|命中" in result
    assert "合计6，2命中，1暴击" in result


def test_format_dice_results_custom_order():
    """测试自定义标记的顺序（字典顺序）"""
    dice_results = {
        "测试骰": ["结果1", "结果2"]
    }
    num_sum = 0
    custom_counter = {"暴击": 1, "命中": 2, "未命中": 3}

    result = format_dice_results(dice_results, num_sum, custom_counter)

    assert "合计" in result
    # 所有标记都应该存在
    assert "1暴击" in result
    assert "2命中" in result
    assert "3未命中" in result
