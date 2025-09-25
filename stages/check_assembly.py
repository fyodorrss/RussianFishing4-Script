import tkinter as tk
from tkinter import messagebox
import time
import random

import config
from utils import sleep_time, stop_program
import utils
from logger import logger  # 确保导入

#检测装备是否齐全
def check_assembly(on_sea=False):
    """
    检查是否组装完成
    """
    sleep_time(random.uniform(0.01, 0.02))

    # 检查是否组装完成
    if utils.check_template_in_region(region=config.region_check_assembly_area, template_path="assembly.png"):
        if config.is_fly_ticket and on_sea:
            logger.warning("线组被咬断")
            #重新配置钓组
            sleep_time(random.uniform(2, 2.1))
            utils.press_key('v')
            #选择引线
            sleep_time(random.uniform(1.42, 1.52))
            utils.move_mouse_random_in_region((1001,511,64,64))
            sleep_time(random.uniform(0.42, 0.52))
            utils.click_left_mouse()
            sleep_time(random.uniform(0.42, 0.52))
            utils.move_mouse_random_in_region((285, 203, 166, 200))
            sleep_time(random.uniform(0.42, 0.52))
            utils.click_left_mouse()
            sleep_time(0.1)
            utils.click_left_mouse()
            #选择钩子
            sleep_time(random.uniform(1.42, 1.52))
            utils.move_mouse_random_in_region((1001,603,64,64))
            sleep_time(random.uniform(0.42, 0.52))
            utils.click_left_mouse()
            sleep_time(random.uniform(0.42, 0.52))
            utils.move_mouse_random_in_region((285, 203, 166, 200))
            sleep_time(random.uniform(0.42, 0.52))
            utils.click_left_mouse()
            sleep_time(0.1)
            utils.click_left_mouse()
            #选择饵
            sleep_time(random.uniform(1.42, 1.52))
            utils.move_mouse_random_in_region((1001,695,64,64))
            sleep_time(random.uniform(0.42, 0.52))
            utils.click_left_mouse()
            sleep_time(random.uniform(0.42, 0.52))
            utils.move_mouse_random_in_region((285, 203, 166, 200))
            sleep_time(random.uniform(0.42, 0.52))
            utils.click_left_mouse()
            sleep_time(0.1)
            utils.click_left_mouse()
            #关闭界面
            sleep_time(random.uniform(0.42, 0.52))
            utils.press_key('v', 0.1)  # 关闭界面

            sleep_time(random.uniform(1.52, 1.62))
            #重新抛竿,修补错误
            if config.is_cast_rod and utils.check_template_in_region(config.region_cast_rod,'cast_rod.png'):
                utils.click_left_mouse(random.uniform(0.08, 0.11))
            return
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)  # 设置最前
        messagebox.showwarning("警告", f"请配置好鱼竿！", parent=root)
        root.destroy()  # 弹窗后销毁隐藏窗口
        stop_program()
       
        
