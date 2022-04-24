import json
import datetime
import time
import random
import requests



def checkToYMD(str):
#     print(type(str))
# #date zhuan  str
#     dc = str.strftime("%Y-%m-%d %H:%M:%S")
    dd = '2022-04-14 00:00'
    print(dd, type(dd))
    dd = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S").date()
    print(dd,type(dd))
    date = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S').date()
    print(date)
# 获取随机温度
def getRandomTemprature(temperature):
  if temperature.find('~') == -1:
      return str(float(temperature))
  else:
      scope = temperature.split('~')
      random.seed(time.ctime())
      return "{:.1f}".format(random.uniform(float(scope[0]),float(scope[1])))

# 地理/逆地理编码请求
def geoCode(url,params):  
  _params = {
    **params,
    "key": "819cfa3cf713874e1757cba0b50a0172",         
  }
  response = requests.get(url=url, params=_params)
  res = json.loads((response.text))
  return res

# 读写 json 文件
class processJson:
  def __init__(self,path):
    self.path = path

  def read(self):
    with open(self.path,'rb') as file:
        data = json.load(file)
    file.close()
    return data
  
  def write(self,data):
    with open(self.path,'w',encoding='utf-8') as file:   
        json.dump(data,file,ensure_ascii = False,indent = 2)
    file.close()
   

