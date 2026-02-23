<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-dice-helper

_✨ NoneBot 可自定义骰子的骰子插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/CaptainDemo/nonebot-plugin-dice-helper.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-dice-helper">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-dice-helper.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

可以自定义骰子和卡组的桌面游戏辅助插件

### 骰子功能示例

add_dice 攻击 未命中 命中 命中|命中

roll 攻击 2d6<br>
骰子结果<br>
攻击 ×1：命中|命中<br>
d6 ×2：2，1<br>
合计3，2命中

### 卡组功能示例

add_deck 扑克牌 黑桃1|黑桃 黑桃K|黑桃 红心1|红心 红心K|红心

draw 扑克牌 2<br>
抽卡结果（扑克牌 ×2）：<br>
1. 黑桃1, 黑桃<br>
2. 红心K, 红心<br>
<br>
标记统计：<br>
黑桃1 ×1、黑桃 ×1、红心K ×1、红心 ×1<br>
<br>
剩余：2张

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-dice-helper

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-dice-helper
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-dice-helper
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-dice-helper
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-dice-helper
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-dice-helper"]

</details>

## ⚙️ 配置

可以在nonebot_plugin_localstore的plugin_config_dir里面建立一个default_data.json，配置全局的自定义骰子和卡组(不能被命令删除)。
格式如下
```json5
{
  "custom_dice": {
    "硬币": [
      ["正面"],
      ["反面"]
    ]
  },
  "card_decks": {
    "扑克牌": {
      "cards": [
        ["黑桃1", "黑桃"],
        ["黑桃K", "黑桃"],
        ["红心1", "红心"],
        ["红心K", "红心"]
      ],
      "shuffle_on_init": true  // 可选，默认true，设为false时创建/重置保持固定顺序
    }
  }
}
```

## 🎉 使用
### 骰子指令
|    指令     | 权限(私聊不需要) | 需要@ |  范围   |                                         说明                                         |
|:---------:|:---------:|:----:|:-----:|:----------------------------------------------------------------------------------:|
|   roll/投掷   |    群员     | 否 | 群聊/私聊 |  投指定骰子<br/>参数为 数量骰子名1 数量骰子名2...<br/>数量1可以省略<br/>dn为数字骰，不需要定义 <br/>eg. roll 4d6 硬币  |
| dice_list |    群员     | 否 | 群聊/私聊 |                                       查看所有骰子                                       |
| add_dice  | 群管理/超级用户  | 否  | 群聊/私聊 | 增加自定义骰子<br/>参数为 骰子名 面1 面2...<br/>一面可以有多个标记，用\|隔开<br/>eg. add_dice 攻击 未命中 命中 命中\|命中 |
| del_dice  | 群管理/超级用户  | 否 | 群聊/私聊 |                                      删除自定义骰子                                       |

### 卡组指令
|       指令       | 权限(私聊不需要) | 需要@ |  范围   |                                         说明                                         |
|:--------------:|:---------:|:----:|:-----:|:----------------------------------------------------------------------------------:|
|  deck_list/卡组列表  |    群员     | 否 | 群聊/私聊 |                                       查看所有卡组                                       |
| add_deck/添加卡组  | 群管理/超级用户  | 否  | 群聊/私聊 | 增加自定义卡组<br/>参数为 卡组名 卡1 卡2...<br/>每张卡可以有多个标记，用\|隔开<br/>eg. add_deck 扑克牌 黑桃1\|黑桃 红心K\|红心 |
|  del_deck/删除卡组  | 群管理/超级用户  | 否 | 群聊/私聊 |                                      删除自定义卡组                                       |
| config_deck/配置卡组 | 群管理/超级用户  | 否 | 群聊/私聊 |          配置卡组参数<br/>eg. config_deck 扑克牌 shuffle_on_init=false<br/>设为false时创建/重置保持固定顺序          |
| draw_top/顶部抽卡/抽卡/draw  |    群员     | 否 | 群聊/私聊 |                 从卡组顶部抽卡<br/>参数为 卡组名 [数量=1]<br/>eg. draw 扑克牌 2                 |
| draw_bottom/底部抽卡 |    群员     | 否 | 群聊/私聊 |                 从卡组底部抽卡<br/>参数为 卡组名 [数量=1]<br/>eg. draw_bottom 扑克牌 1                 |
|  shuffle/洗混   |    群员     | 否 | 群聊/私聊 |                             打乱卡组顺序<br/>参数为 卡组名<br/>eg. shuffle 扑克牌                             |
|  put_top/放顶部   |    群员     | 否 | 群聊/私聊 |          将卡牌放入卡组顶部<br/>参数为 卡组名 卡1 [卡2]...<br/>eg. put_top 扑克牌 黑桃1\|黑桃           |
|  put_bottom/放底部  |    群员     | 否 | 群聊/私聊 |          将卡牌放入卡组底部<br/>参数为 卡组名 卡1 [卡2]...<br/>eg. put_bottom 扑克牌 红心K\|红心          |
| reset_deck/重置卡组 |    群员     | 否 | 群聊/私聊 |                          恢复卡组到初始状态<br/>参数为 卡组名<br/>eg. reset_deck 扑克牌                          |
| view_deck/查看卡组 |    群员     | 否 | 群聊/私聊 |                     查看卡组剩余卡牌<br/>超过20张时显示前后各10张<br/>eg. view_deck 扑克牌                     |

### 效果图
有时间上传
