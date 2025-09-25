import time
import random
import config
from utils import sleep_time, stop_program
from ocr_global import ocr
from stages.check_fishnet_status import get_fish_count
import utils
import navigator
from stages.check_assembly import check_assembly
import time
import random
import config
import navigator
import utils
from stages.check_fishnet_status import get_fish_count
from logger import logger
import tkinter as tk
from tkinter import messagebox

def in_sea_map():
    """
    检查是否在海图页面，如果不在则提示用户并终止程序。
    如果在游戏界面则检查是否需要回城。
    """
    while not config.stop_event.is_set():
        """
        是否在游戏界面
        """
        if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
            logger.info("🎣 已在游戏界面，准备操作...")
            break
        sleep_time(random.uniform(0.4, 0.5))

    # 拿出鱼竿
    if not config.is_fly_ticket:
        sleep_time(random.uniform(0.42, 0.52))
        utils.press_key(config.fishing_rod_btn)
        sleep_time(random.uniform(2, 2.1))

    #检查拟饵的配置情况
    check_assembly()
    
    # 获取当前坐标 + 鱼护状态
    current_pos = navigator.get_current_position()
    logger.debug(f"启动时的坐标: {current_pos}")

    fish_quantity = get_fish_count()
    logger.debug(f"启动时的鱼护: {fish_quantity}")
    
    if current_pos and fish_quantity:
        fish_count, fish_capacity = fish_quantity
        # 如果已出海且鱼护空余充足，则不需要回城
        if current_pos[0] > 230 and (fish_capacity - fish_count) > 0 and not config.need_restart_sign:
            config.need_back = False
            logger.info("🛳️ 不需要小退。")
            return
        
    config.need_back = True
    config.need_restart_sign=False
    logger.info("🛳️ 需要小退。")

    # 尝试进入菜单（用于后续检测是否处于海图）
    sleep_time(random.uniform(0.23, 0.24))
    utils.press_key('esc')
    sleep_time(random.uniform(0.25, 0.26))

    # 判断是否在海图
    if not config.stop_event.is_set():
        st=time.time()
        while not config.stop_event.is_set() and time.time()-st<5:
            sea_name = ocr.recognize_text_from_black_bg_first(region=config.MapPickerRegionScreenshotFly if config.is_fly_ticket else config.MapPickerRegionScreenshot)
            if sea_name and sea_name.strip() == "挪威海":
                logger.info("✅ 当前已在海图界面。")
                return
            sleep_time(random.uniform(0.4, 0.5))    
        logger.warning("⚠️ 未检测到海图，弹窗提醒用户后终止程序。")
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)  # 设置最前
        messagebox.showwarning("警告", f"请先进入海图界面后再运行程序。", parent=root)
        root.destroy()  # 弹窗后销毁隐藏窗口
        stop_program()    


