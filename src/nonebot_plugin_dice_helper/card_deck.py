from typing import Optional, Any

from .storage import (
    load_data,
    save_data,
    get_card_decks_section,
)


def _normalize_deck_definition(definition: Any) -> dict:
    """
    标准化卡组定义格式

    Args:
        definition: 原始定义（可能是 list 或 dict）

    Returns:
        dict: 标准化后的定义 {"cards": [...], "shuffle_on_init": bool}
    """
    if isinstance(definition, list):
        return {"cards": definition, "shuffle_on_init": True}
    if isinstance(definition, dict):
        return {
            "cards": definition.get("cards", []),
            "shuffle_on_init": definition.get("shuffle_on_init", True),
        }
    return {"cards": [], "shuffle_on_init": True}


def add_card_deck(session_id: str, name: str, cards: list[list[str]]) -> bool:
    """
    添加自定义卡组

    Args:
        session_id: 会话ID
        name: 卡组名称
        cards: 卡牌列表，每张卡可以是多个标记的列表

    Returns:
        bool: 成功返回 True，失败返回 False
    """
    default_decks = get_card_decks_section()
    if name in default_decks:
        return False

    data = load_data(session_id)
    if name in data["card_decks"]:
        return False

    # 新卡组默认创建时洗混
    data["card_decks"][name] = {"cards": cards, "shuffle_on_init": True}
    save_data(session_id, data)
    return True


def del_card_deck(session_id: str, name: str) -> bool:
    """
    删除自定义卡组

    Args:
        session_id: 会话ID
        name: 要删除的卡组名称

    Returns:
        bool: 成功返回 True，卡组不存在返回 False
    """
    data = load_data(session_id)
    if name not in data["card_decks"]:
        return False

    del data["card_decks"][name]
    # 同时删除实例
    if name in data.get("card_deck_instances", {}):
        del data["card_deck_instances"][name]
    save_data(session_id, data)
    return True


def config_card_deck(
    session_id: str, name: str, shuffle_on_init: Optional[bool] = None
) -> tuple[bool, Optional[str]]:
    """
    配置自定义卡组参数

    Args:
        session_id: 会话ID
        name: 卡组名称
        shuffle_on_init: 创建实例时是否洗混，None 表示不修改

    Returns:
        tuple: (是否成功, 错误信息)
    """
    data = load_data(session_id)
    if name not in data["card_decks"]:
        return False, "卡组不存在或为默认卡组"

    deck_def = data["card_decks"][name]
    # 兼容旧格式
    if isinstance(deck_def, list):
        data["card_decks"][name] = {"cards": deck_def, "shuffle_on_init": True}
        deck_def = data["card_decks"][name]

    if shuffle_on_init is not None:
        deck_def["shuffle_on_init"] = shuffle_on_init

    save_data(session_id, data)
    return True, None


def get_card_deck_definition(session_id: str, name: str) -> Optional[dict]:
    """
    获取指定卡组的完整定义（优先自定义，其次默认）

    Args:
        session_id: 会话ID
        name: 卡组名称

    Returns:
        Optional[dict]: 卡组定义 {"cards": [...], "shuffle_on_init": bool}，不存在返回 None
    """
    # 优先查找自定义卡组
    data = load_data(session_id)
    if name in data["card_decks"]:
        return _normalize_deck_definition(data["card_decks"][name])

    # 其次查找默认卡组
    default_decks = get_card_decks_section()
    if name in default_decks:
        return _normalize_deck_definition(default_decks[name])

    return None


def get_card_deck_cards(session_id: str, name: str) -> Optional[list[list[str]]]:
    """
    获取指定卡组的卡牌列表

    Args:
        session_id: 会话ID
        name: 卡组名称

    Returns:
        Optional[list]: 卡牌列表，不存在返回 None
    """
    definition = get_card_deck_definition(session_id, name)
    if definition is None:
        return None
    return definition.get("cards", [])


def get_all_card_deck_definitions(session_id: str) -> dict[str, dict]:
    """
    获取所有可用卡组（默认 + 自定义）

    Args:
        session_id: 会话ID

    Returns:
        dict: 所有卡组字典，自定义卡组会覆盖同名的默认卡组
    """
    default_decks = get_card_decks_section()
    custom_decks = get_custom_card_deck_definitions(session_id)

    result = {}
    for name, definition in {**default_decks, **custom_decks}.items():
        result[name] = _normalize_deck_definition(definition)
    return result


def get_custom_card_deck_definitions(session_id: str) -> dict[str, Any]:
    """
    获取指定会话的自定义卡组（原始格式）

    Args:
        session_id: 会话ID

    Returns:
        dict: 自定义卡组字典
    """
    return load_data(session_id).get("card_decks", {})


def get_default_card_deck_definitions() -> dict[str, Any]:
    """
    获取全局默认卡组（原始格式）

    Returns:
        dict: 默认卡组字典
    """
    return get_card_decks_section()


def is_default_card_deck(name: str) -> bool:
    """
    检查卡组是否为默认卡组

    Args:
        name: 卡组名称

    Returns:
        bool: 是默认卡组返回 True
    """
    return name in get_card_decks_section()
