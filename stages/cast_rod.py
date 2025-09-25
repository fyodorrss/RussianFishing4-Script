import random
import config
from utils import sleep_time
from stages.check_fishnet_status import check_fishnet_status
from stages.cut_fish import cut_fish
from stages.return_destination import return_destination
import utils
from logger import logger
#自动抛杆线程        
def cast_rod():
    """
    抛竿
    """
    while not config.stop_event.is_set():
        if(utils.check_template_in_region(config.region_cast_rod,'cast_rod.png')):
            #重置异常状态
            if config.is_space:
                utils.press_key('Space')
                # utils.move_mouse_relative_smooth(0, -800, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
                config.is_space=False

            #检查要不要切鱼
            if not config.stop_event.is_set():
                #阻塞行为，续票完成后再执行下面的操作
                utils.renew_ticket_blocking()
                cut_fish()
            #检查是不是满护了
            if not config.stop_event.is_set():
                #阻塞行为，续票完成后再执行下面的操作
                utils.renew_ticket_blocking()
                sleep_time(0.1)
                if not check_fishnet_status():
                    return
            if not config.stop_event.is_set() and not config.is_need_renew_ticket:
                #抛竿前判断要不要回坑
                if not return_destination():
                    #阻塞行为，续票完成后再执行下面的操作
                    utils.renew_ticket_blocking()
                    sleep_time(random.uniform(0.52, 0.62))
                    utils.click_left_mouse(0.05)
                    logger.info("已经抛竿")
        
        sleep_time(random.uniform(0.5, 0.6))      