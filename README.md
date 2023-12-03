## 一个基于[ChatGPT-on-Wechat](https://github.com/zhayujie/chatgpt-on-wechat)项目的简单插件，直接调用一些实用的api接口！

## 可以调用两个不同的SD绘画接口，还有DALL-E3绘画，以及AI艺术二维码制作等功能！
### 说明
- 这个插件是基于ChatGPT-on-Wechat项目的插件
- 该插件集成了许多的api接口，比如sd绘画，dalle绘画，以及一些摸鱼早报等功能，具体安装后发送#hello toolbox查看功能
- 对于DALLE绘画，ChatGPT-on-Wechat项目本身也支持，只是不支持尺寸，而这个插件支持其他的尺寸
- 该插件的sd和dalle接口要依赖于php，故需要直接在宝塔上面搭建一个php网站，源码在https://github.com/NangGong/SD-ON-PHP
- 有两个SD接口，其中一个需要配合使用：https://github.com/NangGong/SD-ON-PHP

### 安装

- 使用管理员口令在线安装即可，参考这里去如何[认证管理员](https://www.wangpc.cc/aigc/chatgpt-on-wechat_plugin/)！

```
#installp https://github.com/NangGong/Toolbox.git
```
- 也可以直接解压到插件目录就行

- 安装成功后，根据提示使用`#scanp`命令来扫描新插件，再使用`#enablep Toolbox`开启插件

插件配置添加以下信息：
- is_key是你申请的sd的key
- is_sd_domain是你搭建的php网站域名
- https://domain.com格式是这样，不要有任何后缀
- 配置完成后发送#help Toolbox使用
```
 "Toolbox":{
        "is_key":"",
        "is_sd_domain":"https://domain.com",
        "dalle_key":"sk-xxxxxxxxxxxxxxxxxxxxxx"
    },
```
is的key申请地址：https://www.isddi.cn/

其他方式直接在源码中复制模板，具体看项目文档。





