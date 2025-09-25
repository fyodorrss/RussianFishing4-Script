import time
import random
from collections import deque

import config
from utils import sleep_time
from ocr_global import ocr
import utils
from logger import logger

#自动收线的线程
def reel_line():
    """
    鱼上钩收线
    """
    hook_not_detected_count = 0
    max_not_detected_threshold = 2  # 可调参数，建议 2～5 之间
    last_values=deque(maxlen=50)
    while not config.stop_event.is_set():
            
        cast_line_meters = utils.get_cast_line_meters(ocr.recognize_text_from_black_bg(config.region_cast_line_meters,min_confidence=0.9,is_preprocess=False))

        if utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png'):
            hook_not_detected_count = 0  # 检测到，计数清零
            if not config.is_reeling_line:
                config.is_reeling_line=True
                logger.info("开始收线")
                if config.is_electric_reel:
                    # utils.click_left_mouse()
                    # sleep_time(random.uniform(0.52, 0.62))
                    utils.click_left_mouse()
                    sleep_time(0.1)
                    utils.click_left_mouse()
                else:    
                    # sleep_time(random.uniform(0.52, 0.62))
                    utils.mouse_down_left()
                    utils.key_down('Left Shift')
            else:
                #拉起渔竿
                if cast_line_meters is not None :
                    #判断是否抬竿
                    m=0 if config.is_electric_reel else 5 
                    if cast_line_meters<=m and not config.is_mouse_down_right:
                        utils.mouse_down_right()
                        config.is_mouse_down_right=True
                    #收鱼的中断检测机制
                    last_values.append(cast_line_meters)
                    if len(last_values) == 50:
                        if all(x == last_values[0] for x in last_values):
                            logger.info(last_values)
                            logger.info("收鱼中断")
                            if last_values[0]==0:
                                #说明竿子没有抬起来，原因未知
                                utils.mouse_down_right()
                                #有可能大鱼拉不动
                                if not config.is_space:
                                    utils.press_key('Space')
                                    # utils.move_mouse_relative_smooth(0, 800, =0.5, steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
                                    config.is_space=True

                            else:
                                #说明收线中断，原因位置
                                if config.is_electric_reel:
                                    utils.click_left_mouse()
                                    sleep_time(0.1)
                                    utils.click_left_mouse()
                                else:    
                                    utils.mouse_down_left()
                                    utils.key_down('Left Shift')
                    
        else:
            hook_not_detected_count += 1
            if config.is_reeling_line and hook_not_detected_count >= max_not_detected_threshold:
                #说明鱼脱钩了,打开渔轮
                utils.mouse_up_left()
                utils.key_up('Left Shift')
                utils.mouse_up_right()
                config.is_mouse_down_right=False
                config.is_reeling_line=False
                sleep_time(random.uniform(0.52, 0.62))
                utils.press_key('Enter')
                hook_not_detected_count = 0  # 重置防抖
        
        sleep_time(random.uniform(0.5, 0.6))