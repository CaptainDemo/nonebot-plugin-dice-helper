from nonebot.permission import SUPERUSER
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent
)
from nonebot.internal.permission import Permission
from nonebot import logger

from .config import plugin_config
prefix_variance = None
if plugin_config.dice_helper_use_prefix_variance:
    try:
        from nonebot_plugin_message_limiter import prefix_variance
    except ImportError as e:
        prefix_variance = None
        logger.warning(
            "prefix_variance 未加载，dice_helper 将不使用前缀扰动功能",
            exc_info=e,
        )
    
async def dice_admin_permission(bot: Bot, event: Event) -> bool:
    """
    判断用户是否有骰子管理权限

    Args:
        bot: 机器人实例
        event: 事件对象

    Returns:
        bool: 有权限返回 True，否则返回 False
    """
    if isinstance(event, PrivateMessageEvent):
        return True

    # 群聊：群主 / 管理员 / 超级用户
    if isinstance(event, GroupMessageEvent):
        return (
            event.sender.role in ("admin", "owner")
            or await SUPERUSER(bot, event)
        )

    return False
    
DICE_ADMIN = Permission(dice_admin_permission)
    
def maybe_apply_prefix_variance(text: str) -> str:
    """
    根据配置决定是否使用 prefix_variance

    Args:
        text: 原始文本

    Returns:
        str: 处理后的文本，如果 prefix_variance 不可用则返回原文本
    """
    if prefix_variance is None:
        return text

    try:
        return prefix_variance.apply(text)
    except Exception:
        return text
