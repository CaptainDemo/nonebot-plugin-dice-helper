# 测试说明

本项目包含完整的本地测试套件，测试骰子插件的核心功能。

## 快速开始

### 方法一：使用测试脚本（推荐）

```bash
# 运行所有测试
python run_tests.py

# 运行特定模块的测试
python run_tests.py test_utils
python run_tests.py test_dice_logic
python run_tests.py test_dice_management

# 运行名称包含特定关键词的测试
python run_tests.py -k "roll"

# 生成覆盖率报告
python run_tests.py --cov
```

### 方法二：直接使用 pytest

```bash
# 运行所有测试
pytest tests/

# 运行特定文件
pytest tests/test_utils.py

# 运行特定测试函数
pytest tests/test_utils.py::test_parse_roll_args_multiple_dice

# 显示详细输出
pytest -v tests/

# 显示打印输出
pytest -s tests/
```

## 测试结构

```
tests/
├── __init__.py                 # 测试包初始化
├── conftest.py                 # 测试配置和共享 fixtures
├── test_utils.py               # 工具函数测试（9个测试）
├── test_dice_logic.py         # 骰子逻辑测试（15个测试）
└── test_dice_management.py    # 骰子管理测试（13个测试）
```

## 测试统计

总计 **37 个测试**，涵盖：

| 测试模块 | 测试数量 | 覆盖范围 |
|---------|---------|---------|
| test_utils.py | 9 | 参数解析、前缀扰动 |
| test_dice_logic.py | 15 | 投掷逻辑、结果格式化 |
| test_dice_management.py | 13 | 骰子管理、会话隔离 |

## 测试覆盖范围

### test_utils.py
- `parse_roll_args()`: 解析骰子投掷参数
  - 空列表处理
  - 单个骰子（带/不带数量）
  - 多个骰子
  - 空白字符处理
  - 复杂骰子名称
  - 大数量处理
- `maybe_apply_prefix_variance()`: 应用前缀扰动
  - None 处理
  - 异常处理

### test_dice_logic.py
- 数字骰子投掷
- 自定义骰子投掷
- 混合投掷
- 结果统计
- 结果格式化
- 骰子面解析
- 骰子有效性验证

### test_dice_management.py
- 添加骰子
- 删除骰子
- 获取骰子
- 会话隔离
- 默认骰子和自定义骰子合并
- 完整工作流测试

## 测试依赖

测试使用标准的 Python 测试框架：

```bash
pip install pytest pytest-mock pytest-cov pytest-asyncio
```

或者使用项目配置的开发依赖：

```bash
pip install -e .[dev]
```

## 运行测试覆盖率报告

```bash
# 生成覆盖率报告
pytest --cov tests/

# 生成 HTML 覆盖率报告
pytest --cov --cov-report=html tests/

# 在浏览器中打开覆盖率报告
# (Windows) start htmlcov/index.html
# (Mac/Linux) open htmlcov/index.html
```

## 常用 pytest 选项

```bash
# 显示每个测试的打印输出
pytest -s tests/

# 只运行失败的测试
pytest --lf tests/

# 停止在第一个失败处
pytest -x tests/

# 显示详细错误信息
pytest --tb=long tests/

# 运行标记为慢速的测试（如果使用了标记）
pytest -m "not slow" tests/

# 并行运行测试（需要安装 pytest-xdist）
pip install pytest-xdist
pytest -n auto tests/
```

## 测试特点

1. **独立性**: 测试之间相互独立，可以单独运行
2. **无依赖**: 不需要完整的 NoneBot 环境，使用简化的模拟对象
3. **快速执行**: 所有测试在 1 秒内完成
4. **覆盖全面**: 涵盖核心功能的各种场景

## 添加新测试

添加新测试时，请遵循以下规范：

1. 测试文件命名：`test_<module_name>.py`
2. 测试函数命名：`test_<function_name>_<scenario>`
3. 添加清晰的文档字符串说明测试目的

示例：

```python
def test_add_dice_success():
    """测试成功添加骰子"""
    manager = DiceManager()
    session_id = "test_session"
    name = "测试骰子"
    faces = [["面1"], ["面2"]]

    result = manager.add_dice(session_id, name, faces)

    assert result is True
    custom_dice = manager.get_custom_dice(session_id)
    assert name in custom_dice
```

## 测试结果解读

运行测试后，你会看到类似以下输出：

```
============================= test session starts =============================
collected 37 items

tests/test_dice_logic.py::test_dice_roll_numeric PASSED                  [  2%]
tests/test_dice_logic.py::test_dice_roll_custom PASSED                   [  5%]
...
============================= 37 passed in 0.65s ==============================
```

- `PASSED`: 测试通过
- `FAILED`: 测试失败
- `SKIPPED`: 测试被跳过
- `XX%`: 测试进度

## 故障排查

### 测试无法导入模块
如果遇到导入错误，确保项目根目录在 Python 路径中：

```python
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

### 测试失败
如果测试失败，查看详细错误信息：

```bash
pytest -v --tb=long tests/
```

### 缓存问题
如果遇到缓存问题，清除 pytest 缓存：

```bash
pytest --cache-clear tests/
```
