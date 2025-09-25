import time
import random

import config
from utils import sleep_time
from ocr_global import ocr
import utils
from logger import logger 

#检查轮子的类型

def check_reel_type():
    """检查轮子类型"""
    
    utils.press_key('v')
    sleep_time(random.uniform(1, 1.1))

    reel_name = ocr.recognize_text_from_black_bg(
        region=config.region_reel_name,
        fill_black=True,
        is_preprocess=True
    )

    # 兼容返回字符串或列表
    if not reel_name:  # []、''、None 都会触发
        reel_name = ''
    elif isinstance(reel_name, list):
        reel_name = ' '.join(reel_name).strip()
    else:
        reel_name = str(reel_name).strip()

    logger.info(f"识别结果: {reel_name}")

    ELECTRIC_REELS = ["Reef Electro Raptor"]  # 可扩展更多电轮型号
    if reel_name and any(name in reel_name for name in ELECTRIC_REELS):
        logger.info("检测到电轮")
        config.is_electric_reel = True
    else:
        logger.info("检测到其他轮子")
        config.is_electric_reel = False

    sleep_time(random.uniform(0.22, 0.32))
    utils.press_key('v', 0.1)
    utils.press_key('v', 0.1)
