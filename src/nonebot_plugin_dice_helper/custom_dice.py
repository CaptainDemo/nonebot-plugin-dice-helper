from .storage import (
    load_data,
    save_data,
    get_default_section,
)


def add_custom_dice(session_id: str, name: str, faces: list[list[str]]) -> bool:
    """
    添加自定义骰子

    Args:
        session_id: 会话ID，格式为 "group_{id}" 或 "private_{id}"
        name: 骰子名称，不能与数字骰子（如 d6）冲突
        faces: 骰子面列表，每个面可以是多个标记的列表，用 "|" 分隔

    Returns:
        bool: 成功返回 True，失败返回 False

    Examples:
        >>> add_custom_dice("group_123", "硬币", [["正面"], ["反面"]])
        True

        >>> add_custom_dice("private_456", "攻击", [["未命中"], ["命中", "1"], ["命中", "2"]])
        True

        >>> add_custom_dice("group_123", "d6", [["1"], ["2"]])
        False  # 与数字骰子冲突
    """
    default_dice = get_default_section("custom_dice")
    if name in default_dice:
        return False

    data = load_data(session_id)
    if name in data["custom_dice"]:
        return False

    data["custom_dice"][name] = faces
    save_data(session_id, data)
    return True


def del_custom_dice(session_id: str, name: str) -> bool:
    """
    删除自定义骰子

    Args:
        session_id: 会话ID
        name: 要删除的骰子名称

    Returns:
        bool: 成功返回 True，骰子不存在返回 False

    Examples:
        >>> del_custom_dice("group_123", "硬币")
        True

        >>> del_custom_dice("group_123", "不存在的骰子")
        False
    """
    data = load_data(session_id)
    if name not in data["custom_dice"]:
        return False

    del data["custom_dice"][name]
    save_data(session_id, data)
    return True


def get_custom_dice(session_id: str) -> dict[str, list[list[str]]]:
    """
    获取指定会话的自定义骰子

    Args:
        session_id: 会话ID

    Returns:
        dict: 自定义骰子字典，格式为 {骰子名: [面1, 面2, ...]}

    Examples:
        >>> get_custom_dice("group_123")
        {"硬币": [["正面"], ["反面"]], "攻击": [["命中"], ["未命中"]]}
    """
    return load_data(session_id).get("custom_dice", {})


def get_default_dice() -> dict[str, list[list[str]]]:
    """
    获取全局默认骰子

    Returns:
        dict: 默认骰子字典，格式为 {骰子名: [面1, 面2, ...]}

    Note:
        默认骰子定义在 default_data.json 文件中，对所有会话可见
        且不能通过命令删除
    """
    return get_default_section("custom_dice")


def get_all_dice(session_id: str) -> dict[str, list[list[str]]]:
    """
    获取所有可用骰子（默认 + 自定义）

    Args:
        session_id: 会话ID

    Returns:
        dict: 所有骰子字典，自定义骰子会覆盖同名的默认骰子

    Examples:
        >>> get_all_dice("group_123")
        {
            "硬币": [["正面"], ["反面"]],  # 默认骰子
            "攻击": [["命中"], ["未命中"]]  # 自定义骰子
        }
    """
    default_dice = get_default_dice()
    custom_dice = get_custom_dice(session_id)
    return {**default_dice, **custom_dice}
