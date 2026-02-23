import copy
import random
from typing import Optional

from .storage import load_data, save_data
from .card_deck import get_card_deck_definition


def _get_deck_instance(session_id: str, deck_name: str) -> Optional[list[list[str]]]:
    """
    获取卡组实例的卡牌列表

    Args:
        session_id: 会话ID
        deck_name: 卡组名称

    Returns:
        Optional[list]: 卡牌列表，不存在返回 None
    """
    data = load_data(session_id)
    instances = data.get("card_deck_instances", {})
    if deck_name in instances:
        return instances[deck_name].get("cards")
    return None


def _save_deck_instance(session_id: str, deck_name: str, cards: list[list[str]]) -> None:
    """
    保存卡组实例

    Args:
        session_id: 会话ID
        deck_name: 卡组名称
        cards: 卡牌列表
    """
    data = load_data(session_id)
    if "card_deck_instances" not in data:
        data["card_deck_instances"] = {}
    data["card_deck_instances"][deck_name] = {"cards": cards}
    save_data(session_id, data)


def get_or_create_deck_instance(
    session_id: str, deck_name: str
) -> tuple[Optional[list[list[str]]], Optional[str]]:
    """
    获取或创建卡组实例

    Args:
        session_id: 会话ID
        deck_name: 卡组名称

    Returns:
        tuple: (卡牌列表, 错误信息)
    """
    # 先检查实例是否存在
    instance_cards = _get_deck_instance(session_id, deck_name)
    if instance_cards is not None:
        return instance_cards, None

    # 实例不存在，从定义创建
    definition = get_card_deck_definition(session_id, deck_name)
    if definition is None:
        return None, f"卡组「{deck_name}」不存在"

    # 深拷贝创建实例
    cards = copy.deepcopy(definition.get("cards", []))

    # 根据配置决定是否洗混
    if definition.get("shuffle_on_init", True):
        random.shuffle(cards)

    _save_deck_instance(session_id, deck_name, cards)
    return cards, None


def draw_cards_from_top(
    session_id: str, deck_name: str, count: int = 1
) -> tuple[Optional[list[list[str]]], Optional[str]]:
    """
    从卡组顶部抽卡

    Args:
        session_id: 会话ID
        deck_name: 卡组名称
        count: 抽卡数量

    Returns:
        tuple: (抽取的卡牌列表, 错误信息)
    """
    cards, error = get_or_create_deck_instance(session_id, deck_name)
    if error:
        return None, error

    if not cards:
        return None, f"卡组「{deck_name}」已无卡牌，请使用 reset_deck 重置"

    actual_count = min(count, len(cards))
    drawn = cards[:actual_count]
    remaining = cards[actual_count:]
    _save_deck_instance(session_id, deck_name, remaining)

    return drawn, None


def draw_cards_from_bottom(
    session_id: str, deck_name: str, count: int = 1
) -> tuple[Optional[list[list[str]]], Optional[str]]:
    """
    从卡组底部抽卡

    Args:
        session_id: 会话ID
        deck_name: 卡组名称
        count: 抽卡数量

    Returns:
        tuple: (抽取的卡牌列表, 错误信息)
    """
    cards, error = get_or_create_deck_instance(session_id, deck_name)
    if error:
        return None, error

    if not cards:
        return None, f"卡组「{deck_name}」已无卡牌，请使用 reset_deck 重置"

    actual_count = min(count, len(cards))
    drawn = cards[-actual_count:]
    drawn.reverse()  # 底部抽卡时倒序，模拟真实抽卡顺序
    remaining = cards[:-actual_count]
    _save_deck_instance(session_id, deck_name, remaining)

    return drawn, None


def shuffle_deck(
    session_id: str, deck_name: str
) -> tuple[bool, Optional[str]]:
    """
    洗混卡组

    Args:
        session_id: 会话ID
        deck_name: 卡组名称

    Returns:
        tuple: (是否成功, 错误信息)
    """
    cards, error = get_or_create_deck_instance(session_id, deck_name)
    if error:
        return False, error

    random.shuffle(cards)
    _save_deck_instance(session_id, deck_name, cards)
    return True, None


def put_cards_on_top(
    session_id: str, deck_name: str, cards_to_add: list[list[str]]
) -> tuple[bool, Optional[str]]:
    """
    将卡牌放到卡组顶部

    Args:
        session_id: 会话ID
        deck_name: 卡组名称
        cards_to_add: 要添加的卡牌列表

    Returns:
        tuple: (是否成功, 错误信息)
    """
    cards, error = get_or_create_deck_instance(session_id, deck_name)
    if error:
        return False, error

    new_cards = cards_to_add + cards
    _save_deck_instance(session_id, deck_name, new_cards)
    return True, None


