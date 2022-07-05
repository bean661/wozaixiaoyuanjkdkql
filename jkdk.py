# -*- encoding:utf-8 -*-
"""
cron: 0 8 * * *
new Env('我在校园健康打卡');
"""

import datetime
import os
import requests
from urllib.parse import urlencode
import time
import json

# 读写 json 文件
class processJson:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'rb') as file:
            data = json.load(file)
        file.close()
        return data

    def write(self, data):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        file.close()


class WoZaiXiaoYuanPuncher:
    def __init__(self, item):
        # 我在校园账号数据
        self.data = item['wozaixiaoyuan_data']
        # pushPlus 账号数据
        self.pushPlus_data = item['pushPlus_data']
        # mark 打卡用户昵称
        self.mark = item['mark']
        # answers
        if self.data['answers'] == '':
            print("未获取到用户的answers 采用默认answers：['0']打卡")
            self.answers = "['0']"
        else:
            self.answers = self.data['answers'].replace(" ", "").split(',')
        # 初始化  jwsession
        self.jwsession = ""
        # 学校打卡时段
        self.seqs = []
        # 打卡结果
        self.status_code = 0
        # 请求头
        self.header = {
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "content-type": "application/json;charset=UTF-8",
            "Content-Length": "2",
            "Host": "gw.wozaixiaoyuan.com",
            "Accept-Language": "en-us,en",
            "Accept": "application/json, text/plain, */*"
        }
        # signdata  要保存的信息
        self.sign_data = ""
        # 请求体（必须有）
        self.body = "{}"

    # 地理/逆地理编码请求
    def geoCode(self, url, params):
        url = "https://restapi.amap.com/v3/geocode/regeo"
        _params = {
            **params,
            "key": "819cfa3cf713874e1757cba0b50a0172",
        }
        response = requests.get(url=url, params=_params)
        res = json.loads((response.text))
        return res
    # 设置JWSESSION
    def setJwsession(self):
    # 如果找不到cache,新建cache储存目录与文件
        if not os.path.exists('.cache'):
            print("正在创建cache储存目录与文件...")
            os.mkdir('.cache')
            data = {"jwsession": self.jwsession}
        elif not os.path.exists('.cache/'+str(self.data["username"])+".json"):
            print("正在创建cache文件...")
            data = {"jwsession": self.jwsession}
        # 如果找到cache,读取cache并更新jwsession
        else:
            print("找到cache文件，正在更新cache中的jwsession...")
            data = processJson('.cache/'+str(self.data["username"])+".json").read()
            data['jwsession'] = self.jwsession
        processJson('.cache/'+str(self.data["username"])+".json").write(data)
        self.jwsession = data['jwsession']

    # 获取JWSESSION
    def getJwsession(self):
        if not self.jwsession:  # 读取cache中的配置文件
            data = processJson('.cache/'+str(self.data["username"])+".json").read()
            self.jwsession = data['jwsession']
        return self.jwsession
    # 请求地址信息
    def requestAddress(self, location):
        # 根据经纬度求具体地址
        url2 = 'https://restapi.amap.com/v3/geocode/regeo'
        res = self.geoCode(url2, {
            "location": location
        })
        _res = res['regeocode']['addressComponent']
        print(_res)
        location = location.split(',')
        sign_data = {
            "answers": self.answers,
            "latitude": location[1],
            "longitude": location[0],
            "country": '中国',
            "city": _res['city'],
            "district": _res['district'],
            "province": _res['province'],
            "township": _res['township'],
            "street": _res['streetNumber']['street'],
            "areacode": _res['adcode'],
            "towncode":"0",
            "citycode":"0",
            "timestampHeader":round(time.time())
        }
        return sign_data
    # 登录

    def login(self):
        # 登录接口
        loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        username, password = str(self.data['username']), str(self.data['password'])
        url = f'{loginUrl}?username={username}&password={password}'
        self.session = requests.session()
        # 登录
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        if res["code"] == 0:
            self.jwsession = response.headers['JWSESSION']
            self.setJwsession()
            return True
        else:
            print("登录失败，请检查账号信息" + str(res))
            self.status_code = 5
            return False

    # 获取打卡列表，判断当前打卡时间段与打卡情况，符合条件则自动进行打卡
    def PunchIn(self):
        url = "https://student.wozaixiaoyuan.com/health/getHealthLatest.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        self.header['content-type'] = "application/x-www-form-urlencoded"
        self.header['Content-Length'] = "0"
        self.header['JWSESSION'] = self.getJwsession()
        self.session = requests.session()
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        # 如果 jwsession 无效，则重新 登录 + 打卡
        if res['code'] == -10:
            print('jwsession 无效，尝试账号密码打卡')
            self.status_code = 4
            loginStatus = self.login()
            if loginStatus:
                print("登录成功")
                self.PunchIn()
            else:
                print("登录失败")
                self.sendNotification()
        elif res['code'] == 0:
            self.doPunchIn()

    # 打卡
    def doPunchIn(self):
        print('开始打卡，打卡信息：')
        url = "https://student.wozaixiaoyuan.com/health/save.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        self.header['content-type'] = "application/x-www-form-urlencoded"
        self.header['JWSESSION'] = self.jwsession
        sign_data = self.requestAddress(self.data['location'])
        self.sign_data = sign_data
        print(sign_data)
        data = urlencode(sign_data)
        response = self.session.post(url, data=data, headers=self.header)
        response = json.loads(response.text)
        # 打卡情况
        if response["code"] == 0:
            self.status_code = 1
            print("-------------------------打卡成功-------------------------")
            if self.pushPlus_data['onlyWrongNotify'] == "false":
                self.sendNotification()
        else:
            print(response)
            print("-------------------------打卡失败-------------------------")
            self.sendNotification()

    # 获取打卡结果
    def getResult(self):
        res = self.status_code
        if res == 1:
            return "✅ 打卡成功"
        elif res == 2:
            return "✅ 你已经打过卡了，无需重复打卡"
        elif res == 3:
            return "❌ 打卡失败，当前不在打卡时间段内"
        elif res == 4:
            return "❌ 打卡失败，jwsession 无效"
        elif res == 5:
            return "❌ 打卡失败，登录错误，请检查账号信息"
        else:
            return "❌ 打卡失败，发生未知错误"

    # 推送打卡结果
    def sendNotification(self):
        notifyResult = self.getResult()
        # pushplus 推送
        url = 'http://www.pushplus.plus/send'
        notifyToken = self.pushPlus_data['notifyToken']
        content = json.dumps({
            "打卡用户": self.mark,
            "打卡项目": "健康打卡",
            "打卡情况": notifyResult,
            "打卡信息": self.sign_data,
            "打卡时间": time.strftime("%Y-%m-%d %H:%M:%S", (time.localtime())),
        }, ensure_ascii=False)
        msg = {
            "token": notifyToken,
            "title": "⏰ 我在校园打卡结果通知",
            "content": content,
            "template": "json"
        }
        body = json.dumps(msg).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=body, headers=headers).json()
        if r["code"] == 200:
            print("消息经 pushplus 推送成功")
        else:
            print("pushplus: " + r)
            print("消息经 pushplus 推送失败，请检查错误信息")


if __name__ == '__main__':
   # 读取环境变量，若变量不存在则返回 默认值 'null'
    for i in range(200):
        try:
            client_priv_key = os.getenv('wzxy_jkdk_config'+str(i), 'null')
            if client_priv_key == 'null':
                print('打卡完毕，共'+str(i)+"个账号。")
                break
            configs = os.environ['wzxy_jkdk_config'+str(i)]
            configs = json.loads(configs)
            # answers = pre().get_answers(i)
            print("--------------开始打卡用户："+configs["mark"]+"------------------")
            wzxy = WoZaiXiaoYuanPuncher(configs)
            # 如果没有 jwsession，则 登录 + 打卡
            if os.path.exists('.cache/'+str(configs["wozaixiaoyuan_data"]["username"])+".json") is False:
                print("找不到cache文件，正在使用账号信息登录...")
                loginStatus = wzxy.login()
                if loginStatus:
                    print("登录成功,开始打卡")
                    wzxy.PunchIn()
                else:
                    print("登录失败")
            else:
                print("找到cache文件，正在使用jwsession打卡")
                wzxy.PunchIn()
        except Exception as e:
            print("账号"+str(i+1)+"信息异常"+e)