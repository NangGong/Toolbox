import plugins
import requests
import re
import json
from urllib.parse import urlparse
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel import channel
from common.log import logger
from plugins import *
from datetime import datetime, timedelta
BASE_URL_VVHAN = "https://api.vvhan.com/api/"
BASE_URL_ALAPI = "https://v2.alapi.cn/api/"
BASE_URL_AA1CN = "https://v.api.aa1.cn/api/"


@plugins.register(
    name="Toolbox",
    desire_priority=88,
    hidden=False,
    desc="A plugin to handle specific keywords",
    version="0.5",
    author="vision",
)
class Apilot(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.conf = super().load_config()
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            if not self.conf:
                logger.warn("[Toolbox] inited but alapi_token not found in config")
                self.is_key = None
                self.is_sd_domain = None
            else:
                logger.info("[Toolbox] inited and alapi_token loaded successfully")
                self.is_key = self.conf["is_key"]
                self.is_sd_domain = self.conf["is_sd_domain"]
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        except Exception as e:
            raise self.handle_error(e, "[Apiot] init failed, ignore ")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT
        ]:
            return
        content = e_context["context"].content.strip()
        logger.debug("[Apilot] on_handle_context. content: %s" % content)

        if content == "每日新闻":
            news = self.get_morning_news()
            reply_type = ReplyType.IMAGE_URL if self.is_valid_url(news) else ReplyType.TEXT
            reply = self.create_reply(reply_type, news or "早报服务异常，请检查配置或者查看服务器log")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        if content == "摸鱼日历":
            moyu = self.get_moyu_calendar()
            reply_type = ReplyType.IMAGE_URL if self.is_valid_url(moyu) else ReplyType.TEXT
            reply = self.create_reply(reply_type, moyu or "早报服务异常，请检查配置或者查看服务器log")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            
        if content == "随机头像":
            avatar = self.get_avatar_calendar()
            reply_type = ReplyType.IMAGE_URL if self.is_valid_url(avatar) else ReplyType.TEXT
            reply = self.create_reply(reply_type, avatar or "头像服务异常，请检查配置或者查看服务器log")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑   
        
        if content == "职场日历":
            zcr = self.get_zcr_calendar()
            reply_type = ReplyType.IMAGE_URL if self.is_valid_url(zcr) else ReplyType.TEXT
            reply = self.create_reply(reply_type, zcr or "职场人服务异常，请检查配置或者查看服务器log")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑       
             #get_isdraw_calendar
        
        if content.startswith("抖音去水印"):
            url = prompt = content[5:].strip()
            zcr = self.get_douyin_calendar(url)
            reply_type = ReplyType.VIDEO_URL if self.is_valid_url(zcr) else ReplyType.TEXT
            reply = self.create_reply(reply_type, zcr or "请检查配置或者查看服务器log")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS # 事件结束，并跳过处理context的默认逻辑        
             
        if content.startswith("$SD"):
             model = "normal"
             prompt = content[4:].strip()            
             if prompt.startswith("竖版"):
                model = "vertical"
                prompt = prompt[2:].strip() 
             if prompt.startswith("横版"):
                model = "horizontal"
                prompt = prompt[2:].strip() 
                   
             pear_sd_= self.get_pear_sd_calendar(prompt, model)
             reply_type = ReplyType.IMAGE_URL if self.is_valid_url(pear_sd_) else ReplyType.TEXT
             reply = self.create_reply(reply_type, pear_sd_ or "服务异常，请检查配置或者查看服务器log")
             e_context["reply"] = reply
             e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        
        if content.startswith("/sd"):
             if not self.is_key:
                self.handle_error("is_key not configured", "请求失败")
                reply = self.create_reply(ReplyType.TEXT, "请先配置is_key")
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
                return  # End the function here
             else:
                aspect_ratio = "正方形"
                prompt = content[4:].strip()
             if prompt.startswith("漫画"):
                model = '漫画'
                prompt = prompt[2:].strip()
             else:
                model = "现实"
            
             if prompt.startswith("竖版"):
               aspect_ratio = "竖版"
             if prompt.startswith("横版"):
                aspect_ratio = "横版"
                
            #prompt = prompt[2:].strip()    
             isdraw = self.get_isdraw_calendar(self.is_key,self.is_sd_domain,prompt,model,aspect_ratio)
             reply_type = ReplyType.IMAGE_URL if self.is_valid_url(isdraw) else ReplyType.TEXT
             reply = self.create_reply(reply_type, isdraw or "服务异常，请检查配置或者查看服务器log")
             e_context["reply"] = reply
             e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑  
        
        if content.startswith("二维码 "):
             string = content[4:].strip()
             prompt, url = string.split(':', 1)            
             aiqrcode= self.get_aiqrcode(prompt, url)
             reply_type = ReplyType.IMAGE_URL if self.is_valid_url(aiqrcode) else ReplyType.TEXT
             reply = self.create_reply(reply_type, aiqrcode or "服务异常，请检查配置或者查看服务器log")
             e_context["reply"] = reply
             e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑                
 



    def get_help_text(self, verbose=False, **kwargs):
        short_help_text = " 发送特定指令以获取各种信息等功能！"

        if not verbose:
            return short_help_text

        help_text = "📚 发送关键词获取特定信息！\n"

        # 娱乐和信息类
        help_text += "\n🎉 娱乐与资讯：\n"
        help_text += "  🌅 每日新闻: 发送“每日新闻”获取早报。\n"
        help_text += "  🐟 摸鱼日历: 发送“摸鱼日历”获取摸鱼人日历。\n"
        help_text += "  🧑‍💻 职场日历: 发送“职场日历”获取职场人日历。\n"
        help_text += "  🧑 随机头像: 发送“随机头像”获取随机头像。\n"
        help_text += "  🚀 抖音下载: 发送“抖音去水印https://www.abc.com”下载无水印视频。\n"
        help_text += "  🚀 AI二维码: 发送“二维码 cat:你好”来制作二维码。\n"

        help_text += "\n🎨 SD绘画：\n"
        help_text += "\n🎨 示例：$SD girl\n"
        help_text += "\n🎨 示例：$SD 竖版 girl\n"
        help_text += "\n🎨 示例：$SD 横版 girl\n"
        
        help_text += "\n🎨 SD绘画：\n"
        help_text += "\n🎨 示例：/sd girl\n"
        help_text += "\n🎨 示例：/sd 竖版 girl\n"
        help_text += "\n🎨 示例：/sd 横版 girl\n"
        help_text += "\n🎨 示例：/sd 漫画girl\n"
        help_text += "\n🎨 示例：/sd 漫画横版girl\n"
        help_text += "\n🎨 示例：/sd 漫画竖版girl\n"
        
        


        return help_text

    def get_morning_news(self):
            url = BASE_URL_VVHAN + "60s?type=json"
            payload = "format=json"
            headers = {'Content-Type': "application/x-www-form-urlencoded"}
            try:
                morning_news_info = self.make_request(url, method="POST", headers=headers, data=payload)
                if isinstance(morning_news_info, dict) and morning_news_info['success']:                   
                        return morning_news_info['imgUrl']
                else:
                    return self.handle_error(morning_news_info, "get_morning_news失败")
            except Exception as e:
                return self.handle_error(e, "早报获取失败")


    def get_moyu_calendar(self):
        url = BASE_URL_VVHAN + "moyu?type=json"
        payload = "format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        try:
            moyu_calendar_info = self.make_request(url, method="POST", headers=headers, data=payload)
            # 验证请求是否成功
            if isinstance(moyu_calendar_info, dict) and moyu_calendar_info['success']:
                return moyu_calendar_info['url']
            else:
                return self.handle_error(moyu_calendar_info, "moyu_calendar请求失败")
        except Exception as e:
            return self.handle_error(e, "获取摸鱼日历信息失败")
            
    def get_avatar_calendar(self):
        url = BASE_URL_VVHAN + "avatar?type=json"
        payload = "format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        try:
            avatar_calendar_info = self.make_request(url, method="POST", headers=headers, data=payload)
            # 验证请求是否成功
            if isinstance(avatar_calendar_info, dict) and avatar_calendar_info['success']:
                return avatar_calendar_info['avatar']
            else:
                return self.handle_error(avatar_calendar_info, "avatar_calendar请求失败")
        except Exception as e:
            return self.handle_error(e, "获取头像信息失败")
            
    def get_zcr_calendar(self):
        url = BASE_URL_VVHAN + "zhichang?type=json"
        payload = "format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        try:
            zcr_calendar_info = self.make_request(url, method="POST", headers=headers, data=payload)
            # 验证请求是否成功
            if isinstance(zcr_calendar_info, dict) and zcr_calendar_info['success']:
                return zcr_calendar_info['url']
            else:
                return self.handle_error(zcr_calendar_info, "avatar_calendar请求失败")
        except Exception as e:
            return self.handle_error(e, "获取信息失败")
            
    def get_pear_sd_calendar(self, prompt, model):
        url = "https://api.pearktrue.cn/api/stablediffusion/?prompt="+prompt+"&model="+model


        try:
            pear_sd_msg = self.make_request(url, method="GET")
            # 验证请求是否成功
            if isinstance(pear_sd_msg, dict) and pear_sd_msg['code']==200:
                return pear_sd_msg['imgurl']
            else:
                return self.handle_error(pear_sd_msg, pear_sd_msg['msg'])
        except Exception as e:
            return self.handle_error(e, "获取信息失败")          
        
    def get_isdraw_calendar(self,is_key,domain,prompt,model,aspect_ratio):
        url = domain+"/api/sd/?key="+is_key+"&model="+model+"&aspect_ratio="+aspect_ratio
       # payload = "format=json"
        data = {"prompt": prompt}
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        try:
            isdraw_calendar_info = self.make_request(url, method="POST", headers=headers, data=data)
            # 验证请求是否成功
            if isinstance(isdraw_calendar_info, dict) and isdraw_calendar_info['success']:
                return isdraw_calendar_info['url']
            else:
                return self.handle_error(isdraw_calendar_info, isdraw_calendar_info['message'])
        except Exception as e:
            return self.handle_error(e, "获取信息失败")   
        
         
    
    def get_aiqrcode(self, prompt, url):
        url = "https://api.pearktrue.cn/api/aiqrcode/?prompt="+prompt+"&url="+url

        try:
            aiqrcode = self.make_request(url, method="GET")
            # 验证请求是否成功
            if isinstance(aiqrcode, dict) and aiqrcode['code']==200:
                return aiqrcode['imgurl']
            else:
                return self.handle_error(aiqrcode, aiqrcode['msg'])
        except Exception as e:
            return self.handle_error(e, "获取失败!") 
        
                

    def make_request(self, url, method="GET", headers=None, params=None, data=None, json_data=None):
        try:
            if method.upper() == "GET":
                response = requests.request(method, url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.request(method, url, headers=headers, data=data, json=json_data)
            else:
                return {"success": False, "message": "Unsupported HTTP method"}

            return response.json()
        except Exception as e:
            return self.handle_error(e, "请求失败")
        
    def get_douyin_calendar(self,url):
        url = "https://zj.v.api.aa1.cn/api/douyinjx/?url="+url
        payload = "format=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        try:
            douyin_calendar_info = self.make_request(url, method="POST", headers=headers, data=payload)
            # 验证请求是否成功
            if isinstance(douyin_calendar_info, dict):
                return douyin_calendar_info['url']
            else:
                return self.handle_error(douyin_calendar_info, "avatar_calendar请求失败")
        except Exception as e:
            return self.handle_error(e, "获取信息失败")    


    def create_reply(self, reply_type, content):
        reply = Reply()
        reply.type = reply_type
        reply.content = content
        return reply

    def handle_error(self, error, message):
        logger.error(f"{message}，错误信息：{error}")
        return message

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def load_city_conditions(self):
        if self.condition_2_and_3_cities is None:
            try:
                json_file_path = os.path.join(os.path.dirname(__file__), 'duplicate-citys.json')
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    self.condition_2_and_3_cities = json.load(f)
            except Exception as e:
                return self.handle_error(e, "加载condition_2_and_3_cities.json失败")


    def check_multiple_city_ids(self, city):
        self.load_city_conditions()
        city_info = self.condition_2_and_3_cities.get(city, None)
        if city_info:
            return city_info
        return None
