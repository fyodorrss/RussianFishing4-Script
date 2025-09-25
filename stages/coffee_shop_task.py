import random
import re
import config
from utils import sleep_time
from ocr_global import ocr
import utils
from logger import logger
import time



#自动交咖啡厅的任务
def coffee_shop_task():
    """
    交咖啡厅任务
    """
    #转向咖啡厅
    if not config.stop_event.is_set():
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(-1525, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    
    coffee_shop_task_func()
    

def coffee_shop_task_func():     
    if not config.stop_event.is_set():

        #点击 'e' 键进入咖啡厅菜单
        sleep_time(random.uniform(1.5, 1.6))
        utils.press_key('e',0.1)
        sleep_time(random.uniform(0.5, 0.6))

        #等进入商店
        while not config.stop_event.is_set():
            if(utils.check_template_in_region(config.ShopTitleRegionScreenshot, template_path="coffee.png")):
                break
            sleep_time(random.uniform(0.04, 0.06))

        #等待加载
        while not config.stop_event.is_set():
            if(not utils.check_template_in_region(config.LoadingLogoRegionScreenshot, template_path="loadinglogo.png")):
               break
            sleep_time(random.uniform(0.04, 0.06))

        #分组执行多个区域操作
        region_groups = [
            (436, 175, 245, 220),
            (722, 175, 245, 220),
            (1008, 175, 245, 220),
            (1294, 175, 245, 220),
            (1580, 175, 245, 220),
            (436, 597, 245, 220),
            (722, 597, 245, 220),
            (1008, 597, 245, 220),
            (1294, 597, 245, 220),
            (1580, 597, 245, 220),
        ]
        for region in region_groups:
            sleep_time(random.uniform(0.5, 0.6))
            utils.move_mouse_random_in_region(region)
            sleep_time(random.uniform(0.23, 0.33))
            utils.click_left_mouse()
            
            #是不是已经交过任务了
            sleep_time(random.uniform(0.3, 0.4))
            if not utils.check_template_in_region(config.region_coffee_shop_task_sign,'sign.png'):
               continue
            
            #等待加载鱼护
            while not config.stop_event.is_set():
                if(not utils.check_template_in_region(config.SellFishLoadingLogoRegionScreenshot, template_path="loadinglogo.png")):
                    break
                sleep_time(random.uniform(0.04, 0.06))
            
            #不为空
            if not utils.check_template_in_region(config.CoffeeFishBasketEmptyRegionScreenshot,'coffeefishbasketempty.png'):
                #按重量排序
                sleep_time(random.uniform(0.24, 0.34))
                utils.move_mouse_random_in_region((150,799,140,14))
                sleep_time(random.uniform(0.23, 0.33))
                utils.click_left_mouse()
                
                #点击全选按钮
                sleep_time(random.uniform(0.25, 0.35))
                utils.key_down('Left Ctrl')
                sleep_time(random.uniform(0.25, 0.35))
                utils.press_key('A')
                utils.key_up('Left Ctrl')
                sleep_time(random.uniform(0.26, 0.36))

                #交任务
                sleep_time(random.uniform(0.27, 0.37))
                str = ocr.recognize_text_from_black_bg_first(config.region_coffee_shop_task_fish_count)
                if str:
                    match = re.fullmatch(r'(\d+)个[\/1](\d+)个', str)
                    if match :
                        have=int(match.group(1)) 
                        need=int(match.group(2))
                        if have>=need:
                            #可以交任务
                            #先取消全选
                            # sleep_time(random.uniform(0.25, 0.35))
                            utils.key_down('Left Ctrl')
                            sleep_time(random.uniform(0.25, 0.35))
                            utils.press_key('D')
                            utils.key_up('Left Ctrl')
                            sleep_time(random.uniform(0.26, 0.36))
                            #选择任务鱼
                            regions = utils.get_fish_regions(need)
                            utils.ctrl_click_in_regions(regions)
                            #查看任务价格
                            strs = ocr.recognize_text_from_black_bg(
                                config.CafePriceRegionScreenshot, min_confidence=0.9
                            )
                            if strs:
                                config.income_once.append(float(strs[0].replace(',', '')))
                            #点击出售按钮
                            sleep_time(random.uniform(0.28, 0.38))
                            utils.move_mouse_random_in_region((127,628,240,32))
                            sleep_time(random.uniform(0.29, 0.39))
                            utils.click_left_mouse()
                            sleep_time(random.uniform(0.8, 0.9))
                            continue
            
            #退出子菜单 
            sleep_time(random.uniform(0.5, 0.6))
            utils.press_key('esc',0.1)
        
        # 退出界面
        sleep_time(random.uniform(1.1, 1.2))
        utils.press_key('e',0.1)
        utils.press_key('e',0.1) 

        #等待退出商店
        check_start_time = None
        while not config.stop_event.is_set():
            in_shop = utils.check_template_in_region(config.ShopTitleRegionScreenshot, template_path="coffee.png")
            
            if not in_shop:
                logger.info("界面已退出")
                break

            # 第一次检测到还在界面，记录起始时间
            if check_start_time is None:
                check_start_time = time.time()
            
            # 如果持续超过指定时间仍在界面，开始手动退出
            if time.time() - check_start_time >= 5.0:
                logger.info("退出咖啡厅出错")
                utils.press_key('e',0.1)

            sleep_time(random.uniform(0.04, 0.06))
        
