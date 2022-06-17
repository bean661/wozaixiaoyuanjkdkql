# -*- encoding:utf-8 -*-
"""
cron: 0 22 * * *
new Env('我在校园晚检');
"""

import datetime
import os
import requests
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
        # mark 晚签用户昵称
        self.mark = item['mark']
        #jwsession
        self.jwsession = ""
        # 学校晚签时段
        self.seqs = []
        # 晚签结果
        self.status_code = 0
        # id 和signid 等self.sign_message
        self.sign_message = ""
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
    def geoCode(self, url,params):
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
        elif not os.path.exists('.cache/' + str(self.data["username"]) + ".json"):
            print("正在创建cache文件...")
            data = {"jwsession": self.jwsession}
        # 如果找到cache,读取cache并更新jwsession
        else:
            print("找到cache文件，正在更新cache中的jwsession...")
            data = processJson('.cache/' + str(self.data["username"]) + ".json").read()
            data['jwsession'] = self.jwsession
        processJson('.cache/' + str(self.data["username"]) + ".json").write(data)
        self.jwsession = data['jwsession']

    # 获取JWSESSION
    def getJwsession(self):
        if not self.jwsession:  # 读取cache中的配置文件
            data = processJson('.cache/' + str(self.data["username"]) + ".json").read()
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
            "latitude": location[1],
            "longitude": location[0],
            "country": '中国',
            "city": _res['city'],
            "district": _res['district'],
            "province": _res['province'],
            "township": _res['township'],
            "street": _res['streetNumber']['street'],
            "id": self.sign_message['logId'],
            "signId": self.sign_message['id'],
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
        print(res)
        if res["code"] == 0:
            self.jwsession = response.headers['JWSESSION']
            self.setJwsession()
            return True
        else:
            print("登录失败，请检查账号信息" + str(res))
            self.status_code = 5
            return False

    # 判断当前时间段是否可以晚签
    def timeTF(self):
        # 检测当前时间段 先关了
        time_now = time.strftime("%H:%M:%S", time.localtime())
        time_list = time_now.split(":")
        if time_list[0] != '11':
            print("不在晚签时间段,请换时间晚签")
            self.status_code = 3
            return True
        else:
            print("在晚签时间段 开始晚签")
            return True

    # 获取晚签列表，符合条件则自动进行晚签
    def PunchIn(self):
        # 先判断 再晚签
        # if self.timeTF():
        if self.timeTF():
            headers = {
                "jwsession": self.getJwsession()
            }
            post_data = {
                "page": 1,
                "size": 5
            }
            url = "https://student.wozaixiaoyuan.com/sign/getSignMessage.json"
            s = requests.session()
            r = s.post(url, data=post_data, headers=headers)
            res = json.loads(r.text)
            if res['code'] == -10:
                print('jwsession 无效，尝试账号密码晚签')
                self.status_code = 4
                loginStatus = self.login()
                if loginStatus:
                    print("登录成功")
                    self.PunchIn()
                else:
                    print("登录失败")
            elif res['code'] == 0:
                self.sign_message = res['data'][0]
                print("开始晚签")
                self.doPunchIn()

    # 晚签
    def doPunchIn(self):
        headers = {
            "jwsession": self.getJwsession()
        }
        post_data = self.requestAddress(self.data['location'])

        url = "https://student.wozaixiaoyuan.com/sign/doSign.json"
        s = requests.session()
        self.sign_data = post_data
        r = s.post(url, data=json.dumps(post_data), headers=headers)
        r_json = json.loads(r.text)
        if r_json['code'] == 0:
            self.status_code = 1
            print("签到提醒", "签到成功")
            if self.pushPlus_data['onlyWrongNotify'] == "false":
                self.sendNotification()

        else:
            self.status_code = 5
            print("签到提醒", "签到失败,返回信息为:" + str(r_json))
            self.sendNotification()

    # 获取晚签结果
    def getResult(self):
        res = self.status_code
        if res == 1:
            return "✅ 晚签成功"
        elif res == 2:
            return "✅ 你已经晚签了，无需重复晚签"
        elif res == 3:
            return "❌ 晚签失败，当前不在晚签时间段内"
        elif res == 4:
            return "❌ 晚签失败，jwsession 无效"
        elif res == 5:
            return "❌ 晚签失败，登录错误，请检查账号信息"
        else:
            return "❌ 晚签失败，发生未知错误"

    # 推送晚签结果
    def sendNotification(self):
        notifyResult = self.getResult()
        # pushplus 推送
        url = 'http://www.pushplus.plus/send'
        notifyToken = self.pushPlus_data['notifyToken']
        content = json.dumps({
            "晚签用户": self.mark,
            "晚签项目": "晚签",
            "晚签情况": notifyResult,
            "晚签信息": self.sign_data,
            "晚签时间": time.strftime("%Y-%m-%d %H:%M:%S", (time.localtime())),
        }, ensure_ascii=False)
        msg = {
            "token": notifyToken,
            "title": "⏰ 我在校园晚签结果通知",
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
            client_priv_key = os.getenv('wzxy_wq_config' + str(i), 'null')
            if client_priv_key == 'null':
                print('打卡完毕，共' + str(i) + "个账号。")
                break
            configs = os.environ['wzxy_wq_config' + str(i)]
            configs = json.loads(configs)
            print("开始打卡用户：" + configs["mark"])
            wzxy = WoZaiXiaoYuanPuncher(configs)
            # 如果没有 jwsession，则 登录 + 晚签
            if os.path.exists('.cache/'+str(configs["wozaixiaoyuan_data"]["username"])+".json") is False:
                print("找不到cache文件，正在使用账号信息登录...")
                loginStatus = wzxy.login()
                if loginStatus:
                    print("登录成功,开始晚签")
                    wzxy.PunchIn()
                else:
                    print("登录失败")
            else:
                print("找到cache文件，正在使用jwsession晚签")
                wzxy.PunchIn()
        except Exception as e:
            print("账号"+str(i+1)+"信息异常")
