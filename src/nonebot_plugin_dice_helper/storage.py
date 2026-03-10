import json
import logging
from pathlib import Path
from typing import Any, Optional

from nonebot import require
from nonebot.adapters import Event

require("nonebot_plugin_localstore")
from nonebot_plugin_localstore import (
    get_plugin_data_dir,
    get_plugin_config_file,
)

logger = logging.getLogger(__name__)

plugin_config_file: Path = get_plugin_config_file("default_data.json")
plugin_data_dir: Path = get_plugin_data_dir()
default_data: Optional[dict[str, Any]] = None
custom_data: dict[str, dict[str, Any]] = {}

# =====================
# session / path
# =====================

def get_session_id(event: Event) -> str:
    """
    获取会话ID

    Args:
        event: NoneBot事件对象

    Returns:
        str: 会话ID，格式为 "group_{id}" 或 "private_{id}"
    """
    if hasattr(event, "group_id"):
        return f"group_{event.group_id}"
    return f"private_{event.user_id}"


def _get_path(session_id: str) -> Path:
    return plugin_data_dir / f"{session_id}.json"


# =====================
# 会话数据（群 / 私聊）
# =====================

def load_data(session_id: str) -> dict[str, Any]:
    """
    加载会话数据

    Args:
        session_id: 会话ID

    Returns:
        dict: 会话数据，包含 custom_dice, card_decks, card_deck_instances 字段
    """
    global custom_data
    if session_id not in custom_data:
        path = _get_path(session_id)
        if not path.exists():
            custom_data[session_id] = {
                "custom_dice": {},
                "card_decks": {},
                "card_deck_instances": {},
            }
        else:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                # 兼容旧数据结构
                if "card_decks" not in data:
                    data["card_decks"] = {}
                if "card_deck_instances" not in data:
                    data["card_deck_instances"] = {}
                custom_data[session_id] = data
            except json.JSONDecodeError as e:
                logger.warning(f"JSON解析失败 for session {session_id}: {e}")
                custom_data[session_id] = {
                    "custom_dice": {},
                    "card_decks": {},
                    "card_deck_instances": {},
                }
            except IOError as e:
                logger.error(f"读取文件失败 {path}: {e}")
                custom_data[session_id] = {
                    "custom_dice": {},
                    "card_decks": {},
                    "card_deck_instances": {},
                }
    return custom_data[session_id]

def save_data(session_id: str, data: dict[str, Any]) -> None:
    path = _get_path(session_id)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

# =====================
# 默认数据（全插件共用）
# =====================

def _get_default_data() -> dict[str, Any]:
    """
    生成默认数据，包含硬币和扑克牌

    Returns:
        dict: 默认数据
    """
    # 生成扑克牌数据，每张卡是标记列表
    suits = ["♠", "♥", "♣", "♦"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    poker_cards = [[f"{suit}{rank}"] for suit in suits for rank in ranks]
    poker_cards.extend([["小王"], ["大王"]])  # 添加大小王

    return {
        "dice": {
            "硬币": [["正面"], ["反面"]],
        },
        "card_decks": {
            "扑克牌": poker_cards,
        },
    }


def save_default_data(data: dict[str, Any]) -> None:
    """
    保存默认数据到配置文件

    Args:
        data: 默认数据字典
    """
    plugin_config_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_default_data() -> dict[str, Any]:
    """
    加载默认数据

    Returns:
        dict: 默认数据字典
    """
    global default_data
    if default_data is None:
        if not plugin_config_file.exists():
            default_data = _get_default_data()
            save_default_data(default_data)
        else:
            try:
                default_data = json.loads(plugin_config_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                logger.error(f"默认数据JSON解析失败: {e}")
                default_data = _get_default_data()
                save_default_data(default_data)
            except IOError as e:
                logger.error(f"读取默认数据文件失败: {e}")
                default_data = _get_default_data()
                save_default_data(default_data)
    return default_data

def get_default_section(section: str) -> dict[str, Any]:
    """
    读取 default_data.json 中的某个模块数据
    例如：section="dice"
    """
    data = load_default_data()
    value = data.get(section)
    return value if isinstance(value, dict) else {}


def get_card_decks_section() -> dict[str, Any]:
    """
    获取默认卡组定义

    Returns:
        dict: 默认卡组字典，格式为 {卡组名: [卡1, 卡2, ...]}
    """
    return get_default_section("card_decks")
