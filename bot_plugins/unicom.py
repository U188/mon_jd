# -*- coding: utf-8 -*-
from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
import time, re
import os
global lists
try:
    from bot_plugins.service.unicom_task.unicom_json import accounts
    lists = accounts
except Exception as error:
    print(f'失败原因:{error}')
    lists = []
qqnums=['12236573','1292554991','2522431854','2874637212','815548642','1754015308','78438340']

@on_command('沃联通')
async def ssss(session: CommandSession):
    check = await session.aget(prompt='你是否准备了所有东西（手机号，服务密码，appId，沃邮箱登陆Url，沃邮箱密码）:是orfor')
    if '是' in check:
        qqnum = str(session.ctx['user_id'])

        if qqnum not in qqnums and qqnum!='302761125':
            await session.send('您没有沃联通权限，需要上车请联系群主！')
        else:
            qqs=[]
            for list in lists:
                qqs.append(list['qq'])
            if qqnum in qqs and qqnum!='302761125':
                await session.send('您已经有号码记录了，需要多号请联系群主！')
            else:
                ipone = await session.aget(prompt='请输入手机号码:')
                phone = re.compile('^(13(0|1|2|3|7|8|9|6|5|4)|16(0|1|2|3|7|8|9|6|5|4)|17(0|8|5|6|2|3|7)|18(0|1|2|3|4|5|6|7|8|9)|15(0|1|2|3|5|6|7|8|9)|19(0|1|3|8|9))\d{8}$')
                if re.match(phone, ipone):
                    ser_passw = await session.aget(prompt='请输入服务密码:')
                    time.sleep(1)
                    appid = await session.aget(prompt='请输入appid:')
                    time.sleep(1)
                    if len(appid)!=128:
                        await session.send('错误appid，再见！')
                        exit()
                    womail_url1= await session.aget(prompt='请输入沃邮箱登陆Url')
                    time.sleep(1)
                    regx=re.compile(r'^https://nyan.mail.wo.cn/cn/sign/index/index.*openId.*%3D$')
                    if re.search(regx,womail_url1):
                    
                        womail_url=womail_url1.replace(' ','').replace('amp;','')
                        womail_passw = await session.aget(prompt='请输入沃邮箱登陆密码:')
                        time.sleep(3)
                        unicom_config=f'{ipone}<<<{ser_passw}<<<{appid}<<<0<<<{womail_url}<<<{womail_passw}'
                        txt = {"qq":qqnum,"unicom_config": unicom_config}
                        lists.append(txt)
                        txt = f'accounts = {str(lists)}'
                        path=os.path.join(os.path.dirname(__file__) +'/service/unicom_task/unicom_json.py')
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(txt)
                        await session.send('写入成功！')
                    else:
                        await session.send('错误URL，再见！')
                else:
                    await session.send('你发的什么东西？我感觉不是手机号码，再见！')
    else:
        await session.send('请准备好再来，再见！')
        