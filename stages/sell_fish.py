import random
import config
from utils import sleep_time
import utils
from ocr_global import ocr
import re
#自动卖鱼
def sell_fish():
    """
    鱼市卖鱼
    """
    if not config.stop_event.is_set():
        #转向鱼市方向
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(-625, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    if not config.stop_event.is_set():    
        #走向鱼市
        sleep_time(random.uniform(0.33, 0.45))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(1.8)
        utils.key_up('w')
        utils.key_up('Left Shift')

    if not config.stop_event.is_set():      
        #转向鱼市
        sleep_time(random.uniform(0.34, 0.35))
        utils.move_mouse_relative_smooth(550, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    
    sell_fish_func()

def sell_fish_func():

    if not config.stop_event.is_set():      
        #进入鱼市
        sleep_time(random.uniform(1.5, 1.6))
        utils.press_key('e',0.1)
        sleep_time(random.uniform(1, 1.1))
        #等进入商店
        while not config.stop_event.is_set():
            if(utils.check_template_in_region(config.ShopTitleRegionScreenshot, template_path="fishshop.png")):
                break
            sleep_time(random.uniform(0.04, 0.06))
        #等待加载鱼护
        while not config.stop_event.is_set():
            if(not utils.check_template_in_region(config.SellFishLoadingLogoRegionScreenshot, template_path="loadinglogo.png")):
               break
            sleep_time(random.uniform(0.04, 0.06))

    if not config.stop_event.is_set():      
        # 开始卖鱼
        if(not utils.check_template_in_region(config.FishBasketEmptyRegionScreenshot, template_path="fishbasketempty.png")):
            sleep_time(random.uniform(0.24, 0.35))
            utils.move_mouse_random_in_region((127, 237, 90, 34))#全选的区域
            sleep_time(random.uniform(0.25, 0.35))
            utils.click_left_mouse()
            sleep_time(random.uniform(0.56, 0.65))
            #查看鱼市的总售价
            strs = ocr.recognize_text_from_black_bg(
                config.FishMarketPriceRegionScreenshot, min_confidence=0.9
            )
            if strs:
                text = strs[0].replace(',', '')  # 去除千位分隔符
                match = re.search(r'\d+(?:\.\d*)?', text)  # 匹配非负整数或浮点数
                price = None  # 初始化 price 避免未定义错误
                if match:
                    price = float(match.group(0))
                    if price == 0 and len(strs) > 1:  # 修复 str 为 strs
                        text = strs[1].replace(',', '')  # 去除千位分隔符
                        match = re.search(r'\d+(?:\.\d*)?', text)  # 匹配非负整数或浮点数
                        if match:
                            price = float(match.group(0))
                    config.income_once.append(price)
            config.income.append(round(sum(config.income_once),2))
            #初始化硬币数组
            config.income_once.clear()
            #移动到出售按钮
            utils.move_mouse_random_in_region((126, 366, 200, 32))#出售的区域
            sleep_time(random.uniform(0.27, 0.35))
            utils.click_left_mouse()
        sleep_time(random.uniform(1.1, 1.2))
        utils.press_key('e',0.1)
        utils.press_key('e',0.1) 
      
        