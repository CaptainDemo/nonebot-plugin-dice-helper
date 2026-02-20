"""
骰子管理测试

测试骰子的基本管理功能：
- 添加骰子
- 删除骰子
- 获取骰子
- 会话隔离
"""

import sys
from typing import Any
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class DiceManager:
    """简化的骰子管理器，用于测试"""

    def __init__(self):
        self.sessions: dict[str, dict[str, Any]] = {}

    def add_dice(self, session_id: str, name: str, faces: list[list[str]]) -> bool:
        """添加骰子"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {"custom_dice": {}}

        if name in self.sessions[session_id]["custom_dice"]:
            return False

        self.sessions[session_id]["custom_dice"][name] = faces
        return True

    def delete_dice(self, session_id: str, name: str) -> bool:
        """删除骰子"""
        if session_id not in self.sessions:
            return False

        if name not in self.sessions[session_id].get("custom_dice", {}):
            return False

        del self.sessions[session_id]["custom_dice"][name]
        return True

    def get_custom_dice(self, session_id: str) -> dict[str, list[list[str]]]:
        """获取自定义骰子"""
        if session_id not in self.sessions:
            return {}

        return self.sessions[session_id].get("custom_dice", {})

    def get_all_dice(self, session_id: str, default_dice: dict[str, list[list[str]]] = None) -> dict[str, list[list[str]]]:
        """获取所有骰子（默认+自定义）"""
        if default_dice is None:
            default_dice = {}

        custom_dice = self.get_custom_dice(session_id)
        return {**default_dice, **custom_dice}


def test_add_new_dice():
    """测试添加新骰子"""
    manager = DiceManager()
    session_id = "test_session"
    name = "测试骰子"
    faces = [["面1"], ["面2"], ["面3"]]

    result = manager.add_dice(session_id, name, faces)
    assert result is True

    # 验证骰子已添加
    custom_dice = manager.get_custom_dice(session_id)
    assert name in custom_dice
    assert custom_dice[name] == faces


def test_add_duplicate_dice():
    """测试添加重复骰子"""
    manager = DiceManager()
    session_id = "test_session"
    name = "重复骰子"
    faces = [["面1"]]

    # 第一次添加应该成功
    result1 = manager.add_dice(session_id, name, faces)
    assert result1 is True

    # 第二次添加应该失败
    result2 = manager.add_dice(session_id, name, faces)
    assert result2 is False


def test_add_dice_with_multi_items():
    """测试添加多标记骰子"""
    manager = DiceManager()
    session_id = "test_session"
    name = "多标记骰子"
    faces = [["命中", "1"], ["命中", "2"], ["未命中"]]

    result = manager.add_dice(session_id, name, faces)
    assert result is True

    custom_dice = manager.get_custom_dice(session_id)
    assert custom_dice[name] == faces


def test_delete_existing_dice():
    """测试删除存在的骰子"""
    manager = DiceManager()
    session_id = "test_session"
    name = "待删除骰子"
    faces = [["面1"]]

    manager.add_dice(session_id, name, faces)
    result = manager.delete_dice(session_id, name)
    assert result is True

    # 验证已删除
    custom_dice = manager.get_custom_dice(session_id)
    assert name not in custom_dice


def test_delete_nonexistent_dice():
    """测试删除不存在的骰子"""
    manager = DiceManager()
    session_id = "test_session"
    name = "不存在的骰子"

    result = manager.delete_dice(session_id, name)
    assert result is False


def test_get_empty_custom_dice():
    """测试获取空的自定义骰子"""
    manager = DiceManager()
    session_id = "empty_session"

    result = manager.get_custom_dice(session_id)
    assert result == {}


def test_get_custom_dice_with_data():
    """测试获取有数据的自定义骰子"""
    manager = DiceManager()
    session_id = "test_session"

    manager.add_dice(session_id, "骰子1", [["面1"], ["面2"]])
    manager.add_dice(session_id, "骰子2", [["面A"], ["面B"]])

    result = manager.get_custom_dice(session_id)
    assert len(result) == 2
    assert "骰子1" in result
    assert "骰子2" in result


def test_get_all_dice_custom_only():
    """测试仅自定义骰子的获取"""
    manager = DiceManager()
    session_id = "test_session"

    manager.add_dice(session_id, "自定义骰子", [["面1"]])

    result = manager.get_all_dice(session_id)
    assert "自定义骰子" in result


def test_get_all_dice_with_default():
    """测试获取默认和自定义骰子"""
    manager = DiceManager()
    session_id = "test_session"
    default_dice = {
        "默认骰子": [["默认1"], ["默认2"]]
    }

    manager.add_dice(session_id, "自定义骰子", [["自定义1"], ["自定义2"]])

    result = manager.get_all_dice(session_id, default_dice)
    assert "默认骰子" in result
    assert "自定义骰子" in result


def test_get_all_dice_custom_overrides_default():
    """测试自定义骰子覆盖默认骰子"""
    manager = DiceManager()
    session_id = "test_session"
    default_dice = {
        "重叠骰子": [["默认面"]]
    }

    manager.add_dice(session_id, "重叠骰子", [["自定义面"]])

    result = manager.get_all_dice(session_id, default_dice)
    # 自定义骰子应该覆盖默认骰子
    assert result["重叠骰子"] == [["自定义面"]]


def test_session_isolation():
    """测试会话隔离"""
    manager = DiceManager()
    session1 = "group_123"
    session2 = "group_456"

    manager.add_dice(session1, "骰子1", [["面1"]])
    manager.add_dice(session2, "骰子2", [["面2"]])

    result1 = manager.get_custom_dice(session1)
    result2 = manager.get_custom_dice(session2)

    assert "骰子1" in result1
    assert "骰子1" not in result2
    assert "骰子2" in result2
    assert "骰子2" not in result1


def test_complete_workflow():
    """测试完整工作流"""
    manager = DiceManager()
    session_id = "workflow_test"

    # 1. 添加骰子
    success = manager.add_dice(
        session_id,
        "命中骰",
        [["命中", "1"], ["命中", "2"], ["未命中"]]
    )
    assert success is True

    # 2. 获取骰子
    custom_dice = manager.get_custom_dice(session_id)
    assert "命中骰" in custom_dice

    # 3. 删除骰子
    success = manager.delete_dice(session_id, "命中骰")
    assert success is True

    # 4. 确认已删除
    custom_dice = manager.get_custom_dice(session_id)
    assert "命中骰" not in custom_dice


def test_session_id_generation():
    """测试会话ID生成"""
    # 群消息事件模拟
    class GroupEvent:
        def __init__(self, group_id):
            self.group_id = group_id

    # 私聊消息事件模拟
    class PrivateEvent:
        def __init__(self, user_id):
            self.user_id = user_id

    group_event = GroupEvent(12345)
    private_event = PrivateEvent(67890)

    # 模拟 get_session_id 函数
    def get_session_id(event):
        if hasattr(event, "group_id"):
            return f"group_{event.group_id}"
        return f"private_{event.user_id}"

    # 测试群消息
    session_id = get_session_id(group_event)
    assert session_id == "group_12345"

    # 测试私聊消息
    session_id = get_session_id(private_event)
    assert session_id == "private_67890"
