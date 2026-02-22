"""
测试配置文件

提供测试所需的共享 fixture 和配置
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))


# 测试配置
pytest_plugins = []


# 在测试前设置 NoneBot 所需的配置
@pytest.fixture(autouse=True)
def setup_nonebot_env():
    """设置 NoneBot 测试环境"""
    import os
    import tempfile

    # Mock NoneBot 模块
    mock_driver = Mock()
    mock_driver.config = {}

    with patch('nonebot.get_driver', return_value=mock_driver):
        with patch('nonebot.plugin.get_plugin_config') as mock_get_plugin_config:
            # 模拟 localstore 插件
            mock_localstore = MagicMock()
            sys.modules['nonebot_plugin_localstore'] = mock_localstore

            # 模拟 get_plugin_data_dir 和 get_plugin_config_file
            temp_dir = Path(tempfile.mkdtemp())
            mock_localstore.get_plugin_data_dir.return_value = temp_dir / "data"
            mock_localstore.get_plugin_config_file.return_value = temp_dir / "config" / "default_data.json"

            # 模拟环境变量
            os.environ.setdefault("NONEBOT_PLUGIN_LOCALSTORE_DATA_DIR", str(temp_dir / "data"))

            yield

            # 清理
            sys.modules.pop('nonebot_plugin_localstore', None)
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_nonebot_driver():
    """Mock NoneBot 驱动"""
    driver = Mock()
    driver.config = {}
    return driver
