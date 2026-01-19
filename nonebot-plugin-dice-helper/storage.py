import json
from pathlib import Path
from nonebot_plugin_localstore import (
    get_plugin_data_dir,
    get_plugin_config_dir,
)

DATA_DIR: Path = get_plugin_data_dir()
CONFIG_DIR: Path = get_plugin_config_dir()

DEFAULT_DATA_FILE = CONFIG_DIR / "default_data.json"


def get_session_id(event) -> str:
    if hasattr(event, "group_id"):
        return f"group_{event.group_id}"
    return f"private_{event.user_id}"


def _get_path(session_id: str) -> Path:
    return DATA_DIR / f"{session_id}.json"


def load_data(session_id: str) -> dict:
    path = _get_path(session_id)
    if not path.exists():
        return {"custom_dice": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"custom_dice": {}}


def save_data(session_id: str, data: dict):
    path = _get_path(session_id)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# =====================
# 默认数据（全插件共用）
# =====================

def load_default_data() -> dict:
    if not DEFAULT_DATA_FILE.exists():
        return {}
    try:
        return json.loads(DEFAULT_DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_default_section(section: str) -> dict:
    """
    读取 default_data 中的某个模块数据
    例如：section="dice"
    """
    data = load_default_data()
    value = data.get(section)
    return value if isinstance(value, dict) else {}
