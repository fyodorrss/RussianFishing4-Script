import re
import time
import random
import config
import navigator
from utils import sleep_time
from ocr_global import ocr
import utils
from logger import logger  # 确保文件开头有这行

#自动购买船票
def buy_boat_ticket(is_have_sell):
    """
    购买船票
    """ 
    
    if is_have_sell:
        """
        卖完鱼之后的路径
        """
        # 向后转，前往购买船票
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(910, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

        # 向前走
        sleep_time(random.uniform(0.23, 0.33))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(3)
        utils.key_up('w')
        utils.key_up('Left Shift')
        
        # 向左转
        sleep_time(random.uniform(0.23, 0.33))
        utils.move_mouse_relative_smooth(-650, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
        
        # 向前走
        sleep_time(random.uniform(0.23, 0.33))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(4.8)
        utils.key_up('w')
        utils.key_up('Left Shift')
    
        # 向右转e
        sleep_time(random.uniform(0.23, 0.33))
        utils.move_mouse_relative_smooth(620, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
        
    else:
        """
        没鱼可以卖的路径
        """
        if not config.stop_event.is_set():
            #向左转
            sleep_time(random.uniform(0.52, 0.65))
            utils.move_mouse_relative_smooth(-625, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
        
        if not config.stop_event.is_set():
            #向前走一段路
            sleep_time(random.uniform(0.23, 0.33))
            utils.key_down('Left Shift')
            utils.key_down('w')
            sleep_time(1.2)
            utils.key_up('w')
            utils.key_up('Left Shift')

        if not config.stop_event.is_set():
            #向左转
            sleep_time(random.uniform(0.2, 0.3))
            utils.move_mouse_relative_smooth(-725, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

        if not config.stop_event.is_set():
            #向前走一段路
            sleep_time(random.uniform(0.23, 0.33))
            utils.key_down('Left Shift')
            utils.key_down('w')
            sleep_time(4.92)
            utils.key_up('w')
            utils.key_up('Left Shift')

        if not config.stop_event.is_set():
            #向右转e
            sleep_time(random.uniform(0.22, 0.32))
            utils.move_mouse_relative_smooth(620, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))    


    if not config.stop_event.is_set():
        #点击进入船票界面
        sleep_time(random.uniform(1.5, 1.6))
        utils.press_key('e',0.1)
        sleep_time(random.uniform(1, 1.1))
        #等进入商店
        while not config.stop_event.is_set():
            if(utils.check_template_in_region(config.ShopTitleRegionScreenshot, template_path="shipside.png")):
                break
            sleep_time(random.uniform(0.04, 0.06))

    if not config.stop_event.is_set():
        #等待加载船票
        while not config.stop_event.is_set():
            if(not utils.check_template_in_region(config.LoadingLogoRegionScreenshot, template_path="loadinglogo.png")):
               break
            sleep_time(random.uniform(0.04, 0.06))
        #查看有几张票
        sleep_time(random.uniform(0.25, 0.35))
        utils.move_mouse_random_in_region((1168, 250, 1, 1))#船票背包logo
        sleep_time(random.uniform(0.25, 0.35))
    
    # 26. 购买船票
    if not config.stop_event.is_set():
        # st=time.time()
        # while not config.stop_event.is_set():
        #     num=ocr.recognize_text_from_black_bg_first(region=config.TicketCountDisplayRegionScreenshot,scale=3)#识别船票数量
        #     match = re.search(r'(\d+)个', num)
        #     if match:
        #         num = int(match.group(1))
        #         logger.info(f"船票数量剩余：{num}")
        #         break
        #     elif time.time() - st > 3:
        #         logger.warning("未识别到船票数量")
        #         num = 1
        #         break
        #     sleep_time(random.uniform(0.04, 0.06))

        # if num==0 or num==1 or num==2:
        #     sleep_time(random.uniform(0.27, 0.37))
        #     utils.move_mouse_random_in_region((1165, 395, 195, 147))#选择船票区域
        #     sleep_time(random.uniform(0.27, 0.37))
        #     utils.click_left_mouse()
        #     sleep_time(random.uniform(0.27, 0.37)) 
        #     utils.move_mouse_random_in_region((1631,265,101,33))#点击购买区域
        #     if num==0:
        #         sleep_time(random.uniform(0.57, 0.67))
        #         utils.click_left_mouse()
        #         sleep_time(random.uniform(0.57, 0.67))
        #         utils.click_left_mouse()
        #         sleep_time(random.uniform(0.57, 0.67))
        #         utils.click_left_mouse() 
        #     if num==1:
        #         sleep_time(random.uniform(0.57, 0.67))
        #         utils.click_left_mouse()
        #         sleep_time(random.uniform(0.57, 0.67))
        #         utils.click_left_mouse()  
        #     if num==2:
        #         sleep_time(random.uniform(0.57, 0.67))
        #         utils.click_left_mouse()
        target_count=config.ticket_target_count
        if  isinstance(target_count, int) and target_count > 0:
            st = time.time()
            while not config.stop_event.is_set():
                num_text = ocr.recognize_text_from_black_bg_first(
                    region=config.TicketCountDisplayRegionScreenshot,
                    scale=3
                )
                match = re.search(r'(\d+)个', num_text)
                if match:
                    current_count = int(match.group(1))
                    logger.info(f"船票数量剩余：{current_count}")
                    break
                elif time.time() - st > 3:
                    logger.warning("未识别到船票数量，默认当前为 1 张")
                    current_count = 1
                    break
                sleep_time(random.uniform(0.04, 0.06))

            to_buy = target_count - current_count
            if to_buy <= 0:
                logger.info("船票数量已满足，无需购买")
            else:
                to_buy = min(to_buy, 10)
                logger.info(f"准备购买 {to_buy} 张船票")

                sleep_time(random.uniform(0.27, 0.37))
                utils.move_mouse_random_in_region((1165, 395, 195, 147))  # 选择船票区域
                sleep_time(random.uniform(0.27, 0.37))
                utils.click_left_mouse()
                sleep_time(random.uniform(0.27, 0.37))
                utils.move_mouse_random_in_region((1631, 265, 101, 33))  # 点击购买区域

                for _ in range(to_buy):
                    sleep_time(random.uniform(0.57, 0.67))
                    utils.click_left_mouse()
          
                sleep_time(random.uniform(0.5, 0.6))
                utils.press_key('e',0.4)  
        # #退出界面          
        sleep_time(random.uniform(1.1, 1.2))
        utils.press_key('e',0.1)
        utils.press_key('e',0.1) 
