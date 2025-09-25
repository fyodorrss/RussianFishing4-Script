import random
import config
from utils import sleep_time
import utils

#准备出海，到船上去
def prepare_for_sailing():
    """
    准备出海
    """

    if not config.stop_event.is_set():
        #向左转
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(-625, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    
    if not config.stop_event.is_set():
        #向前走一段路
        sleep_time(random.uniform(0.33, 0.45))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(1.2)
        utils.key_up('w')
        utils.key_up('Left Shift')

    if not config.stop_event.is_set():
        #向左转
        sleep_time(random.uniform(0.33, 0.45))
        utils.move_mouse_relative_smooth(-725, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    if not config.stop_event.is_set():
        #向前走一段路
        sleep_time(random.uniform(0.33, 0.45))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(4.92)
        utils.key_up('w')
        utils.key_up('Left Shift')

    if not config.stop_event.is_set():
        #向左转
        sleep_time(random.uniform(0.33, 0.45))
        utils.move_mouse_relative_smooth(-490, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    if not config.stop_event.is_set():
        #向下转
        sleep_time(random.uniform(0.33, 0.45))
        utils.move_mouse_relative_smooth(0, 130, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    
    if not config.stop_event.is_set():
        #向前走一段路
        sleep_time(random.uniform(0.33, 0.45))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(2.4)
        utils.key_up('w')
        utils.key_up('Left Shift')
    
    if not config.stop_event.is_set():
        #向左转一点
        sleep_time(random.uniform(0.33, 0.45))
        utils.move_mouse_relative_smooth(-110, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    
    if not config.stop_event.is_set():
        #进入船中
        sleep_time(random.uniform(1, 1.2))
        utils.press_key('e',0.05)
        sleep_time(random.uniform(1, 1.2))
        utils.press_key('e',0.05)

    if not config.stop_event.is_set():    
        #上船和选择船票
        sleep_time(random.uniform(0.6, 0.7))
        if utils.check_template_in_region(region=config.DisplayTicketOptionsRegionScreenshot, template_path="choose.png"):
            sleep_time(random.uniform(0.27, 0.37))
            utils.move_mouse_random_in_region((284,204,166,271))#续费船票的区域
            sleep_time(random.uniform(0.27, 0.37))
            utils.click_left_mouse()
            sleep_time(0.1)
            utils.click_left_mouse()