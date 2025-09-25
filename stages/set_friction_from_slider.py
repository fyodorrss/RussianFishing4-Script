import time
import random
import config
from utils import sleep_time
import utils

#自动点锁线程
def set_friction_from_slider():
    """
    点锁功能
    """
    last_action = 'down'
    while not config.stop_event.is_set():
        if config.is_reeling_line and config.is_open_lock_unlock:
            ratio = utils.analyze_tension_color_percentage(config.region_fishing_tension_bar)
            if ratio is None:
                continue
            green = ratio['green']
            yellow = ratio['yellow']
            red = ratio['red']

            tension_value = max(green, yellow, red)
            config.tension_value=tension_value

            #点锁    
            if config.min_lock_unlock_value < tension_value < config.max_lock_unlock_value and last_action != 'up':
                utils.slow_scroll(up=True, steps=1)
                last_action = 'up'
            elif (tension_value < config.min_lock_unlock_value or tension_value >= config.max_lock_unlock_value) and last_action != 'down':
                utils.slow_scroll(up=False, steps=1)
                last_action = 'down'
                
        #一定不能注释，会导致整体速度变慢
        sleep_time(random.uniform(0.001, 0.002)) 


#自动点锁线程-单独版本
def set_friction_from_slider_alone():
    """
    点锁功能
    """
    last_action = 'down'
    while not config.stop_event.is_set():
        # 检测鱼咬钩
        fish_bite = utils.check_template_in_region(
        config.region_fish_bite, 'fish_bite.png'
        )
        if fish_bite:
            ratio = utils.analyze_tension_color_percentage(config.region_fishing_tension_bar)
            if ratio is None:
                continue
            green = ratio['green']
            yellow = ratio['yellow']
            red = ratio['red']

            tension_value = max(green, yellow, red)
            config.tension_value=tension_value

            #点锁
            if config.min_lock_unlock_value < tension_value < config.max_lock_unlock_value and last_action != 'up':
                utils.slow_scroll(up=True, steps=1)
                last_action = 'up'
            elif (tension_value < config.min_lock_unlock_value or tension_value >= config.max_lock_unlock_value) and last_action != 'down':
                utils.slow_scroll(up=False, steps=1)
                last_action = 'down'
        #一定不能注释，会导致整体速度变慢
        sleep_time(random.uniform(0.001, 0.002))         