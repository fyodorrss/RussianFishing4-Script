import time
import random
import pyperclip

import config
from utils import sleep_time
from ocr_global import ocr
import utils
from logger import logger  # ✅ 添加日志模块

# 自动更换拟饵
def change_bait():
    """
    自动更换损坏的拟饵
    """
    while not config.stop_event.is_set(): 
        # 判断拟饵是否损坏
        if utils.check_template_in_region(region=config.region_damaged_lure, template_path="damagedlure.png") and not config.is_need_renew_ticket:
            # 打开鱼竿配置界面
            sleep_time(random.uniform(0.52, 0.62))
            utils.press_key('v', 0.1)
            # 移动到可以滚动的地方
            sleep_time(random.uniform(0.52, 0.62))
            utils.move_mouse_random_in_region((1006, 129, 875, 927))  # 假设这是可以滚动的区域

            # 在指定区域找到损坏的拟饵，最多两处
            damaged_regions = utils.find_template_in_regions(config.region_check_damaged_bait_area, 'damaged.png', confidence=0.95)
            if len(damaged_regions) > 0:
                logger.info(f"检测到{len(damaged_regions)}处损坏的拟饵。")
                for i, r in enumerate(damaged_regions):
                    logger.info(f"匹配{i + 1}: {r}")
                    region = {"left": 1073, "top": r["top"] - 39, "width": 700, "height": 39}
                    sleep_time(random.uniform(0.52, 0.62))
                    damaged_bait_name = ocr.recognize_text_from_black_bg(region=region, fill_black=True, is_preprocess=True)
                    if len(damaged_bait_name) > 0:
                        damaged_bait_name = ' '.join([item for item in damaged_bait_name]).strip()                              
                        texts = ['BLU', 'RED', 'FLU', 'GRN', 'ORN', 'ROS', 'WHT', 'YEL']
                        for text in texts:
                            if text in damaged_bait_name and "WTA Fire Tubes" in damaged_bait_name:
                                damaged_bait_name = text
                                break
                        logger.info(f"损坏的拟饵名称: {damaged_bait_name}")
                        pyperclip.copy(damaged_bait_name)

                        sleep_time(random.uniform(0.22, 0.32))
                        utils.move_mouse_random_in_region((region["left"], region["top"], region["width"], region["height"]))
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.move_mouse_random_in_region((324, 104, 222, 23))
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()

                        sleep_time(random.uniform(0.22, 0.32))
                        utils.key_down('Left Ctrl')
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.press_key('v')
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.key_up('Left Ctrl')    
                        sleep_time(random.uniform(1.22, 1.32))

                        if damaged_bait_name == "RED":
                            cout = 0
                            max_attempts = 10
                            while not config.stop_event.is_set() and cout < max_attempts:
                                cout += 1
                                damaged_regions_red = utils.find_template_in_regions(config.region_check_damaged_bait_area_red, 'redtubes.png', confidence=0.95)
                                if len(damaged_regions_red) > 0:
                                    drr = damaged_regions_red[0]
                                    utils.move_mouse_random_in_region((drr["left"], drr["top"], drr["width"], drr["height"]))
                                    break
                                else:
                                    sleep_time(random.uniform(0.52, 0.62))
                                    utils.press_key_sc('PageDown')
                                    sleep_time(random.uniform(0.52, 0.62))
                        else:
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.move_mouse_random_in_region((285, 203, 166, 200))
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()
                        sleep_time(0.1)
                        utils.click_left_mouse()
                    else:
                        logger.warning("未识别到损坏的拟饵名称")
                        return
            
            # ------------------ 翻页 ------------------
            for _ in range(2):
                sleep_time(random.uniform(0.52, 0.62))
                utils.move_mouse_random_in_region((1006, 129, 875, 927))
                sleep_time(random.uniform(0.52, 0.62))
                utils.press_key_sc('PageDown')
                utils.press_key_sc('PageDown')
                sleep_time(random.uniform(0.52, 0.62))

                damaged_regions_second = utils.find_template_in_regions(config.region_check_damaged_bait_area, 'damaged.png', confidence=0.95)
                if len(damaged_regions_second) > 0:
                    logger.info(f"检测到第二页有{len(damaged_regions_second)}处损坏的拟饵。")
                    for i, r in enumerate(damaged_regions_second):
                        logger.info(f"匹配{i + 1}: {r}")
                        region = {"left": 1073, "top": r["top"] - 39, "width": 700, "height": 39}
                        sleep_time(random.uniform(0.52, 0.62))
                        damaged_bait_name_second = ocr.recognize_text_from_black_bg(region=region, fill_black=True, is_preprocess=True)
                        if len(damaged_bait_name_second) > 0:
                            damaged_bait_name_second = ' '.join([item for item in damaged_bait_name_second]).strip()                              
                            logger.info(f"损坏的拟饵名称: {damaged_bait_name_second}")
                            pyperclip.copy(damaged_bait_name_second)

                            sleep_time(random.uniform(0.22, 0.32))
                            utils.move_mouse_random_in_region((region["left"], region["top"], region["width"], region["height"]))
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.move_mouse_random_in_region((324, 104, 222, 23))
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()

                            sleep_time(random.uniform(0.22, 0.32))
                            utils.key_down('Left Ctrl')
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.press_key('v')
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.key_up('Left Ctrl')    
                            sleep_time(random.uniform(1.22, 1.32))

                            sleep_time(random.uniform(0.22, 0.32))
                            utils.move_mouse_random_in_region((285, 203, 166, 200))
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()
                            sleep_time(0.1)
                            utils.click_left_mouse()
                        else:
                            logger.warning("未识别到损坏的拟饵名称")
                            return

            sleep_time(random.uniform(0.52, 0.52))
            utils.press_key('v', 0.1)

        sleep_time(random.uniform(0.5, 0.6))
