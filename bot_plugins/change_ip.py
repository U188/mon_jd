import os
from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
import time, re
path=os.path.join(os.path.dirname(__file__) +'/../../../conf/config.yaml')
def g_ip():
	with open (path,'r',encoding="utf-8") as f:
		f=f.read()
		regex1 = re.compile(r"(?<=address: http:\/\/).+?(?=:)", re.M)
		address = re.findall(regex1, f)
		address1=sorted(set(address),key=address.index)
		num=len(address1)
		return num,address1

def alter(file,old_ip,new_ip):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_ip in line:
                line = line.replace(old_ip,new_ip)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)
@on_command('ip', aliases=('IP', '更换ip'))
async def ssss(session: CommandSession):
	num,address=g_ip()
	await session.send(f'共检测到你有{num}个ip地址')
	time.sleep(1)
	for n in range(num):
		new_ip = await session.aget(prompt=f'请输入第{n+1}个更换的ip地址')
		ip=re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
		if re.match(ip,new_ip):
			alter(path,address[n],new_ip)
			await session.send('更换成功')
		else:
			await session.send(f'错误ip地址，再见！')
			break