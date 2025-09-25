import random
import config
from utils import sleep_time
import utils
import navigator


#自动前往目的地
def sail_to_destination():
    """
    前往目的地
    """
    if not config.stop_event.is_set() :
        #驶出码头操作
        sleep_time(random.uniform(3, 3.1))
        #阻塞行为
        utils.renew_ticket_blocking()
        #防止被自动续费船票的操作打断操作
        config.is_important_action=True
        utils.key_down('w')
        utils.key_down('d')
        sleep_time(2.2)
        utils.key_up('d')
        sleep_time(5.7)
        utils.key_down('a')
        sleep_time(1.7)
        utils.key_up('a')
        utils.key_up('w') 
        config.is_important_action=False
    
    #更新下自己的位置
    if not config.stop_event.is_set():
        navigator.get_current_position()
        
    if not config.stop_event.is_set():
        #等待驶出码头
        # sleep_time(random.uniform(140, 142))
        sleep_time(random.uniform(60, 62))
        utils.press_key('g',0.05)
        utils.press_key('g',0.05)
        #前往中转站
        navigator.start_navigation((199,399))
        #更新下坑位
        if config.auto_change_pit and not config.stop_event.is_set():
            utils.switch_to_next_auto_pit()
        #前往目的地
        navigator.go_destination()    