def put_cards_on_bottom(
    session_id: str, deck_name: str, cards_to_add: list[list[str]]
) -> tuple[bool, Optional[str]]:
    """
    将卡牌放到卡组底部

    Args:
        session_id: 会话ID
        deck_name: 卡组名称
        cards_to_add: 要添加的卡牌列表

    Returns:
        tuple: (是否成功, 错误信息)
    """
    cards, error = get_or_create_deck_instance(session_id, deck_name)
    if error:
        return False, error

    # 底部放卡时倒序，模拟真实放卡顺序（后放的在最底部）
    reversed_cards = cards_to_add.copy()
    reversed_cards.reverse()
    new_cards = cards + reversed_cards
    _save_deck_instance(session_id, deck_name, new_cards)
    return True, None


def reset_deck_instance(
    session_id: str, deck_name: str
) -> tuple[bool, Optional[str], int]:
    """
    重置卡组实例到初始状态

    Args:
        session_id: 会话ID
        deck_name: 卡组名称

    Returns:
        tuple: (是否成功, 错误信息, 卡牌数量)
    """
    definition = get_card_deck_definition(session_id, deck_name)
    if definition is None:
        return False, f"卡组「{deck_name}」不存在", 0

    cards = copy.deepcopy(definition.get("cards", []))

    # 根据配置决定是否洗混
    if definition.get("shuffle_on_init", True):
        random.shuffle(cards)

    _save_deck_instance(session_id, deck_name, cards)
    return True, None, len(cards)


def get_deck_instance_cards(
    session_id: str, deck_name: str
) -> tuple[Optional[list[list[str]]], Optional[str]]:
    """
    获取卡组实例的卡牌列表（用于查看）

    Args:
        session_id: 会话ID
        deck_name: 卡组名称

    Returns:
        tuple: (卡牌列表, 错误信息)
    """
    return get_or_create_deck_instance(session_id, deck_name)


def count_tags(cards: list[list[str]]) -> dict[str, int]:
    """
    统计卡牌标记出现次数

    Args:
        cards: 卡牌列表，每张卡是一个标记列表

    Returns:
        dict: 标记统计字典
    """
    counter: dict[str, int] = {}
    for card in cards:
        for tag in card:
            counter[tag] = counter.get(tag, 0) + 1
    return counter


def format_draw_result(
    deck_name: str,
    drawn_cards: list[list[str]],
    remaining_count: int,
    actual_count: int,
    requested_count: int,
) -> str:
    """
    格式化抽卡结果

    Args:
        deck_name: 卡组名称
        drawn_cards: 抽取的卡牌，每张卡是一个标记列表
        remaining_count: 剩余卡牌数
        actual_count: 实际抽卡数
        requested_count: 请求抽卡数

    Returns:
        str: 格式化后的结果字符串
    """
    lines = [f"抽卡结果（{deck_name} ×{actual_count}）："]

    if actual_count < requested_count:
        lines[0] += f"（请求{requested_count}张，仅剩{actual_count}张）"

    for i, card in enumerate(drawn_cards, 1):
        if card:
            lines.append(f"{i}. {', '.join(card)}")
        else:
            lines.append(f"{i}. （空）")

    # 标记统计
    tag_counter = count_tags(drawn_cards)
    if tag_counter:
        lines.append("")
        lines.append("标记统计：")
        tag_items = sorted(tag_counter.items(), key=lambda x: (-x[1], x[0]))
        lines.append("、".join(f"{tag} ×{count}" for tag, count in tag_items))

    lines.append("")
    lines.append(f"剩余：{remaining_count}张")

    return "\n".join(lines)


def format_view_result(
    deck_name: str,
    cards: list[list[str]],
) -> str:
    """
    格式化查看卡组结果

    Args:
        deck_name: 卡组名称
        cards: 卡牌列表，每张卡是一个标记列表

    Returns:
        str: 格式化后的结果字符串
    """
    total = len(cards)
    lines = [f"卡组「{deck_name}」剩余{total}张："]

    if total <= 20:
        # 显示全部
        for i, card in enumerate(cards, 1):
            if card:
                lines.append(f"[{i}] {', '.join(card)}")
            else:
                lines.append(f"[{i}] （空）")
    else:
        # 显示前后各10张
        lines.append("")
        for i, card in enumerate(cards[:10], 1):
            if card:
                lines.append(f"[{i}] {', '.join(card)}")
            else:
                lines.append(f"[{i}] （空）")

        lines.append(f"... 省略 {total - 20} 张 ...")

        for i, card in enumerate(cards[-10:], total - 9):
            if card:
                lines.append(f"[{i}] {', '.join(card)}")
            else:
                lines.append(f"[{i}] （空）")

    return "\n".join(lines)
