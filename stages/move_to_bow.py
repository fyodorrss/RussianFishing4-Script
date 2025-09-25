import random

import config
from utils import sleep_time
import utils


#走向船头
def move_to_bow():
    """走出船舱"""
    #阻塞行为
    utils.renew_ticket_blocking()
    #防止被自动续费船票的操作打断操作
    config.is_important_action=True
    sleep_time(random.uniform(1.52, 1.62))
    utils.press_key('y',0.2)
    sleep_time(random.uniform(1.57, 1.67))
    utils.key_down('a')
    sleep_time(0.4)
    utils.key_up('a')
    sleep_time(random.uniform(0.22, 0.32))
    utils.key_down('w')
    sleep_time(1.2)
    utils.key_up('w')
    sleep_time(random.uniform(0.22, 0.32))
    utils.key_down('d')
    sleep_time(0.4)
    utils.key_up('d')
    sleep_time(random.uniform(0.22, 0.32))
    utils.key_down('w')
    sleep_time(1)
    utils.key_up('w')
    sleep_time(random.uniform(0.22, 0.32))
    utils.move_mouse_relative_smooth(0, 200, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    # utils.setinput_move_relative(0, 200, duration=random.uniform(0.2, 0.4))
    sleep_time(random.uniform(0.22, 0.32))
    config.is_important_action=False