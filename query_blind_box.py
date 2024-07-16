from typing import Tuple, Any
from protocol_adapter.adapter_type import AdapterMessageEvent
from protocol_adapter.protocol_adapter import ProtocolAdapter
from nonebot import on_regex
from . import data
from nonebot.params import RegexGroup
from utils.permission import white_list_handle


query_blind_box = on_regex(
    pattern=r"^(.*)盲盒( +[0-9]+|$)",
    priority=5,
)

query_blind_box.__doc__ = """盲盒"""
query_blind_box.__help_type__ = None

query_blind_box.handle()(white_list_handle("blind_box"))


@query_blind_box.handle()
async def _(
        event: AdapterMessageEvent,
        params: Tuple[Any, ...] = RegexGroup(),
):
    blind_box_name = params[0]
    try:
        if len(params[1]) == 0:
            blind_box_count = 1
        else:
            blind_box_count = int(params[1])
    except ValueError:
        return await query_blind_box.finish(ProtocolAdapter.MS.reply(event) + ProtocolAdapter.MS.text("抽取次数未输入或输入错误！"))
    if blind_box_count < 0:
        return await query_blind_box.finish(ProtocolAdapter.MS.reply(event) + ProtocolAdapter.MS.text("抽取次数不能为负！"))
    if blind_box_count > 10000000:
        return await query_blind_box.finish(ProtocolAdapter.MS.reply(event) + ProtocolAdapter.MS.text("抽取次数过多！"))
    bonus_info = data.random_get_box(blind_box_name + "盲盒", blind_box_count)
    if bonus_info is None:
        return await query_blind_box.finish()

    msg = ProtocolAdapter.MS.reply(event) + ProtocolAdapter.MS.text(f"打开{blind_box_name}盲盒，获得奖励：\n")
    for info in bonus_info['gift']:
        msg += ProtocolAdapter.MS.text(f"{info['name']} × {info['count']}，"
                                       f"价值{info['price']}{bonus_info['price']['unit']}\n")

    msg += ProtocolAdapter.MS.text(f"\n本次盲盒总计抽得价值{bonus_info['price']['earn']}{bonus_info['price']['unit']}的道具，"
                                   f"{'净赚' if bonus_info['price']['win'] >= 0 else '亏损'}"
                                   f"{abs(bonus_info['price']['win'])}{bonus_info['price']['unit']}\n")
    await query_blind_box.finish(msg)
