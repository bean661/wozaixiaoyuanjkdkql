**目录：**

腾讯云云函数版本：

* 健康打卡：[bean661/WoZaiXiaoYuanPuncher: 我在校园自动健康打卡程序 (github.com)](https://github.com/bean661/WoZaiXiaoYuanPuncher)
* 日检日报：[bean661/WoZaiXiaoYuanDay: 我在校园 日检日报 (github.com)](https://github.com/bean661/WoZaiXiaoYuanDay)

* 晚签：[bean661/WoZaiXiaoYuan: 我在校园小程序 晚上签到 晚签 晚检 (github.com)](https://github.com/bean661/WoZaiXiaoYuan)

青龙版本：

* ：[bean661/wozaixiaoyuanjkdkql: 我在校园 健康打卡 适配青龙面板 脚本 (github.com)](https://github.com/bean661/wozaixiaoyuanjkdkql)

配置项参数介绍：（仅供参考）

仅供参考：[bean661/WoZaiXiaoYuanPuncher: 我在校园自动健康打卡程序 (github.com)](https://github.com/bean661/WoZaiXiaoYuanPuncher)



## 我在校园 **健康打卡**  **晚签**  **日检日报**

青龙面板初始配置参照教程 https://blog.csdn.net/FishBean/article/details/121819862

到2.4部分即可，2.4的拉库地址为 `ql repo https://github.com/bean661/wozaixiaoyuanjkdkql.git` 即我在校园脚本仓库。

<img src="https://gitee.com/Bean6560/images/raw/master/typora/image-20220426130306654.png" alt="drawing" width="500"/>

拉取成功如下

![image-20220426130612684](https://gitee.com/Bean6560/images/raw/master/typora/image-20220426130612684.png)

### 配置：

每个参数介绍看这个[bean661/WoZaiXiaoYuanPuncher: 我在校园自动健康打卡程序 (github.com)](https://github.com/bean661/WoZaiXiaoYuanPuncher)

填写位置：青龙面板-配置文件-config.sh 下方有最终截图

#### 单用户：

##### 健康打卡 

​	格式：

```
wzxy_jkdk_config0='
    {
        "wozaixiaoyuan_data":{
            "username": "15512345678",
            "password": "wzxywzxy",
            "location":"133.333333,33.333333",
            "answers":"0,2,36.5,2,7"
        },
        "pushPlus_data":{
            "notifyToken" : "4d25976cc88888ae8f8688889780bfe1",
            "onlyWrongNotify" : "false"
        },
        "mark": "Bean"
    }
'
```


##### 日检日报

​	格式：

```
wzxy_rjrb_config0='
    {
        "wozaixiaoyuan_data":{
            "username": "15512345678",
            "password": "wzxywzxy",
            "location":"133.333333,33.333333",
            "answers":"0,2,36.5,2,7"
        },
        "pushPlus_data":{
            "notifyToken" : "4d25976cc88888ae8f8688889780bfe1",
            "onlyWrongNotify" : "false"
        },
        "mark": "Bean"
    }
'
```


#####  晚签

  格式：

```
wzxy_wq_config0='
    {
        "wozaixiaoyuan_data":{
            "username": "15512345678",
            "password": "wzxywzxy",
            "location":"133.333333,33.333333"
        },
        "pushPlus_data":{
            "notifyToken" : "4d25976cc88888ae8f8688889780bfe1",
            "onlyWrongNotify" : "false"
        },
        "mark": "Bean"
    }
'
```

#### 多用户：

规则都一样 以健康打卡为例

第一个用户是wzxy_jkdk_config**0**='xxxx'  

第二个用户是wzxy_jkdk_config**1**='xxxx'  

以此累加

<img src="https://gitee.com/Bean6560/images/raw/master/typora/QQ截图20220619112833.png" alt="drawing" width="500"/>

#### 最后点击保存即可 

#### 回到青龙面板-定时任务

#### 自行进行设置任务 以及手动测试脚本即可。

### 赞赏支持
<img src="https://gitee.com/Bean6560/images/raw/master/typora/QQ%E5%9B%BE%E7%89%8720220430120324.jpg" width="500px" height="650px" alt="daka" align=center>

