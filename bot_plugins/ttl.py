from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
import time, re
import os
global lists
try:
    from bot_plugins.service.ttl_json import accounts
    lists = accounts
except Exception as error:
    print(f'失败原因:{error}')
    lists = []
qqnums=['','']

@on_command('话费车', aliases=('太太乐', 'ttl'))
async def ssss(session: CommandSession):
    #ipone = session.current_arg_text.strip()
    if True:
        qqnum = str(session.ctx['user_id'])

        if qqnum not in qqnums:
            await session.send('您没有话费车权限，需要上车请联系群主！')
        else:
            qqs=[]
            for list in lists:
                qqs.append(list['qq'])
            if qqnum in qqs:
                await session.send('您已经有号码记录了，需要多号请联系群主！')
            else:
                ipone = await session.aget(prompt='请输入手机号码:')
                phone = re.compile(
'^(13(0|1|2|3|7|8|9|6|5|4)|16(0|1|2|3|7|8|9|6|5|4)|17(0|8|5|6|2|3|7)|18(0|1|2|3|4|5|6|7|8|9)|15(0|1|2|3|5|6|7|8|9)|19(0|1|3|8|9))\d{8}$')
                if re.match(phone, ipone):
                    passw = await session.aget(prompt='请输入密码:')
                    time.sleep(1)
                    comp = await session.aget(prompt='电信or联通or移动:')
                    time.sleep(3)
                    txt = {"qq": qqnum, "iphone": ipone, "passw": passw, "comp": comp}
                    lists.append(txt)
                    txt = f'accounts = {str(lists)}'
                    path=os.path.join(os.path.dirname(__file__) +'/service/ttl_json.py')
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(txt)
                    await session.send('写入成功！')
                else:
                    await session.send('你发的什么东西？我感觉不是手机号码.......')
                    await session.send('拜拜了您！')
