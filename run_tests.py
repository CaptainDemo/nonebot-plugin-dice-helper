#!/usr/bin/env python3
"""
本地测试运行脚本

使用方法：
    python run_tests.py              # 运行所有测试
    python run_tests.py -v          # 详细输出
    python run_tests.py test_utils  # 运行特定模块测试
    python run_tests.py -k roll     # 运行名称包含 roll 的测试
    python run_tests.py --cov       # 生成覆盖率报告
"""

import sys
import subprocess
from pathlib import Path


def main():
    """主函数"""
    # 切换到项目根目录
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root / "src"))
    sys.path.insert(0, str(project_root))

    # 默认参数
    pytest_args = [
        sys.executable,
        "-m",
        "pytest",
        "-v",  # 详细输出
        "--tb=short",  # 简短的回溯信息
        "--color=yes",  # 彩色输出
        "tests/",  # 测试目录
    ]

    # 添加用户传递的参数
    if len(sys.argv) > 1:
        user_args = sys.argv[1:]
        # 如果用户指定了特定的测试文件或参数，替换默认的 "tests/"
        if user_args[0] in ["test_utils", "test_dice_logic", "test_dice_management"]:
            # 补全文件名
            user_args[0] = f"tests/{user_args[0]}.py"
        pytest_args = pytest_args[:-1] + user_args

    print("=" * 60)
    print("NoneBot Dice Helper 测试")
    print("=" * 60)
    print(f"运行命令: {' '.join(pytest_args)}")
    print()

    try:
        result = subprocess.run(pytest_args, check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)


if __name__ == "__main__":
    main()
