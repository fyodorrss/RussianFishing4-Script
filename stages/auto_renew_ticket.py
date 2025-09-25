import time
import random

import pyautogui

import config
from utils import sleep_time
from ocr_global import ocr
import utils


from logger import logger

def auto_renew_ticket():
    """
    自动续费船票（优化版：限速 OCR、减少模板检测）
    """
    last_check_time = 0
    ocr_interval = 2.0  # 每2秒检查一次

    while not config.stop_event.is_set():

        now = time.time()
        
        # 🚦 限速 OCR 检测是否提示续费
        if now - last_check_time > ocr_interval:
            try:
                strs = ocr.recognize_text_from_black_bg(
                    config.RenewTicketTipRegionScreenshot, min_confidence=0.9
                )
                if any("请您选择下一张" in s.strip() for s in strs):
                    config.is_need_renew_ticket = True
                    logger.info("[续费检测] 检测到船票续费提示")
            except Exception as e:
                logger.error(f"[续费检测] OCR 异常: {e}")
            last_check_time = now

        # 🚀 自动续费流程
        if config.is_need_renew_ticket:
            while not config.stop_event.is_set():
                if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") and not config.is_important_action:
                    sleep_time(random.uniform(1.47, 1.57))
                    #先释放所有可能按下的按键
                    utils.mouse_up_left()
                    utils.key_up('Left Shift')
                    utils.mouse_up_right()
                    for key in ['w', 'a', 'd']:
                        pyautogui.keyUp(key)

                    utils.press_key('L')  # 打开续费界面
                    sleep_time(random.uniform(0.27, 0.37))
                    utils.move_mouse_random_in_region((284, 204, 166, 271))  # 选择票区域
                    sleep_time(random.uniform(0.27, 0.37))
                    utils.click_left_mouse()
                    sleep_time(0.1)
                    utils.click_left_mouse()
                    logger.info("✅ 已续费船票")
                    sleep_time(random.uniform(0.67, 0.77))
                    # 重置状态
                    config.is_need_renew_ticket = False
                    config.is_reeling_line = False
                    break
                sleep_time(0.1)

        sleep_time(0.2)  # 主循环更轻量
