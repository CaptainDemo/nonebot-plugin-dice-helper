import logging

from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg

from .utils import maybe_apply_prefix_variance, DICE_ADMIN
from .storage import get_session_id
from .card_deck import (
    add_card_deck,
    del_card_deck,
    config_card_deck,
    get_all_card_deck_definitions,
    get_custom_card_deck_definitions,
    get_default_card_deck_definitions,
    get_card_deck_definition,
    is_default_card_deck,
)
from .card_draw import (
    draw_cards_from_top,
    draw_cards_from_bottom,
    shuffle_deck,
    put_cards_on_top,
    put_cards_on_bottom,
    reset_deck_instance,
    get_deck_instance_cards,
    format_draw_result,
    format_view_result,
)

logger = logging.getLogger(__name__)


# =====================
# add_deck（仅群管理 / 超级用户）
# =====================

add_deck_cmd = on_command(
    "add_deck",
    aliases={"添加卡组"},
    priority=5,
    permission=DICE_ADMIN,
)


@add_deck_cmd.handle()
async def handle_add_deck(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理添加卡组命令
    """
    text = args.extract_plain_text().strip()
    if not text:
        await add_deck_cmd.finish(
            maybe_apply_prefix_variance("用法：add_deck <卡组名> <卡1> <卡2> ...\n卡片格式：标记1|标记2|...")
        )

    parts = text.split()
    if len(parts) < 2:
        await add_deck_cmd.finish(maybe_apply_prefix_variance("至少需要一张卡牌"))

    name = parts[0]
    cards = [p.split("|") for p in parts[1:]]

    session_id = get_session_id(event)
    ok = add_card_deck(session_id, name, cards)

    if ok:
        await add_deck_cmd.finish(
            maybe_apply_prefix_variance(f"卡组「{name}」定义成功（{len(cards)}张）")
        )
    else:
        await add_deck_cmd.finish(
            maybe_apply_prefix_variance(f"卡组「{name}」定义失败（可能与默认卡组同名）")
        )


# =====================
# del_deck（仅群管理 / 超级用户）
# =====================

del_deck_cmd = on_command(
    "del_deck",
    aliases={"删除卡组"},
    priority=5,
    permission=DICE_ADMIN,
)


@del_deck_cmd.handle()
async def handle_del_deck(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理删除卡组命令
    """
    name = args.extract_plain_text().strip()
    if not name:
        await del_deck_cmd.finish(maybe_apply_prefix_variance("用法：del_deck <卡组名>"))

    session_id = get_session_id(event)

    # 检查是否为默认卡组
    if is_default_card_deck(name):
        await del_deck_cmd.finish(maybe_apply_prefix_variance("无法删除默认卡组"))

    ok = del_card_deck(session_id, name)
    await del_deck_cmd.finish(
        maybe_apply_prefix_variance("删除成功" if ok else "删除失败（卡组不存在）")
    )


# =====================
# config_deck（仅群管理 / 超级用户）
# =====================

config_deck_cmd = on_command(
    "config_deck",
    aliases={"配置卡组"},
    priority=5,
    permission=DICE_ADMIN,
)


@config_deck_cmd.handle()
async def handle_config_deck(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理配置卡组命令
    """
    text = args.extract_plain_text().strip()
    if not text:
        await config_deck_cmd.finish(
            maybe_apply_prefix_variance(
                "用法：config_deck <卡组名> [选项]\n"
                "选项：\n"
                "  shuffle_on_init=true  创建/重置时自动洗混\n"
                "  shuffle_on_init=false 创建/重置时保持固定顺序\n"
                "不带选项时显示当前配置"
            )
        )

    parts = text.split()
    deck_name = parts[0]

    session_id = get_session_id(event)

    # 检查是否为默认卡组
    if is_default_card_deck(deck_name):
        await config_deck_cmd.finish(maybe_apply_prefix_variance("无法配置默认卡组"))

    # 获取当前配置
    definition = get_card_deck_definition(session_id, deck_name)
    if definition is None:
        await config_deck_cmd.finish(maybe_apply_prefix_variance("卡组不存在"))

    # 如果只有卡组名，显示当前配置
    if len(parts) == 1:
        shuffle_on_init = definition.get("shuffle_on_init", True)
        cards = definition.get("cards", [])
        status = "随机洗混" if shuffle_on_init else "固定顺序"
        await config_deck_cmd.finish(
            maybe_apply_prefix_variance(
                f"卡组「{deck_name}」（{len(cards)}张）\n"
                f"创建/重置时：{status}"
            )
        )

    # 解析配置项
    shuffle_on_init = None
    for part in parts[1:]:
        if part.startswith("shuffle_on_init="):
            value = part.split("=", 1)[1].lower()
            if value in ("true", "1", "yes"):
                shuffle_on_init = True
            elif value in ("false", "0", "no"):
                shuffle_on_init = False
            else:
                await config_deck_cmd.finish(
                    maybe_apply_prefix_variance(f"无效的值：{part}")
                )

    if shuffle_on_init is None:
        await config_deck_cmd.finish(maybe_apply_prefix_variance("未指定有效配置项"))

    ok, error = config_card_deck(session_id, deck_name, shuffle_on_init)
    if error:
        await config_deck_cmd.finish(maybe_apply_prefix_variance(error))

    status = "随机洗混" if shuffle_on_init else "固定顺序"
    await config_deck_cmd.finish(
        maybe_apply_prefix_variance(f"卡组「{deck_name}」配置已更新\n创建/重置时：{status}")
    )


# =====================
# deck_list / 卡组列表
# =====================

deck_list_cmd = on_command(
    "deck_list",
    aliases={"卡组列表"},
    priority=5,
)


@deck_list_cmd.handle()
async def handle_deck_list(event: MessageEvent):
    """
    处理卡组列表命令
    """
    session_id = get_session_id(event)
    default_decks = get_default_card_deck_definitions()
    custom_decks = get_custom_card_deck_definitions(session_id)

    lines = ["当前可用卡组："]

    if default_decks:
        lines.append("【默认卡组】")
        for name, cards in default_decks.items():
            lines.append(f"- {name}（{len(cards)}张）")

    if custom_decks:
        lines.append("【自定义卡组】")
        for name, cards in custom_decks.items():
            lines.append(f"- {name}（{len(cards)}张）")

    if not default_decks and not custom_decks:
        lines.append("（暂无卡组）")

    await deck_list_cmd.finish(maybe_apply_prefix_variance("\n".join(lines)))


# =====================
# draw_top / 顶部抽卡
# =====================

draw_top_cmd = on_command(
    "draw_top",
    aliases={"顶部抽卡", "抽卡", "draw"},
    priority=5,
)


@draw_top_cmd.handle()
async def handle_draw_top(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理顶部抽卡命令
    """
    text = args.extract_plain_text().strip()
    if not text:
        await draw_top_cmd.finish(maybe_apply_prefix_variance("用法：draw_top <卡组名> [数量=1]"))

    parts = text.split()
    deck_name = parts[0]
    count = 1

    if len(parts) > 1:
        try:
            count = int(parts[1])
            if count <= 0:
                await draw_top_cmd.finish(maybe_apply_prefix_variance("数量必须大于0"))
        except ValueError:
            await draw_top_cmd.finish(maybe_apply_prefix_variance("数量格式错误"))

    session_id = get_session_id(event)
    drawn, error = draw_cards_from_top(session_id, deck_name, count)

    if error:
        await draw_top_cmd.finish(maybe_apply_prefix_variance(error))

    # 获取剩余数量
    remaining_cards, _ = get_deck_instance_cards(session_id, deck_name)
    remaining_count = len(remaining_cards) if remaining_cards else 0

    result = format_draw_result(deck_name, drawn, remaining_count, len(drawn), count)
    await draw_top_cmd.finish(maybe_apply_prefix_variance(result))


# =====================
# draw_bottom / 底部抽卡
# =====================

draw_bottom_cmd = on_command(
    "draw_bottom",
    aliases={"底部抽卡"},
    priority=5,
)


@draw_bottom_cmd.handle()
async def handle_draw_bottom(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理底部抽卡命令
    """
    text = args.extract_plain_text().strip()
    if not text:
        await draw_bottom_cmd.finish(maybe_apply_prefix_variance("用法：draw_bottom <卡组名> [数量=1]"))

    parts = text.split()
    deck_name = parts[0]
    count = 1

    if len(parts) > 1:
        try:
            count = int(parts[1])
            if count <= 0:
                await draw_bottom_cmd.finish(maybe_apply_prefix_variance("数量必须大于0"))
        except ValueError:
            await draw_bottom_cmd.finish(maybe_apply_prefix_variance("数量格式错误"))

    session_id = get_session_id(event)
    drawn, error = draw_cards_from_bottom(session_id, deck_name, count)

    if error:
        await draw_bottom_cmd.finish(maybe_apply_prefix_variance(error))

    # 获取剩余数量
    remaining_cards, _ = get_deck_instance_cards(session_id, deck_name)
    remaining_count = len(remaining_cards) if remaining_cards else 0

    result = format_draw_result(deck_name, drawn, remaining_count, len(drawn), count)
    await draw_bottom_cmd.finish(maybe_apply_prefix_variance(result))


# =====================
# shuffle / 洗混
# =====================

shuffle_cmd = on_command(
    "shuffle",
    aliases={"洗混"},
    priority=5,
)


@shuffle_cmd.handle()
async def handle_shuffle(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理洗混命令
    """
    deck_name = args.extract_plain_text().strip()
    if not deck_name:
        await shuffle_cmd.finish(maybe_apply_prefix_variance("用法：shuffle <卡组名>"))

    session_id = get_session_id(event)
    success, error = shuffle_deck(session_id, deck_name)

    if error:
        await shuffle_cmd.finish(maybe_apply_prefix_variance(error))

    # 获取卡牌数量
    cards, _ = get_deck_instance_cards(session_id, deck_name)
    count = len(cards) if cards else 0

    await shuffle_cmd.finish(
        maybe_apply_prefix_variance(f"卡组「{deck_name}」已洗混（{count}张）")
    )


# =====================
# put_top / 放顶部
# =====================

put_top_cmd = on_command(
    "put_top",
    aliases={"放顶部"},
    priority=5,
)


@put_top_cmd.handle()
async def handle_put_top(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理放顶部命令
    """
    text = args.extract_plain_text().strip()
    if not text:
        await put_top_cmd.finish(
            maybe_apply_prefix_variance("用法：put_top <卡组名> <卡1> [卡2] ...\n卡片格式：标记1|标记2|...")
        )

    parts = text.split()
    if len(parts) < 2:
        await put_top_cmd.finish(maybe_apply_prefix_variance("至少需要一张卡牌"))

    deck_name = parts[0]
    cards = [p.split("|") for p in parts[1:]]

    session_id = get_session_id(event)
    success, error = put_cards_on_top(session_id, deck_name, cards)

    if error:
        await put_top_cmd.finish(maybe_apply_prefix_variance(error))

    # 获取卡牌数量
    remaining_cards, _ = get_deck_instance_cards(session_id, deck_name)
    count = len(remaining_cards) if remaining_cards else 0

    await put_top_cmd.finish(
        maybe_apply_prefix_variance(f"已将{len(cards)}张卡牌放入「{deck_name}」顶部（共{count}张）")
    )


# =====================
# put_bottom / 放底部
# =====================

put_bottom_cmd = on_command(
    "put_bottom",
    aliases={"放底部"},
    priority=5,
)


@put_bottom_cmd.handle()
async def handle_put_bottom(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理放底部命令
    """
    text = args.extract_plain_text().strip()
    if not text:
        await put_bottom_cmd.finish(
            maybe_apply_prefix_variance("用法：put_bottom <卡组名> <卡1> [卡2] ...\n卡片格式：标记1|标记2|...")
        )

    parts = text.split()
    if len(parts) < 2:
        await put_bottom_cmd.finish(maybe_apply_prefix_variance("至少需要一张卡牌"))

    deck_name = parts[0]
    cards = [p.split("|") for p in parts[1:]]

    session_id = get_session_id(event)
    success, error = put_cards_on_bottom(session_id, deck_name, cards)

    if error:
        await put_bottom_cmd.finish(maybe_apply_prefix_variance(error))

    # 获取卡牌数量
    remaining_cards, _ = get_deck_instance_cards(session_id, deck_name)
    count = len(remaining_cards) if remaining_cards else 0

    await put_bottom_cmd.finish(
        maybe_apply_prefix_variance(f"已将{len(cards)}张卡牌放入「{deck_name}」底部（共{count}张）")
    )


# =====================
# reset_deck / 重置卡组
# =====================

reset_deck_cmd = on_command(
    "reset_deck",
    aliases={"重置卡组"},
    priority=5,
)


@reset_deck_cmd.handle()
async def handle_reset_deck(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理重置卡组命令
    """
    deck_name = args.extract_plain_text().strip()
    if not deck_name:
        await reset_deck_cmd.finish(maybe_apply_prefix_variance("用法：reset_deck <卡组名>"))

    session_id = get_session_id(event)
    success, error, count = reset_deck_instance(session_id, deck_name)

    if error:
        await reset_deck_cmd.finish(maybe_apply_prefix_variance(error))

    await reset_deck_cmd.finish(
        maybe_apply_prefix_variance(f"卡组「{deck_name}」已重置（{count}张）")
    )


# =====================
# view_deck / 查看卡组
# =====================

view_deck_cmd = on_command(
    "view_deck",
    aliases={"查看卡组"},
    priority=5,
)


@view_deck_cmd.handle()
async def handle_view_deck(
    event: MessageEvent,
    args: Message = CommandArg(),
):
    """
    处理查看卡组命令
    """
    deck_name = args.extract_plain_text().strip()
    if not deck_name:
        await view_deck_cmd.finish(maybe_apply_prefix_variance("用法：view_deck <卡组名>"))

    session_id = get_session_id(event)
    cards, error = get_deck_instance_cards(session_id, deck_name)

    if error:
        await view_deck_cmd.finish(maybe_apply_prefix_variance(error))

    result = format_view_result(deck_name, cards)
    await view_deck_cmd.finish(maybe_apply_prefix_variance(result))
