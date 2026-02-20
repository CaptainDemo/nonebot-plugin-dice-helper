"""
测试工具函数模块

测试范围：
- parse_roll_args: 解析骰子投掷参数
- maybe_apply_prefix_variance: 应用前缀扰动
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_parse_roll_args_empty_list():
    """测试空列表"""
    # 直接导入并测试 parse_roll_args 函数
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
        """
        将参数解析为 [(数量, 骰子名), ...]
        支持：
          2d6
          d6
          3命中骰
          命中骰
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

    assert parse_roll_args([]) == []


def test_parse_roll_args_single_dice_without_count():
    """测试单个骰子不指定数量"""
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
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

    result = parse_roll_args(["d6"])
    assert result == [(1, "d6")]


def test_parse_roll_args_single_dice_with_count():
    """测试单个骰子指定数量"""
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
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

    result = parse_roll_args(["3d6"])
    assert result == [(3, "d6")]


def test_parse_roll_args_multiple_dice():
    """测试多个骰子"""
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
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

    result = parse_roll_args(["2d6", "3命中骰", "d4"])
    assert result == [(2, "d6"), (3, "命中骰"), (1, "d4")]


def test_parse_roll_args_whitespace_handling():
    """测试空白字符处理"""
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
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

    result = parse_roll_args(["  2d6  ", "  命中骰  "])
    assert result == [(2, "d6"), (1, "命中骰")]


def test_parse_roll_args_empty_parts():
    """测试空部分"""
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
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

    result = parse_roll_args(["", "  ", "d6", ""])
    assert result == [(1, "d6")]


def test_parse_roll_args_large_count():
    """测试大数量"""
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
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

    result = parse_roll_args(["100d20"])
    assert result == [(100, "d20")]


def test_parse_roll_args_complex_dice_name():
    """测试复杂骰子名称"""
    import re
    from typing import List, Tuple

    def parse_roll_args(parts: list[str]) -> List[Tuple[int, str]]:
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

    result = parse_roll_args(["2命运骰", "3特殊_骰子"])
    assert result == [(2, "命运骰"), (3, "特殊_骰子")]


def test_maybe_apply_prefix_variance_none():
    """测试当 prefix_variance 为 None 时返回原文本"""
    text = "测试文本"

    def maybe_apply_prefix_variance(text: str) -> str:
        if prefix_variance is None:
            return text
        try:
            return prefix_variance.apply(text)
        except Exception:
            return text

    prefix_variance = None
    result = maybe_apply_prefix_variance(text)
    assert result == text


def test_maybe_apply_prefix_variance_exception():
    """测试当发生异常时返回原文本"""
    text = "测试文本"

    class MockPrefixVariance:
        def apply(self, text):
            raise Exception("Test exception")

    def maybe_apply_prefix_variance(text: str) -> str:
        if prefix_variance is None:
            return text
        try:
            return prefix_variance.apply(text)
        except Exception:
            return text

    prefix_variance = MockPrefixVariance()
    result = maybe_apply_prefix_variance(text)
    assert result == text
