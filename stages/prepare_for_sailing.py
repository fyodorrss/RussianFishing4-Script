import random
import config
from utils import sleep_time
import utils

#准备出海，到船上去
def prepare_for_sailing():
    """
    准备出海
    """

    # 拿出鱼竿
    if config.is_fly_ticket:
        sleep_time(random.uniform(0.42, 0.52))
        utils.key_down('U')
        sleep_time(random.uniform(0.42, 0.52))
        cout = 0
        max_attempts = 10  # 最大尝试次数
        flyrod_regions=[]
        while not config.stop_event.is_set() and cout < max_attempts:
            cout += 1
            flyrod_regions=utils.find_template_in_regions(config.FlyRodRegionScreenshot, 'flyrod.png', confidence=0.95)
            if len(flyrod_regions) > 0:
                drr=flyrod_regions[0]
                utils.move_mouse_random_in_region((drr["left"], drr["top"], drr["width"], drr["height"]))
                break
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse(0.1)
        sleep_time(random.uniform(0.42, 0.52))
        utils.key_up('U')
        
        #配置鱼杆
        sleep_time(random.uniform(2, 2.1))
        utils.press_key('v')
        #修改钓组
        sleep_time(random.uniform(1.42, 1.52))
        utils.move_mouse_random_in_region((1105,258,80,17))
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.42, 0.52))
        utils.move_mouse_random_in_region((1039,421,159,47))
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse()
        sleep_time(0.1)
        utils.click_left_mouse()
        #选择钩子
        sleep_time(random.uniform(1.42, 1.52))
        utils.move_mouse_random_in_region((1001,603,64,64))
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.42, 0.52))
        utils.move_mouse_random_in_region((285, 203, 166, 200))
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse()
        sleep_time(0.1)
        utils.click_left_mouse()
        #选择饵
        sleep_time(random.uniform(1.42, 1.52))
        utils.move_mouse_random_in_region((1001,695,64,64))
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.42, 0.52))
        utils.move_mouse_random_in_region((285, 203, 166, 200))
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse()
        sleep_time(0.1)
        utils.click_left_mouse()
        #关闭界面
        sleep_time(random.uniform(0.42, 0.52))
        utils.press_key('v', 0.1)  # 关闭界面
    
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