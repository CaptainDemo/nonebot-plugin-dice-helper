from nonebot.plugin import PluginMetadata
from .config import DiceHelperConfig

__plugin_meta__ = PluginMetadata(
    name="Dice Helper",
    description="NoneBot 可自定义骰子的骰子插件",
    usage=(
        "=== 骰子功能 ===\n"
        "roll / 投掷 <参数>\n"
        "add_dice <骰子名> <面1> <面2> ...\n"
        "del_dice <骰子名>\n"
        "dice_list\n"
        "\n"
        "=== 卡组功能 ===\n"
        "add_deck / 添加卡组 <卡组名> <卡1> <卡2> ...\n"
        "del_deck / 删除卡组 <卡组名>\n"
        "config_deck / 配置卡组 <卡组名> [shuffle_on_init=true/false]\n"
        "deck_list / 卡组列表\n"
        "draw / draw_top / 顶部抽卡 / 抽卡 <卡组名> [数量=1]\n"
        "draw_bottom / 底部抽卡 <卡组名> [数量=1]\n"
        "shuffle / 洗混 <卡组名>\n"
        "put_top / 放顶部 <卡组名> <卡1> [卡2] ...\n"
        "put_bottom / 放底部 <卡组名> <卡1> [卡2] ...\n"
        "reset_deck / 重置卡组 <卡组名>\n"
        "view_deck / 查看卡组 <卡组名>\n"
        "\n"
        "卡片格式：标记1|标记2|..."
    ),
    type="application",
    homepage="https://github.com/CaptainDemo/nonebot-plugin-dice-helper",
    config=DiceHelperConfig,
    supported_adapters={"~onebot.v11"},
)

from . import roll
from . import draw
