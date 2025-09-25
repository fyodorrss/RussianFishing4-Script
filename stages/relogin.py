import tkinter as tk
from tkinter import messagebox
import time
import random
import datetime

import config
import navigator
from utils import sleep_time, stop_program
from ocr_global import ocr
import utils
from logger import logger  # ✅ 添加日志模块

def schedule_next_rest():
    """生成当天必休的随机休息时间（全天随机）"""
    now = datetime.datetime.now()

    # 随机生成时间点（全天 0~23 小时，0~59 分钟）
    rand_hour = random.randint(0, 23)
    rand_minute = random.randint(0, 59)
    rest_start = datetime.datetime(now.year, now.month, now.day, rand_hour, rand_minute)

    # 如果随机时间已过 → 调整到未来1分钟内，保证今天能休息
    if rest_start <= now:
        rest_start = now + datetime.timedelta(minutes=1)

    # 随机休息时长（秒）
    rest_duration = random.uniform(config.min_sleep_time, config.max_sleep_time) * 3600

    # 保存配置
    config.next_rest_time = rest_start.timestamp()
    config.rest_duration = rest_duration
    config.rest_done_today = False

    logger.info(f"已设定每日休息时间: {rest_start.strftime('%Y-%m-%d %H:%M')} "
                f"持续 {rest_duration/3600:.2f} 小时")


def check_and_rest():
    """检查是否需要进入休息"""
    now = time.time()
    today = datetime.date.today()

    # 如果还没生成，或跨天 → 重新生成
    if (config.next_rest_time is None or
        datetime.datetime.fromtimestamp(config.next_rest_time).date() != today):
        schedule_next_rest()

    # 如果今天还没休息并且时间已到
    if not config.rest_done_today and now >= config.next_rest_time:
        hours = config.rest_duration / 3600
        logger.info(f"进入每日休息，暂停脚本 {hours:.2f} 小时")
        
        # 分段休息，每分钟检查是否中断
        elapsed = 0
        interval = 60  # 秒
        while elapsed < config.rest_duration:
            if hasattr(config, "stop_event") and config.stop_event.is_set():
                logger.info("休息被中断")
                break
            sleep_time(min(interval, config.rest_duration - elapsed))
            elapsed += interval

        logger.info("休息结束，恢复脚本运行")
        config.rest_done_today = True

        # ✅ 自动生成明天的休息时间
        schedule_next_rest_for_tomorrow()

    else:
        # 每小时打印一次剩余时间，避免刷屏
        remain = config.next_rest_time - now
        if remain > 0 and remain % 3600 < 60:
            h, m = divmod(int(remain // 60), 60)
            logger.info(f"距离每日休息还有 {h} 小时 {m} 分钟")


def schedule_next_rest_for_tomorrow():
    """生成明天的随机休息时间"""
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    rand_hour = random.randint(0, 23)
    rand_minute = random.randint(0, 59)
    rest_start = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, rand_hour, rand_minute)
    rest_duration = random.uniform(config.min_sleep_time, config.max_sleep_time) * 3600

    config.next_rest_time = rest_start.timestamp()
    config.rest_duration = rest_duration
    config.rest_done_today = False

    logger.info(f"已设定明日休息时间: {rest_start.strftime('%Y-%m-%d %H:%M')} "
                f"持续 {rest_duration/3600:.2f} 小时")

# ========== 小退操作 ==========
def relogin():
    """
    重新登录游戏，并在检测到登录界面时，可能触发每日随机休息 3~4 小时（每天一次）
    """
    while not config.stop_event.is_set():
        # 是否在菜单界面
        if ocr.recognize_text_from_black_bg_first(
            region=config.QuitGameButtonRegionScreenshotFly if config.is_fly_ticket else config.QuitGameButtonRegionScreenshot
        ).strip() == "退出":
            break

        # 是否在游戏界面
        if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
            logger.info("已在游戏界面。")
            sleep_time(random.uniform(0.23, 0.24))
            utils.press_key('esc')
            sleep_time(random.uniform(0.25, 0.26))
            break
        
        sleep_time(random.uniform(0.4, 0.5))
    
    if not config.stop_event.is_set():
        # 把鼠标移动到退出游戏按钮区域
        sleep_time(random.uniform(0.23, 0.235))
        utils.move_mouse_random_in_region(
            region=config.QuitGameButtonRegionClickFly if config.is_fly_ticket else config.QuitGameButtonRegionClick
        )
        sleep_time(random.uniform(0.53, 0.54))
        utils.key_down('Left Shift')
        sleep_time(random.uniform(0.53, 0.54))
        utils.click_left_mouse(0.02)
        sleep_time(random.uniform(0.53, 0.54))
        utils.key_up('Left Shift')

    if not config.stop_event.is_set():
        # 把鼠标移动到确定按钮区域
        sleep_time(random.uniform(0.23, 0.235))
        utils.move_mouse_random_in_region(region=config.QuitConfirmButtonRegionClick)
        sleep_time(random.uniform(0.23, 0.24))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.23, 0.24))

    # 等待出现重新登录界面
    steam_match = standalone_match = False
    while not config.stop_event.is_set():
        steam_match = utils.check_template_in_region(config.SteamLoginRegionScreenshot, template_path="steamlogin.png")
        standalone_match = utils.check_template_in_region(config.StandaloneLoginRegionScreenshot, template_path="standalonelogin.png")
        if steam_match or standalone_match:
            logger.info("检测到%s登录界面。" % ("Steam" if steam_match else "独立"))

            # ✅ 每日随机休息逻辑
            check_and_rest()

            # 继续登录操作
            if steam_match:
                logger.info("准备重新登录Steam端。")
                sleep_time(random.uniform(0.23, 0.235))
                utils.move_mouse_random_in_region(region=config.SteamLoginRegionClick)
                sleep_time(random.uniform(0.23, 0.235))
                utils.click_left_mouse()
                break
            if standalone_match:
                logger.info("准备重新登录独立端。")
                sleep_time(random.uniform(0.23, 0.235))
                utils.move_mouse_random_in_region(region=config.StandaloneLoginRegionClick)
                sleep_time(random.uniform(0.23, 0.24))
                utils.click_left_mouse()
                break
        sleep_time(random.uniform(0.04, 0.06))

    while not config.stop_event.is_set():
        fish_match = utils.check_template_in_region(config.FishRegionScreenshot, "fish.png")
        login_error_match = utils.check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png")
        if fish_match:
            logger.info("重新登录成功")
            break
        if login_error_match:
            # 如果Steam端登录失败，重启游戏
            if steam_match:
                utils.restart_game()
                continue
            # 如果独立端登陆失败，退出游戏
            if standalone_match:
                logger.warning("登录错误！独立端填写密码和勾选记住密码。")
                root = tk.Tk()
                root.withdraw()  # 隐藏主窗口
                root.attributes("-topmost", True)  # 设置最前
                messagebox.showwarning("警告", f"登录错误！独立端检测密码和勾选记住密码！", parent=root)
                root.destroy()
                stop_program()
                return  # ✅ 直接退出 relogin

        sleep_time(random.uniform(0.04, 0.06))
