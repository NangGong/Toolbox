## 一个基于[ChatGPT-on-Wechat](https://github.com/zhayujie/chatgpt-on-wechat)项目的简单插件，直接调用一些实用的api接口！

## 可以调用两个不同的SD绘画接口，以及AI艺术二维码制作等功能！

### 安装

使用管理员口令在线安装即可，参考这里去如何[认证管理员](https://www.wangpc.cc/aigc/chatgpt-on-wechat_plugin/)！

```
#installp https://github.com/NangGong/Toolbox.git
```

安装成功后，根据提示使用`#scanp`命令来扫描新插件，再使用`#enablep Toolbox`开启插件

具体使用发送#help Toolbox使用。

docker部署插件配置添加以下信息，以下信息为配置IS的SD绘画
```
 "Toolbox":{
        "is_key":"",
        "is_sd_domain":"https://domain.com",
        "dalle_key":"sk-xxxxxxxxxxxxxxxxxxxxxx"
    },
```
is的key申请地址：https://www.isddi.cn/

其他方式直接在源码中复制模板，具体看项目文档。

有两个SD接口，其中一个需要配合使用：https://github.com/NangGong/SD-ON-PHP



