import random
import time
import keyboard
import config
from logger import logger
import navigator
import utils
from gui_config import launch_config_window  # ✅ GUI 配置窗口（Tkinter）

# ✅ 守护线程：监视 need_restart 并执行重启
def monitor_and_restart():
    while True:
        time.sleep(random.uniform(1.04, 1.06))
        #服务器失联
        lossgameconnect = utils.check_template_in_region(config.LossGameConnectRegionScreenshot, template_path="lossgameconnect.png")
        gift = utils.find_template_in_regions(config.GiftRegionScreenshot, template_filename="gift.png")
        serverloss = utils.check_template_in_region(config.ServerLossRegionScreenshot, template_path="serverloss.png")
        login_error_match = utils.check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png")
        
        if login_error_match:
            logger.info("检测到登陆错误，准备重新登录。")
            time.sleep(random.uniform(0.23, 0.235))
            utils.move_mouse_random_in_region(region=config.ServerLossRegionClick)
            time.sleep(random.uniform(2.23, 3.235))
            utils.click_left_mouse()
            # 等待出现重新登录界面
            while not config.stop_event.is_set():
                login_error_match = utils.check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png")
                steam_match = utils.check_template_in_region(config.SteamLoginRegionScreenshot, template_path="steamlogin.png")
                standalone_match = utils.check_template_in_region(config.StandaloneLoginRegionScreenshot, template_path="standalonelogin.png")
                if login_error_match:
                    break
                if steam_match:
                    logger.info("检测到Steam登录界面，准备重新登录。")
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.move_mouse_random_in_region(region=config.SteamLoginRegionClick)
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.click_left_mouse()
                    break
                if standalone_match:
                    logger.info("检测到独立登录界面，准备重新登录。")
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.move_mouse_random_in_region(region=config.StandaloneLoginRegionClick)
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.click_left_mouse()
                    break
                time.sleep(random.uniform(0.04, 0.06))
            while not config.stop_event.is_set():    
                login_error_match = utils.check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png")
                if login_error_match:
                    break
                # 是否在游戏界面
                if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
                    logger.info("已在游戏界面。")
                    time.sleep(random.uniform(2.23, 3.235))
                    config.need_restart=True
                    break    
                time.sleep(random.uniform(0.04, 0.06))    

        if serverloss:
            logger.warning("🔁 检测到服务器未响应")
            time.sleep(random.uniform(0.23, 0.235))
            utils.move_mouse_random_in_region(region=config.ServerLossRegionClick)
            time.sleep(random.uniform(0.23, 0.235))
            utils.click_left_mouse()
            # 等待出现重新登录界面
            while True:
                serverloss = utils.check_template_in_region(config.ServerLossRegionScreenshot, template_path="serverloss.png")
                steam_match = utils.check_template_in_region(config.SteamLoginRegionScreenshot, template_path="steamlogin.png")
                standalone_match = utils.check_template_in_region(config.StandaloneLoginRegionScreenshot, template_path="standalonelogin.png")
                if serverloss:
                    break
                if steam_match:
                    logger.info("检测到Steam登录界面，准备重新登录。")
                    time.sleep(random.uniform(0.23, 0.235))
                    utils.move_mouse_random_in_region(region=config.SteamLoginRegionClick)
                    time.sleep(random.uniform(0.23, 0.235))
                    utils.click_left_mouse()
                    break
                if standalone_match:
                    logger.info("检测到独立登录界面，准备重新登录。")
                    time.sleep(random.uniform(0.23, 0.235))
                    utils.move_mouse_random_in_region(region=config.StandaloneLoginRegionClick)
                    time.sleep(random.uniform(0.23, 0.24))
                    utils.click_left_mouse()
                    break
                time.sleep(random.uniform(0.04, 0.06))
            while not config.stop_event.is_set():    
                serverloss = utils.check_template_in_region(config.ServerLossRegionScreenshot, template_path="serverloss.png")
                if serverloss:
                    break
                # 是否在游戏界面
                if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
                    logger.info("已在游戏界面。")
                    time.sleep(random.uniform(2.23, 3.235))
                    config.need_restart=True
                    break    
                time.sleep(random.uniform(0.04, 0.06))    

        if lossgameconnect:
            logger.warning("🔁 检测到服务器失联，立即重启")
            time.sleep(random.uniform(0.23, 0.235))
            utils.move_mouse_random_in_region(region=config.LossGameConnectRegionClick)
            time.sleep(random.uniform(0.23, 0.235))
            utils.click_left_mouse()
             # 等待出现重新登录界面
            while not config.stop_event.is_set():
                steam_match = utils.check_template_in_region(config.SteamLoginRegionScreenshot, template_path="steamlogin.png")
                standalone_match = utils.check_template_in_region(config.StandaloneLoginRegionScreenshot, template_path="standalonelogin.png")
                lossgameconnect = utils.check_template_in_region(config.LossGameConnectRegionScreenshot, template_path="lossgameconnect.png")
                if lossgameconnect:
                    break
                if steam_match:
                    logger.info("检测到Steam登录界面，准备重新登录。")
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.move_mouse_random_in_region(region=config.SteamLoginRegionClick)
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.click_left_mouse()
                    break
                if standalone_match:
                    logger.info("检测到独立登录界面，准备重新登录。")
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.move_mouse_random_in_region(region=config.StandaloneLoginRegionClick)
                    time.sleep(random.uniform(2.23, 3.235))
                    utils.click_left_mouse()
                    break
                time.sleep(random.uniform(0.04, 0.06))
            while not config.stop_event.is_set():    
                lossgameconnect = utils.check_template_in_region(config.LossGameConnectRegionScreenshot, template_path="lossgameconnect.png")
                if lossgameconnect:
                    break
                # 是否在游戏界面
                if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
                    logger.info("已在游戏界面。")
                    time.sleep(random.uniform(2.23, 3.235))
                    config.need_restart=True
                    break    
                time.sleep(random.uniform(0.04, 0.06))

        if len(gift)>0:
            time.sleep(random.uniform(0.43, 0.45))
            utils.press_key('Space')

        if config.need_restart:
            logger.warning("🔁 检测到 need_restart=True，立即重启")
            config.need_restart = False
            config.need_restart_sign = True
            utils.stop_program()
            utils.delayed_start()


# ✅ 热键绑定（运行在后台线程中）
def hotkey_listener():
    keyboard.add_hotkey(config.START_HOTKEY, utils.delayed_start)
    keyboard.add_hotkey(config.STOP_HOTKEY, utils.stop_program)
    # keyboard.add_hotkey(config.EXIT_HOTKEY, lambda: os._exit(0))  # 立即退出整个进程
    # logger.info("🎮 热键监听已启动（在后台线程中）")
    time.sleep(0.5)
    logger.info(f"🎮 按 {config.START_HOTKEY} 启动，{config.STOP_HOTKEY} 停止。")
    keyboard.wait()  # 会阻塞线程，但不影响主线程的 GUI


def main():

    utils.start_daemon_thread(monitor_and_restart)

    utils.start_daemon_thread(hotkey_listener)

    # ✅ 主线程运行 GUI（Tkinter 要求）
    logger.info("🚀 正在启动配置界面")
    launch_config_window()
    
    #清理按键
    utils.cleanup_keys()

    # ❌ 不再使用 keyboard.wait()，因为 GUI 窗口在主线程，关闭 GUI 即退出
    logger.info("👋 GUI 退出，程序结束")


if __name__ == "__main__":
    main()
