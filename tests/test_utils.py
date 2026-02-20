"""
测试工具函数模块

注意: 此模块中的测试需要 NoneBot 运行时环境。
如需单独运行，请在完整的 NoneBot 环境中运行测试。

以下功能已移至 test_dice_roller.py:
- parse_roll_args 测试
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_note():
    """
    注意: utils 模块中的函数依赖 NoneBot 运行时环境
    如需测试 dice_admin_permission 和 maybe_apply_prefix_variance，
    请在完整的 NoneBot 环境中运行。

    parse_roll_args 函数已移至 dice_roller 模块，
    其测试请在 test_dice_roller.py 中查看。
    """
    assert True
