from nonebot.plugin import PluginMetadata
from nonebot import get_driver
from .config import DiceHelperConfig

__plugin_meta__ = PluginMetadata(
    name="Dice Helper",
    description="桌游辅助插件：投骰子、自定义骰子",
    usage=(
        "roll / 投掷 <参数>\n"
        "add_dice <骰子名> <面1> <面2> ...\n"
        "del_dice <骰子名>\n"
        "dice_list"
    ),
    type="application",
    homepage="https://github.com/CaptainDemo/nonebot-plugin-dice-helper",
    config=DiceHelperConfig,
    supported_adapters={"~onebot.v11"},
)

driver = get_driver()
plugin_config = DiceHelperConfig.model_validate(
    driver.config.model_dump()
)

from . import roll  # noqa
