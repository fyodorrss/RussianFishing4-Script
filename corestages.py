from stages.buy_boat_ticket import buy_boat_ticket
from utils import sleep_time, start_daemon_thread
import navigator
from stages.auto_fish_single import auto_fish_single
from stages.auto_renew_ticket import auto_renew_ticket
from stages.check_fishnet_status import get_fish_count
from stages.coffee_shop_task import coffee_shop_task
from stages.in_sea_map import in_sea_map
import config
from stages.is_stuck import is_stuck
from stages.prepare_for_sailing import prepare_for_sailing
from stages.relogin import relogin
from stages.sail_to_destination import sail_to_destination
from stages.sell_fish import sell_fish

from logger import logger

def run_loop():
    """
    主流程
    """
    # 确保进入海图    
    if config.stop_event.is_set():
        return
    in_sea_map()

    if config.stop_event.is_set():
        return
    if config.need_back:
        logger.debug("需要回城")

        # 重新登录，初始化状态
        if config.stop_event.is_set():
            return
        relogin()
        
        # 判断是否要去卖鱼
        sleep_time(0.5)
        fish_quantity = get_fish_count()
        is_have_sell=False
        if fish_quantity:
            fish_count, fish_capacity = fish_quantity
            logger.info(f"鱼护当前数量: {fish_count}, 容量: {fish_capacity}")
            if fish_count > 0:
                is_have_sell=True
               
        # 卖鱼
        if config.stop_event.is_set():
            return
        if is_have_sell:
            # 咖啡厅交任务
            if config.stop_event.is_set():
                return
            coffee_shop_task()

            if config.stop_event.is_set():
                return
            # 鱼市卖鱼
            sell_fish()


        # 检查船票，自动补充
        if config.stop_event.is_set():
            return
        if not config.is_fly_ticket:
            buy_boat_ticket(is_have_sell)

        #小退一次
        if config.stop_event.is_set():
            return
        if not config.is_fly_ticket or is_have_sell:
            relogin()    

        # 开始卡住的检测机制
        if config.stop_event.is_set():
            return
        start_daemon_thread(is_stuck)    

        # 准备出海
        if config.stop_event.is_set():
            return
        prepare_for_sailing()

        # 开始自动续票的检测线程
        if config.stop_event.is_set():
            return
        start_daemon_thread(auto_renew_ticket)

        # 已经上船，开始出发
        if config.stop_event.is_set():
            return
        sail_to_destination()

    else:
        logger.debug("不需要回城")
        
        # 开始卡住的检测机制
        if config.stop_event.is_set():
            return
        start_daemon_thread(is_stuck)

        # 开始自动续票的检测线程
        if config.stop_event.is_set():
            return
        start_daemon_thread(auto_renew_ticket) 

        if config.stop_event.is_set():
            return
        # 直接去目的地
        navigator.go_destination()

    if config.stop_event.is_set():
        return
    # 开始自动钓鱼
    # auto_fish()
    auto_fish_single()
