本教程测试于centos7.6系统

1.部署qltools 

项目仓库：[青龙面板的变量第三方手动/半自动提交（上传）管理中间件 ](https://github.com/nuanxinqing123/QLTools)

部署教程

```
# 创建QLTools目录并进入
mkdir qltools && cd qltools

# Docker版本提供架构：amd64、arm64、arm-7
docker run --restart=always -itd --name QLTools -v /root/config:/QLTools/config -v /root/plugin:/QLTools/plugin -p 15000:15000 nuanxinqing123/qltools:latest

# 更新步骤：后台点击更新，稍等5分钟左右。手动重启容器即可完成更新（如果更新失败，请删除容器和镜像，然后重新拉取镜像启动）
# 重启命令：docker restart QLTools
```

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072147499.png" alt="image-20220707214654104" style="zoom:66%;" />

2.注册管理员

浏览器打开    IP或域名:15000/#/register       例如：120.30.22.55:15000/#/register

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072149383.png" alt="image-20220707214923324" style="zoom:50%;" />

3.登录后台

* 浏览器打开    IP或域名:15000/#/login       例如：120.30.22.55:15000/#/login
* 登录成功后-右上角小人-管理面板![](https://cdn.jsdelivr.net/gh/bean661/images@main/img/202206241257336.png)
* 面板管理-新增

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202206241302652.png" alt="image-20220624130235578" style="zoom: 67%;" />

* 点击”测试连接” 看是否成功

4.插件管理-上传插件-选择插件-确认 （插件在QQ群808655664群文件 wzxy_check.js）

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072154476.png" alt="image-20220707215458414" style="zoom:80%;" />

5.变量管理-新增-确认新增

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072159205.png" alt="image-20220707215931107" style="zoom: 67%;" />

```
变量匹配正则：
username=.*?;password=.*?;location=.*?;answers=.*?;pushPlusToken=.*?;onlyWrongNotify=.*?;mark=.*?;
更新匹配正则
username=.*?;
```

此时按道理来说就可以使用了，但是目前QlTOOS还存在bug（初始状态提交不上去），所以要在 青龙面板-环境变量-新建变量

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072203351.png" alt="image-20220707220343236" style="zoom:80%;" />

6.面板管理-绑定变量

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072211526.png" alt="image-20220707221154453" style="zoom: 67%;" />

7.网站设置-设置公告-填写内容-提交设置

> ## 我在校园打卡提交
>
> ### **健康打卡-提交格式**
>
> username=15512345678;password=wzxywzxy;location=133.333333,33.333333;answers=0,2,36.5,2,7;pushPlusToken=4d25976cc88888ae8f8688889780bfe1;onlyWrongNotify=true;mark=Bean;
>
> ### 日检日报-提交格式
>
> username=15512345678;password=wzxywzxy;location=133.333333,33.333333;answers=0,2,36.5,2,7;pushPlusToken=4d25976cc88888ae8f8688889780bfe1;onlyWrongNotify=true;mark=Bean;
>
> ### 晚签或抽检-提交格式(没有answers)
>
> username=15512345678;password=wzxywzxy;location=133.333333,33.333333;pushPlusToken=4d25976cc88888ae8f8688889780bfe1;onlyWrongNotify=true;mark=Bean;
>
> ### 注释：
>
> 1. username：手机号
> 2.  password：我在校园小程序密码
> 3.  location：设置的打卡位置 获取地址  [坐标拾取](https://api.map.baidu.com/lbsapi/getpoint/index.html) 
> 4.  answers：打卡页面问题的值  如果设置answers="" 使用脚本自带的answers
> 5.  pushPlusToken：关注公众号pushplus推送加 发送"token"获取
> 6.  onlyWrongNotify：true：仅打卡失败通知 false：失败和成功都会通知
> 7.  mark： 用户昵称  随便写
>
> 项目Github地址及更多教程说明： [我在校园打卡仓库](https://github.com/bean661/WoZaiXiaoYuanPuncher) 

8.提交完成之后，点击右上角跳转到login页面  或者 ip:15000/#/login

<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072209932.png" alt="image-20220707220953894" style="zoom:50%;" />



提交个人打卡信息即可



对应的健康打卡脚本名字为 jkdk2.py

日检日报和晚签的操作类似 先等脚本更新 

PS:如果出现下图问题，解决办法：在管理员端-变量管理-修改-关闭插件-确认修改   然后在开启插件-确认修改即可 （作者的小bug）



<img src="https://cdn.jsdelivr.net/gh/bean661/images@main/img/202207072219486.png" alt="image-20220707221918444" style="zoom:50%;" />
