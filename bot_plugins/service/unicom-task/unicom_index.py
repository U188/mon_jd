# -*- coding: utf-8 -*-
#unicom_config="13091159008<<<552297<<<1f7af72ad6912d306b5053abf90c7ebb736685d153b12c307c805ac0e85a16ae12911a5f207aaa59d0ca46960d72fc1c7b1a3bf3b2adf08ee9e48b60770cfd02<<<0<<<https://nyan.mail.wo.cn/cn/sign/index/index?mobile=4pc6Zs5%2BagNPrzvmxwW2Qw%3D%3D&userName=&openId=BesstOGVUgidLpXxOPzihNLJt3d3zj39qYUpkDCevYo%3D<<<WOWlove123"
import schedule
import os,sys
import requests
import datetime
sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/task')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/tenscf_rely')
import json,time,re,traceback,random,datetime,util,sys,login,logging
import pytz,importlib,requests,rsa,lxml
try:
    from lxml.html import fromstring
except Exception as e:
    print(str(e) + "\n缺少lxml,pytz,requests,rsa模块中的一个, 请执行命令：pip3 install xxx\n")
requests.packages.urllib3.disable_warnings()
client = None

try:
    from unicom_json import accounts

    lists = accounts
except Exception as error:
    print(f'失败原因:{error}')
    lists = []
   
#日志基础配置
def log():
    # 创建一个logger
    global logger,logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 创建一个handler，用于写入日志文件
    # w 模式会记住上次日志记录的位置
    fh = logging.FileHandler('log.txt', mode='a', encoding='utf-8')
    fh.setFormatter(logging.Formatter("%(filename)s: %(message)s"))
    logger.addHandler(fh)
    # 创建一个handler，输出到控制台
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(filename)s: %(message)s"))
    logger.addHandler(ch)
log() 


#读取用户配置信息
#错误原因有两种：格式错误、未读取到错误
def readJson(unicom_config):
    try:
        users=list()
        user_list=[v for v in unicom_config.split('<<<')]
        print(user_list)
        user_dict={
            "username": user_list[0],
            "password": user_list[1],
            "appId": user_list[2],
        }
        if len(user_list) > 3:
            if user_list[3] and user_list[3] != '0' and user_list[3] != ' ' :
                user_dict['lotteryNum']=user_list[3]
        if len(user_list) > 4:
            if user_list[4] and user_list[4] != ' ' :
                user_dict['woEmail']=user_list[4]
        if len(user_list) > 5:
            if user_list[5] and user_list[5] != ' ' :
                user_dict['woEmail_password']=user_list[5]                
        users.append(user_dict)
        return users
    except:
        logging.error('变量填写错误')

#运行任务
def runTask(client, user):
    with os.scandir(os.path.abspath(os.path.dirname(__file__))+'/task') as entries:
        try:
            for entry in entries:
                if entry.is_file():
                    if entry.name == '__init__.py':
                        continue
                    if entry.name == 'login.py':
                        continue
                    if entry.name == 'sendNotify.py':
                        continue
                    if entry.name == 'util.py':
                        continue 
                    if entry.name == 'rsa':
                        continue       
                    if entry.name == 'rsa-4.7.2.dist-info':
                        continue  
                    if entry.name == '__pycache__':
                        continue  
                    if entry.name == 'turntable_lottery.py':
                        continue 
                    # if entry.name != 'everyday_way.py':
                    #     continue  
                    task_module = importlib.import_module('task.'+entry.name[:-3])
                    task_class = getattr(task_module, entry.name[0:-3])
                    task_obj = task_class()
                    task_obj.run(client, user)
                    message=read_log()
        except Exception as e:
            print(e)
    send_qq('531762900',message)
def send_qq(qqgroup,mess):
    QQurl=f"http://127.0.0.1:6547/send_group_msg?group_id={qqgroup}&message={mess}"
    try:
        print("\n")
        if not QQurl:
            print("QQ服务的token未设置!!\n取消推送")
            return
        print("QQ服务启动")
        response = requests.get(url=QQurl).json()
        print(response)
        if response['status'] == 'ok':
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)

def read_log():
    content = ''
    with open('log.txt', encoding='utf-8') as f:
            for line in f.readlines():
                content += line
    return content


def main_handler():
    global lists
    for each in lists:
        if each['unicom_config'] != '':
            unicom_config=each['unicom_config']
            users = readJson(unicom_config)
            #print(users)
            for user in users:
                # 清空上一个用户的日志记录
                with open('log.txt',mode='w',encoding='utf-8') as f:
                    pass
                global client
                client = login.login(user['username'],user['password'],user['appId'])
                #获取账户信息
                util.getIntegral(client)
                if client != False:
                    runTask(client, user)
    '''
#主函数入口
if __name__ == '__main__':
    main_handler()
'''
schedule.every().day.at("08:30").do(main_handler)
#schedule.every().day.at("12:00").do(main_handler)
while True:
    print(datetime.datetime.now())
    schedule.run_pending()
    time.sleep(1800)
