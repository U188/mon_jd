# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 22:30
# @Author  : wuye9999
# 沃邮箱
import os,sys
sys.path.append('/tmp')
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/task')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'/tenscf_rely')
import requests,login,logging,urllib.parse,util,re

class email_task:
    def dotask(self, email):
        try:
            try:
                url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.2967650751258384"
                res = email.post(url=url).json()
                logging.info(f"【沃邮箱签到】: 已连续签到{res['result']['keepSign']}天")
            except:
                logging.info('【沃邮箱签到】: 查询签到天数错误')

            url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
            res = email.post(url=url).json()
            result = res.get("result")
            if result == -2:
                logging.info("【沃邮箱签到】: 已签到")
            elif result is None:
                logging.info("【沃邮箱签到】: 签到失败")
            else:
                logging.info(f"【沃邮箱签到】: 签到成功~已签到{result}天！")
        except Exception as e:
            logging.info(f"【沃邮箱签到】: 错误 \n{e}")
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            data_params = {
                "沃邮箱每日首次登录": {"taskName": "loginmail"},
                "浅秋领福利": {"taskName": "clubactivity"},
                "下载沃邮箱app": {"taskName": "download"},
                "去用户俱乐部逛一逛": {"taskName": "club"},
            }
            for key, data in dict.items(data_params):
                try:
                    res = email.post(url=url, data=data).json()
                    result = res.get("result")
                    if result == 1:
                        logging.info(f"【{key}】: 做任务成功")
                    elif result == -1:
                        logging.info(f"【{key}】: 任务已做过")
                    elif result == -2:
                        logging.info(f"【{key}】: 请检查登录状态")
                    else:
                        logging.info(f"【{key}】: 未知错误")
                except Exception as e:
                    logging.info(f"【沃邮箱】: 沃邮箱执行任务【{key}】错误\n{e}")
        except Exception as e:
            logging.info(f"【沃邮箱】: 沃邮箱执行任务错误\n{e}")

    def dotask_2(self, email):
        #查询签到天数
        try:
            url = "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/query-continuous-sign-record"
            res = email.get(url=url).text
            newContinuousDay=re.findall(r'"newContinuousDay":(.*?),', res)
            logging.info(f'【沃邮箱】: 已连续签到 {newContinuousDay[0]} 天')
        except Exception as e:
            logging.info(f'【沃邮箱】: 查询签到天数错误 \n{e}')
            
        try:
            #任务签到
            url = 'https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create?channelId='
            res = email.get(url=url).json()
            logging.info(f"【沃邮箱】: 成长值签到结果: {res['description']}")
        except Exception as e:
            logging.info(f'【沃邮箱】: 签到失败 \n{e}')

        #积分任务
        try:
            url = 'https://club.mail.wo.cn/clubwebservice/growth/queryIntegralTask'
            res = email.get(url=url).json()
            for data in res['data']:
                if data['irid'] == None or data['irid'] == 339 or data['taskState'] == 1:
                    logging.info(f"【沃邮箱】: 跳过{data['resourceName']}")
                    continue
                url = 'https://club.mail.wo.cn/clubwebservice/growth/addIntegral?resourceType='+urllib.parse.quote(str(data['resourceFlag']))
                ress = email.get(url=url).json()
                logging.info(f"【沃邮箱】: 执行任务: {data['resourceName']} ")
                logging.info(f"【沃邮箱】: 状态: {ress['description']}")
        except Exception as e:
            logging.info(f'【沃邮箱】: 积分任务出错 \n{e}')

        #成长值任务
        try:
            url = 'https://club.mail.wo.cn/clubwebservice/growth/queryGrowthTask'
            res = email.get(url=url).json()
            for data in res['data']:
                if data['irid'] == None or data['irid'] == 576 or data['taskState'] == 1:
                    logging.info(f"【沃邮箱】: 跳过{data['resourceName']}")
                    continue
                url = 'https://club.mail.wo.cn/clubwebservice/growth/addGrowthViaTask?resourceType='+urllib.parse.quote(str(data['resourceFlag']))
                ress = email.get(url=url).json()
                logging.info(f"【沃邮箱】: 执行任务: {data['resourceName']}")
                logging.info(f"【沃邮箱】: 状态: {ress['description']}")
        except Exception as e:
            logging.info(f'【沃邮箱】: 成长值任务出错 \n{e}')

    def dotask_3(self,email,uid,sid):
        #app
        upcookies=requests.utils.cookiejar_from_dict({
            'Coremail.sid': sid,
            'domain':'domain=mail.wo.cn',
        }) 
        email.cookies.update(upcookies)      
        email.headers.update({
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "com.asiainfo.android"
        }) 
        #增加积分
        try:
            integral_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
            }
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"integral"}
                res = email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】：{key}app积分结果:{res['code']}")
        except Exception as e:
            logging.info(f'【沃邮箱扩展任务】：app沃邮箱执行任务错误\n{e}')

        #增加成长值
        try:
            growth_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
            }            
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"growth"}
                res = email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】：{key}app成长值结果:{res['code']}")
        except Exception as e:
            logging.info(f'【沃邮箱扩展任务】：app沃邮箱执行任务错误\n{e}')

        #网页
        upcookies=requests.utils.cookiejar_from_dict({
            'CoremailReferer':'https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Fhxphone%2F',
        }) 
        email.cookies.update(upcookies) 
        email.headers.update({
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "com.tencent.mm",
        })
        #增加积分
        try:
            integral_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
                "上传文件到中转站": 'uploadFile',
            }            
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"integral"}
                res = email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】：{key}网页端积分结果:{res['code']}")
        except Exception as e:
            logging.info(f'【沃邮箱扩展任务】：网页端沃邮箱执行任务错误\n{e}')
                
        #增加成长值
        try:
            growth_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
                "上传文件到中转站": 'uploadFile',
            }   
            for key, userAction in integral_data.items():             
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"uid": uid,"userAction":userAction,"userType":"growth"}
                res = email.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】：{key}网页端成长值结果:{res['code']}")
        except Exception as e:
            logging.info(f'【沃邮箱扩展任务】：网页端沃邮箱执行任务错误\n{e}')

        #电脑
        upcookies=requests.utils.cookiejar_from_dict({
            'domain':'',
            'CoremailReferer':'https%3A%2F%2Fmail.wo.cn%2Fcoremail%2Findex.jsp%3Fcus%3D1'
        }) 
        email.cookies.update(upcookies)         
        email.headers.update({
            "Origin": "https://mail.wo.cn",
            "X-Requested-With": "XMLHttpRequest",
        })
        #增加积分
        try:
            integral_data = {
                "每日登录": 'login',
                "发送邮件": 'sendMail',
                "查看邮件": 'listMail',
                "登录百度网盘": 'baiduCloud',
                "新建日程": 'createCal',
                "上传文件到中转站": 'uploadFile',
            }            
            for key, userAction in integral_data.items():
                url = f'https://mail.wo.cn/coremail/s/?func=club:addClubInfo&sid={sid}'
                data = {"userAction":userAction}
                response = requests.post(url=url,json=data).json()
                logging.info(f"【沃邮箱扩展任务】：{key}电脑端积分结果:{res['code']}")
        except Exception as e:
            logging.info(f'【沃邮箱扩展任务】：电脑端沃邮箱执行任务错误\n{e}')

    def run(self, client, user):
        if "woEmail" not in user:
            return False
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(user['woEmail']).query))
        params = (
            ('mobile', query['mobile'].replace(' ', '+')),
            ('userName', ''),
            ('openId', query['openId'].replace(' ', '+')),
        )

        with requests.Session() as email:
            url='https://nyan.mail.wo.cn/cn/sign/index/index'
            email.get(url=url, headers=headers, params=params)
            self.dotask(email)

        with requests.Session() as email:
            url="https://club.mail.wo.cn/clubwebservice"
            email.get(url=url, headers=headers, params=params)
            self.dotask_2(email)

        with requests.Session() as email:
            url="https://mail.wo.cn/coremail/s/json?func=user:login"
            try:
                woEmail_uid=user['username']+'@wo.cn'
                woEmail_password=user['woEmail_password']
            except:
                logging.info("【沃邮箱扩展任务】：未找到沃邮箱密码")
                return
            email.headers.update({
                    "Accept": "text/x-json",
                    "Content-Type": "text/x-json",
                    "X-CM-SERVICE": "PHONE",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
            })
            data={"uid": woEmail_uid, "password": woEmail_password}
            res=email.post(url=url, json=data).json()
            logging.info(f"【沃邮箱扩展任务】：登录沃邮箱结果 {res['code']}")
            try:
                self.dotask_3(email,res['var']['uid'],res['var']['sid'])
            except:
                logging.info(f"【沃邮箱扩展任务】：登录失败，沃邮箱扩展任务跳过")


