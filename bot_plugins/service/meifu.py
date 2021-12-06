import requests
Member_Id='2DAD09FD68E89EF658A062D1852A27FA'
Member_Token='P0P80ZJRT868B6NJ'
url='https://mobil-api.winsafe.cn/API.ashx'
header={"Accept-Encoding": "gzip,compress,br,deflate","Connection": "keep-alive","Content-Length": "193","Host": "mobil-api.winsafe.cn","Referer": "https://servicewechat.com/wxf6aa337a93d7e0a6/86/page-frame.html","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001034) NetType/WIFI Language/zh_CN","X-MXAPI-Authorization": "P0P80ZJRT868B6NJ","content-type": "application/x-www-form-urlencoded"}
def task_post2(menmber_id,member_token,task_id):

	data=f'Api_Type=mobil_tdxw_{task_id}&Member_Id={menmber_id}&Member_Token={member_token}&Activity_Id=1&Timestamp=1638774647468&App_Key=liyuan_jifen&sign=fe0f6ac6ea998a07a2cfc0e9672d7a9b'
	print(data)
	result=requests.post(url=url,data=data,headers=header).text
	print(result)
def task_post(menmber_id,member_token,task_id):

	data=f'Api_Type=mobil_tdxw_{task_id}&Member_Id={menmber_id}&Member_Token={member_token}&Timestamp=1638664197768&App_Key=liyuan_jifen&sign=030e77ae792b8507a71277463b215598'
	print(data)
	result=requests.post(url=url,data=data,headers=header).text
	print(result)
def everyday_task():
	#签到
	task_post(Member_Id,Member_Token,202)
	#抽奖
	task_post2(Member_Id,Member_Token,207)
    task_post2(Member_Id,Member_Token,207)
if __name__ == '__main__':
	everyday_task()
