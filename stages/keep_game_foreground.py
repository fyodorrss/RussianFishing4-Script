import win32gui
import win32con
import tkinter as tk
from tkinter import messagebox
import time
import win32api
import random
import config
from logger import logger
from utils import sleep_time, stop_program  # 添加 logger 导入

#把游戏置顶
def keep_game_foreground():
    """
    检测游戏是否运行，以及使游戏窗口保持在最前面
    """
    while not config.stop_event.is_set():
        hwnd = win32gui.FindWindow(None, config.TARGET_WINDOW_TITLE)
        if hwnd == 0:
            logger.warning(f"未检测到游戏：{config.TARGET_WINDOW_TITLE}")
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            root.attributes("-topmost", True)  # 设置最前
            messagebox.showwarning("警告", f"先启动游戏！", parent=root)
            root.destroy()  # 弹窗后销毁隐藏窗口
            stop_program()
        else:
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Alt down
                win32gui.SetForegroundWindow(hwnd)
                win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)  # Alt up
                # 获取客户区坐标 (左上角 (0, 0), 右下角 (width, height))
                left, top, right, bottom = win32gui.GetClientRect(hwnd)
                width = right - left
                height = bottom - top
                if width != 1920 or height != 1080:
                    logger.warning("只支持1920x1080分辨率的游戏窗口。")
                    root = tk.Tk()
                    root.withdraw()  # 隐藏主窗口
                    root.attributes("-topmost", True)  # 设置最前
                    messagebox.showwarning("警告", f"只支持1920x1080分辨率的游戏窗口！", parent=root)
                    root.destroy()  # 弹窗后销毁隐藏窗口
                    stop_program()

            except Exception as e:
                logger.error(f"激活目标窗口时出错：{e}")

        sleep_time(random.uniform(0.1, 0.2))  # 随机时间检查一次
