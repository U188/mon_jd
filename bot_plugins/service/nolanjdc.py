import requests
uu='nolanjdc地址' #jdc地址如http://asadasd:5701
def sendsms(phone):
    url=f'{uu}/api/SendSMS'
    data={
        'Phone':phone,
        'qlkey':0
    }
    result=requests.post(url,json=data)
    return result.json()['message']
    
def AutoCaptcha(phone):
    url=f'{uu}/api/AutoCaptcha'
    data={
        'Phone':phone
    }
    result=requests.post(url,json=data,timeout=240)
    return result.json()['success']

def VerifyCode(phone,qq,code):
    url=f'{uu}/api/VerifyCode'
    qq=str(qq)
    data={
        'Phone':phone,
        'QQ':qq,
        'qlkey':0,
        'Code':code
    }
    result=requests.post(url,json=data)
    return result.json()['message']
