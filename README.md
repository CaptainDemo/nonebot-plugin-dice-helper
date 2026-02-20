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

可以自定义骰子的骰子插件

add_dice 攻击 未命中 命中 命中|命中

roll 攻击 2d6<br>
骰子结果<br>
攻击 ×1：命中|命中<br>
d6 ×2：2，1<br>
合计3，2命中

代码我让AI写的，检查了下大致没问题

以后再添加抽卡，抽盲袋等方法

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

可以在nonebot_plugin_localstore的plugin_config_dir里面建立一个default_data.json，配置全局的自定义骰子(不能被命令删除)。
格式如下
```json5
{
  "custom_dice": {
    "硬币": [
      [
        "正面"
      ],
      [
        "反面"
      ]
    ]
  }
}
```

## 🎉 使用
### 指令表
|    指令     | 权限(私聊不需要) | 需要@ |  范围   |                                         说明                                         |
|:---------:|:---------:|:----:|:-----:|:----------------------------------------------------------------------------------:|
|   roll/投掷   |    群员     | 否 | 群聊/私聊 |  投指定骰子<br/>参数为 数量骰子名1 数量骰子名2...<br/>数量1可以省略<br/>dn为数字骰，不需要定义 <br/>eg. roll 4d6 硬币  |
| dice_list |    群员     | 否 | 群聊/私聊 |                                       查看所有骰子                                       |
| add_dice  | 群管理/超级用户  | 否  | 群聊/私聊 | 增加自定义骰子<br/>参数为 骰子名 面1 面2...<br/>一面可以有多个标记，用\|隔开<br/>eg. add_dice 攻击 未命中 命中 命中\|命中 |
| del_dice  | 群管理/超级用户  | 否 | 群聊/私聊 |                                      删除自定义骰子                                       |
### 效果图
有时间上传

## 🧪 测试

本项目包含完整的本地测试套件，可以验证骰子插件的核心功能。

### 安装测试依赖

```bash
pip install pytest pytest-mock pytest-cov pytest-asyncio
```

### 运行测试

```bash
# 使用测试脚本运行所有测试
python run_tests.py

# 或者直接使用 pytest
pytest tests/

# 运行特定模块的测试
python run_tests.py test_utils
python run_tests.py test_dice_logic
python run_tests.py test_dice_management

# 查看测试示例
python tests/example_usage.py
```

### 测试覆盖

- **test_utils.py**: 测试参数解析和前缀扰动功能
- **test_dice_logic.py**: 测试骰子投掷逻辑和结果格式化
- **test_dice_management.py**: 测试骰子管理和会话隔离

详细的测试说明请查看 [README_TEST.md](./README_TEST.md)
