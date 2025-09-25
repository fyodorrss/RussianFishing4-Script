import time
import random
import config
from utils import sleep_time
from ocr_global import ocr
import utils
import dxgi
from logger import logger

#自动把鱼收入护中
def put_fish_in_keepnet():
    """
    把鱼放入鱼护
    """
     
    while not config.stop_event.is_set():
        if utils.check_template_in_region(config.region_keepnet,'keepnet.png'):
            utils.mouse_up_left()
            utils.key_up('Left Shift')
            utils.mouse_up_right()
            config.is_reeling_line=False
            config.is_mouse_down_right=False
            try:
                while not config.stop_event.is_set() :
                    st=time.time()
                    fish_name = ocr.recognize_text_from_black_bg_first(config.region_fish_name,min_confidence=0.6)
                    fish_info = ocr.recognize_text_from_black_bg_first(config.region_fish_info,min_confidence=0.6)
                    logger.info(time.time()-st)
                    if fish_name and fish_info and isinstance(fish_name, str) and isinstance(fish_info, str):
                        weight = utils.parse_weight(fish_info)
                        if weight is not None :
                            logger.info(f"检测到鱼名: {fish_name}, 鱼信息: {fish_info}")
                            break
                    sleep_time(random.uniform(0.01, 0.02))

                should_keep = False

                region = config.region_fish_name
                screenshot = dxgi.grab_region(region)
                is_green  = utils.check_template_in_region(region, 'green.png',  threshold=0.9, screenshot=screenshot)
                is_yellow = utils.check_template_in_region(region, 'yellow.png', threshold=0.9, screenshot=screenshot)
                is_blue   = utils.check_template_in_region(region, 'blue.png',   threshold=0.9, screenshot=screenshot)
                
                if is_green:
                    logger.info("检测到达标鱼")
                    should_keep = True
                    #大西洋鲭达标但是不超过400克的鱼切掉
                    if fish_name == '大西洋':
                        if weight<400 and weight>=300:
                            #当前需要切的鱼是大西洋鲭
                            config.cut_fish_type = 2
                            logger.info("大西洋鲭大于300克+不超过400克，有鱼可以切")
                        elif weight<300:
                            should_keep=False    
                            logger.info("大西洋鲭不超过300克，扔了")
                    elif fish_name == '绿青鳕':
                        if weight<=3000:
                             #当前需要切的鱼是绿青鳕
                            config.cut_fish_type = 1
                            logger.info("大西洋鲭不超过400克，有鱼可以切")        
                    elif fish_name == '黑线鳕':
                        if weight<1500:
                            should_keep=False    
                            logger.info("黑线鳕不超过1.5kg，扔了")       
                    elif fish_name == "短角大杜父鱼":
                        if weight<500:
                            should_keep=False    
                            logger.info("短角大杜父鱼不超过500g，扔了") 

                elif is_yellow:
                    logger.info("检测到达标星鱼")
                    utils.press_key('F12')
                    should_keep = True
                elif is_blue:
                    logger.info("检测到蓝冠鱼")
                    utils.press_key('F12')
                    should_keep = True  
                else:
                    logger.info("检测不达标的鱼！")
                    if fish_name == '绿青鳕':
                        if config.fish_block_types1 == 1:
                            #当前需要切的鱼是绿青鳕,需要小块的绿青鳕
                            if weight>=300:
                                config.cut_fish_type = 1
                                config.current_fish_block_types1 = 1
                                should_keep = True
                        elif config.fish_block_types1 == 2:
                            #当前需要切的鱼是绿青鳕,需要绿青鱼柳
                            if weight>=300:
                                config.cut_fish_type = 1
                                config.current_fish_block_types1 = 2
                                should_keep = True
                        elif config.fish_block_types1 == 3:
                            #当前需要切的鱼是绿青鳕,需要大鱼块
                            if weight>=600:
                                config.cut_fish_type = 1
                                config.current_fish_block_types1 = 3
                                should_keep = True        
                            #看能不能切鱼柳    
                            elif weight>=300:
                                config.cut_fish_type = 1
                                config.current_fish_block_types1 = 2
                                should_keep = True
                        elif config.fish_block_types1 == 4:
                            #当前需要切的鱼是绿青鳕,需要巨大鱼块
                            if weight>=800:
                                config.cut_fish_type = 1
                                config.current_fish_block_types1 = 4
                                should_keep = True        
                            #看能不能切大鱼块
                            elif weight>=600:
                                config.cut_fish_type = 1
                                config.current_fish_block_types1 = 3
                                should_keep = True 
                            #看能不能切鱼柳                   
                            elif weight>=300:
                                config.cut_fish_type = 1
                                config.current_fish_block_types1 = 2
                                should_keep = True                               
                
                # 最终判断处理
                if should_keep:
                    logger.info(">> 入护 ✅")
                    utils.press_key('Space')
                else:
                    logger.info(">> 扔掉 ❌")
                    utils.press_key('Backspace')

            except Exception as e:
                logger.info(f"识别或判断出错: {e}")
            
        sleep_time(random.uniform(0.1, 0.2))
