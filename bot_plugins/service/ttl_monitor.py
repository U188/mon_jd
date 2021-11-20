# !/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cron:  0 * * * * TimingCash.py
new Env('太太乐奖品监控');
'''
import requests, json, os,random,time,re

# 礼品代码
gift_list = ['61', '62', '631', '633']
# 导入账户
try:
    from ttl_json import accounts
    lists = accounts
except Exception as error:
    print(f'失败原因:{error}')
    lists = []

# 获取Token
def get_token(iphone, passw):
    url = 'https://www.ttljf.com/ttl_site/user.do'
    #randomn=random.randint(10000,99999)
    header={
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN'
    }
    data = {
        'device_brand': 'apple',
        'device_model': 'iPhone11, 8',
        'device_uuid': f'FCE{random.randint(10000,99999)} - 32ED - 4C1D - 97DB - 59FED8E9CC59',
        'device_version': '14.6',
        'mthd': 'login',
        'password': passw,
        'platform': 'ios',
        'sign': '47f675126adc115bc92fd6a1358028b9',
        'username': iphone
    }
    result = requests.post(url,data=data,headers=header).text
    token = json.loads(result)['user']['loginToken']
    userid = json.loads(result)['user']['userId']
    return token,userid
#定义任务头部
def head(token):
    headers= {
        'Host': 'www.ttljf.com',
        'Accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'token': token,
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxe9aa8f1c4a77ddf5/17/page-frame.html',
    }
    return headers
#做任务 任务HOST
host='https://www.ttljf.com/ttl_chefHub/'
def ttlsign(token):
    header=head(token)
    url = f'{host}user/api/sign/today'
    result = requests.put(url,headers=header).text
    message = json.loads(result)['message']
    return message
def ttlshare(token):
    header=head(token)
    url = f'{host}Common/share/A35D575F-C004-4717-AABC-ED9D1979C3FA/blog'
    body = {"id": "A35D575F-C004-4717-AABC-ED9D1979C3FA", "type": "blog"}
    result = requests.put(url,data=body,headers=header).text
    message = json.loads(result)['message']
    return message
def ttl_userinfo(token):
    header = head(token)
    url = f'{host}user/api/my'
    result = requests.get(url, headers=header).text
    integral = json.loads(result)['data']['integral']
    return integral

# 兑换礼品
def get_gift(token,userid,iphone,giftid):
    url = f'https://www.ttljf.com/ttl_site/chargeApi.do?giftId={giftid}&loginToken={token}&method=charge&mobile={iphone}&sign=47f675126adc115bc92fd6a1358028b9&userId={userid}'
    header = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN'
    }
    result = requests.get(url,headers=header).text
    r = json.loads(result)
    message = r['message']
    return message

# 获取剩余数量
def gift_count(giftid):
    url = f'https://www.ttljf.com/ttl_site/giftApi.do?giftId={giftid}&mthd=giftDetail&sign=1275eded3f5a2ddc5794d59d97e0a852&userId='
    header = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN'
    }
    result = requests.get(url,headers=header).text
    r = json.loads(result)
    count = r['gifts']['stockAmount']
    name = r['gifts']['giftName']
    return name,count

def do_task_and_get_gift(token,comp,iphone,userid):
    global messagea
    sign_mess=ttlsign(token)
    time.sleep(random.randint(2,5))
    share_mess=ttlshare(token)
    integral=ttl_userinfo(token)
    if '移动' in comp and int(integral)>=45:
        name,count=gift_count(633)
        if int(count)>0:
            messagea=get_gift(token,userid,iphone,633)
        else:
            pass
    elif '电信' in comp and int(integral)>=15:
        name, count = gift_count(631)
        if int(count) > 0:
            messagea = get_gift(token, userid, iphone, 631)
        else:
            pass
    elif '联通' in comp and int(integral)>=7:
        name, count = gift_count(62)
        if int(count) > 0:
            messagea = get_gift(token, userid, iphone, 62)
        else:
            pass
    else:
        messagea='不满足兑换条件，跳过'
    return sign_mess,share_mess,messagea

def main():
    global lists
    for each in lists:
        if each['iphone']!='' and each['passw'] != '' and each['comp'] != '':
            iphone=each['iphone']
            passw=each['passw']
            comp=each['comp']
            token,userid=get_token(iphone,passw)
            sign_mess,share_mess,messagea=do_task_and_get_gift(token,comp,iphone,userid)
            print(f'太太乐:\t每日签到：{sign_mess}\t分享任务：{share_mess}\t兑换：{messagea}')
        elif not all(each.values()):
            print("账号:空账户\t状态:跳过")
if __name__ == '__main__':
    #token,userid=get_token('13091159008','xm552297')
    #print(get_gift(token,userid,'13091159008',61))
    main()


