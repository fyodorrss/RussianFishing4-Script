import random
import time
import config
from utils import sleep_time,press_key
from ocr_global import ocr
from logger import logger  # 确保导入

#检查鱼护数量
def get_fish_count():
    """检测鱼护数量"""
    fish_quantity = None
    st = time.time()
    while not config.stop_event.is_set() and time.time() - st < 60:
        fish_quantity = ocr.recognize_text_from_black_bg_first(region=config.region_fish_quantity)
        if fish_quantity and '/' in fish_quantity:
            parts = fish_quantity.split('/')
            if len(parts) == 2:
                fish_count_str, fish_capacity_str = parts
                if fish_count_str.isdigit() and fish_capacity_str.isdigit():
                    return (int(fish_count_str), int(fish_capacity_str))
        sleep_time(random.uniform(0.5, 0.6))
    return None

def check_fishnet_status():
    """检测鱼护数量 - 小退"""
    fish_quantity = get_fish_count()
    logger.info(f"开始检查鱼护库存:{fish_quantity}")
    if fish_quantity:
        fish_count, fish_capacity = fish_quantity
        # 鱼护满了或接近满
        if fish_count >= fish_capacity-1:
            logger.info(f"鱼护已满，当前数量: {fish_count}, 容量: {fish_capacity}")
            config.need_restart = True
            return False
    return True


def get_fish_count_other():
    """检测鱼护数量"""
    fish_quantity = None
    st = time.time()
    sleep_time(random.uniform(0.5, 0.6))
    press_key('c')
    sleep_time(random.uniform(0.5, 0.6))
    while not config.stop_event.is_set() and time.time() - st < 60:
        fish_quantity = ocr.recognize_text_from_black_bg_first(region=config.region_fish_quantity_other)
        if fish_quantity and '/' in fish_quantity:
            parts = fish_quantity.split('/')
            if len(parts) == 2:
                fish_count_str, fish_capacity_str = parts
                if fish_count_str.isdigit() and fish_capacity_str.isdigit():
                    sleep_time(random.uniform(0.5, 0.6))
                    press_key('c')
                    sleep_time(random.uniform(0.5, 0.6))
                    return (int(fish_count_str), int(fish_capacity_str))
        sleep_time(random.uniform(0.5, 0.6))
    return None