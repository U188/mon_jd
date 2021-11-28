#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests,time,re
import os,sys
from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
import time, re
path=os.path.join(os.path.dirname(__file__))
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
def get_url():
    url='http://api.qemao.com/api/douyin/'
    s= requests.get(url,headers=headers,allow_redirects=True)
    return s.url
def dowm_load(url,name):
    movie_url = url
    movie_name = name
    downsize = 0
    #print('开始下载')
    startTime = time.time()
    req = requests.get(movie_url, headers=headers, stream=True, verify=False,timeout=120)
    file_size = int(req.headers['content-length'])
    with(open(path+'/vido/'+movie_name + '.mp4', 'wb')) as f:
        for chunk in req.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
                downsize += len(chunk)
                do_size = (downsize / file_size)*100
                line = 'downloading %d KB/s - %.2f MB，已完成%d%%'
                line = line%(downsize/1024/(time.time()-startTime),downsize/1024/1024,do_size)
        if '100%' in line:
            return True
        else:
            return False

def move_vido(name):
    os.remove(name)
    #print(f'已移除{name}')

@on_command('扭一扭', aliases=('抖音', '小姐姐'))
async def ssss(session: CommandSession):
    url=get_url()
    name=re.findall(r'(?<=\/lib\/).+(?=.mp4)',url)[0]
    do_load=dowm_load(url,name)
    if do_load:
        vido_path=f'{path}/vido/{name}.mp4'
        await session.send('[CQ:video,file=file:///{}]'.format(vido_path))
        time.sleep(30)
        move_vido(vido_path)
    else:
        await session.send('下载出错啦！')
