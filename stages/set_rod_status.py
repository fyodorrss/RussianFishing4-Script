from collections import deque
import time
import random
from utils import sleep_time
from ocr_global import ocr
import config
import utils
from logger import logger

#自动打状态线程
def set_rod_status():
    """
    渔杆打状态
    """
    last_values=deque(maxlen=20) #检测鱼钩是不是到底了
    # 配置每种状态对应的 sleep 和 click 延迟
    status_action_map = {
        1: {"sleep": (0.8, 0.9), "click": (0.3, 0.33)},
        2: {"sleep": (1.4, 1.45), "click": (0.5, 0.6)},
        3: {"sleep": (1.5, 1.55), "click": (0.8, 0.9)},
        # 未来可扩展更多状态类型...
    }
    
    # 当前状态类型（来自 config）
    status_type = config.status_type  # 确保 config 是已导入的模块或变量

    # 从映射中获取该状态的行为参数
    action = status_action_map.get(status_type)

    while not config.stop_event.is_set():

        cast_line_meters = utils.get_cast_line_meters(ocr.recognize_text_from_black_bg(config.region_cast_line_meters,min_confidence=0.9))
        
        #这是不卡米的情况
        if utils.check_template_in_region(config.region_hook_status, 'hook_status.png',0.9) and not config.is_reeling_line and not config.is_sailing:
            logger.info("开始打状态")
            # 锁轮
            utils.click_left_mouse()
            is_locked=True
            # 参数
            hook_not_detected_count = 0
            max_not_detected_threshold = 3  # 可调参数，建议 2～5 之间
            while not config.stop_event.is_set() and not config.is_reeling_line:

                # 检测是否有图标
                hook_detected = utils.check_template_in_region(config.region_hook_status, 'hook_status.png',0.9)
                fish_bite_detected = utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png')

                if hook_detected:
                    hook_not_detected_count = 0  # 检测到，计数清零
                    if action:
                        # 执行延迟和点击操作
                        sleep_time(random.uniform(*action["sleep"]))
                        utils.key_down('Left Shift')
                        utils.click_right_mouse(random.uniform(*action["click"]))
                        utils.key_up('Left Shift')
                    else:
                        logger.info(f"⚠️ 未知的 status_type: {status_type}")
                                        
                else:
                    hook_not_detected_count += 1 
                    if is_locked and not fish_bite_detected and hook_not_detected_count >= max_not_detected_threshold:
                        # sleep_time(random.uniform(0.52, 0.62))
                        utils.press_key('Enter')
                        sleep_time(random.uniform(1.6, 1.7))
                        is_locked = False
                        hook_not_detected_count = 0  # 重置防抖
                        logger.info("放线出状态")
                        break

                sleep_time(random.uniform(0.1, 0.2))

        #这是卡米的情况
        elif config.cast_line_meters != 0 and not config.is_reeling_line and not config.stop_event.is_set() and not config.is_sailing:
            if cast_line_meters is not None and cast_line_meters == config.cast_line_meters :
                logger.info("开始打状态")
                # 锁轮
                utils.click_left_mouse()
                # 打状态（右键）
                while not config.stop_event.is_set() and not config.is_reeling_line:
                    if action:
                        # 执行延迟和点击操作
                        sleep_time(random.uniform(*action["sleep"]))
                        utils.key_down('Left Shift')
                        utils.click_right_mouse(random.uniform(*action["click"]))
                        utils.key_up('Left Shift')
                    else:
                        logger.info(f"⚠️ 未知的 status_type: {status_type}")

        #长时间没有触发沉底的图标，收线等待触发
        elif cast_line_meters is not None and not config.is_reeling_line and not config.stop_event.is_set() and cast_line_meters!=0 and not config.is_sailing:
            last_values.append(cast_line_meters)
            if len(last_values) == 20:
                if all(x == last_values[0] for x in last_values):
                    logger.info(last_values)
                    logger.info("已沉底！")
                    utils.click_left_mouse(0.5)
        
        sleep_time(random.uniform(0.5, 0.6))