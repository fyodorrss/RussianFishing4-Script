import random
import config
from utils import sleep_time
from stages.move_to_bow import move_to_bow
import utils
import navigator
from logger import logger

#自动回坑
def return_destination():
    """
    回坑
    """
    current_pos =  navigator.get_current_position()
    logger.info(f"检测回坑识别到当前位置: {current_pos}")
    if current_pos:    
        distance =  navigator.calculate_distance(current_pos,  config.destination)
        if distance > config.dist and not config.is_trolling_mode:
            #一般来说人不在方向盘上，所以先进入船中
            sleep_time(random.uniform(0.22, 0.32))
            utils.press_key('y',0.1)
            sleep_time(random.uniform(1.22, 1.32))
            logger.info("已经回到船上，准备回坑")
            utils.move_mouse_relative_smooth(0, -200, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
            # utils.setinput_move_relative(0, -200, duration=random.uniform(0.2, 0.4))
            sleep_time(random.uniform(0.22, 0.32))
            navigator.go_destination()
            move_to_bow()
            logger.info("已经回到船头！")
            return True
        else:
            #不需要回坑，直接钓鱼
            return False
    else:
        #获取坐标失败，直接钓鱼
        return False