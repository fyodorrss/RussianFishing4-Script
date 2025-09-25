import random
import sys
import time
from tkinter import messagebox
import tkinter as tk
import pyperclip
import config
import dxgi
from logger import logger
import navigator
from stages.check_fishnet_status import get_fish_count_other
from stages.relogin import relogin
from stages.sell_fish import sell_fish_func
import utils
from utils import sleep_time, stop_program
from ocr_global import ocr
import threading

def turn_and_walk(turn_value, walk_time, sleep_min=0.23, sleep_max=0.33):
    if not config.stop_event.is_set():       
        # 转向
        sleep_time(random.uniform(sleep_min, sleep_max))
        utils.move_mouse_relative_smooth(
            turn_value, 0,
            duration=random.uniform(0.4, 0.6),
            steps=random.randint(30, 50),
            interrupt_checker=lambda: getattr(config, 'running', True)
        )
    if not config.stop_event.is_set():   
        # 向前走
        sleep_time(random.uniform(sleep_min, sleep_max))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(walk_time)
        utils.key_up('w')
        utils.key_up('Left Shift')

def position_72_85():
    route = [
        (1080, 6),
        (650, 1.5),
        (-500, 0)
    ]

    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_87_103():
    route = [
        (0, 1),
        (-450, 6),
        (315, 9.5),
        (-570, 1.5),
        (-500, 0)

    ]

    for turn, walk in route:
        turn_and_walk(turn, walk)

def run_loop():
    if config.hand_rod_fishing_mode ==1:
        all_day_hand_rod_fishing()
    elif config.hand_rod_fishing_mode ==2:
        shougan()

def goToMap():

    while not config.stop_event.is_set():
        if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
            logger.info("已在游戏界面。")
            break
        sleep_time(random.uniform(0.4, 0.5))
        
    #进入游戏菜单
    sleep_time(random.uniform(0.23, 0.24))
    utils.press_key('esc')
    sleep_time(random.uniform(0.55, 0.56))

    if config.hand_rod_fishing_map==1:
        mapName='惟有诺克河'
        region=config.weiyouMapPickerRegionScreenshotClick
    elif config.hand_rod_fishing_map==2:
        mapName='北顿涅茨河'
        region=config.BeidunMapPickerRegionScreenshotClick
    
    #查看是不是在指定的地图中
    map_name1 = ocr.recognize_text_from_black_bg_first(region=config.MapPickerRegionScreenshotFly)
    map_name2 = ocr.recognize_text_from_black_bg_first(region=config.MapPickerRegionScreenshot)
    print(map_name1, map_name2)
    if (map_name1 and mapName in map_name1.replace(" ", "") ) or (map_name2 and mapName in map_name2.replace(" ", "")) :
        logger.info("✅ 当前已在指定地图中。")
        #小退游戏还原状态
        relogin()
    else:
        #进入指定的地图中
        #进入地图选择界面
        if config.stop_event.is_set():
            return
        sleep_time(random.uniform(0.23, 0.235))
        utils.move_mouse_random_in_region(region=config.MapPickerRegionScreenshotClick)
        sleep_time(random.uniform(0.23, 0.24))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.23, 0.24))
        #移动到指定的地图
        if config.stop_event.is_set():
            return
        sleep_time(random.uniform(0.23, 0.235))
        utils.move_mouse_random_in_region(region)
        sleep_time(random.uniform(0.23, 0.24))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.23, 0.24))
        #点击进入按钮
        if config.stop_event.is_set():
            return
        sleep_time(random.uniform(0.23, 0.235))
        utils.move_mouse_random_in_region(region=config.MapPickerConfirmButtonRegionClick)
        sleep_time(random.uniform(0.23, 0.24))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.53, 0.54))

        if utils.check_template_in_region(config.MapLimitRegionScreenshot, "maplimit.png"):
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)  # 设置最前
            messagebox.showwarning("警告", f"进入地图出错，查看等级限制！", parent=root)
            root.destroy()  # 弹窗后销毁隐藏窗口
            stop_program() 

        #判断是否进图成功
        while not config.stop_event.is_set():
            if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
                logger.info("进入地图成功。")
                break
            sleep_time(random.uniform(0.4, 0.5))

    #卖鱼
    #1.查看鱼护数量
    fish_quantity = get_fish_count_other()
    if fish_quantity:
        fish_count, fish_capacity = fish_quantity
        logger.info(f"鱼护当前数量: {fish_count}, 容量: {fish_capacity}")
        if fish_count > 0:
            if config.hand_rod_fishing_map==1:
                #咖啡厅任务
                if config.stop_event.is_set():
                    return
                sleep_time(random.uniform(1.23, 1.33))
                utils.move_mouse_relative_smooth(-500, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
                
                if config.stop_event.is_set():
                    return
                sell_fish_func()

                if config.stop_event.is_set():
                    return
                sleep_time(random.uniform(1.23, 1.33))
                utils.move_mouse_relative_smooth(500, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
                sleep_time(random.uniform(1.23, 1.33))
            
            elif config.hand_rod_fishing_map==2:

                # 向左转
                if config.stop_event.is_set():
                    return
                sleep_time(random.uniform(1.23, 1.33))
                utils.move_mouse_relative_smooth(-1450, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

                # 向前走
                if config.stop_event.is_set():
                    return
                sleep_time(random.uniform(1.23, 1.33))
                utils.key_down('Left Shift')
                utils.key_down('w')
                sleep_time(5)
                utils.key_up('w')
                utils.key_up('Left Shift')

                if config.stop_event.is_set():
                    return
                sell_fish_func()
                
                # 向前走
                if config.stop_event.is_set():
                    return
                sleep_time(random.uniform(1.23, 1.33))
                utils.key_down('Left Shift')
                utils.key_down('s')
                sleep_time(5)
                utils.key_up('s')
                utils.key_up('Left Shift')

                # 向右转
                if config.stop_event.is_set():
                    return
                sleep_time(random.uniform(1.23, 1.33))
                utils.move_mouse_relative_smooth(1450, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
                sleep_time(random.uniform(1.23, 1.33))

def hand_next_position():
    
    if config.hand_rod_fishing_map==1:
        positions=[{"point_id":"7285"},{"point_id":"87103"}]
    elif config.hand_rod_fishing_map==2:
        positions=[]

    # 检查点位列表是否为空
    if not positions:
        logger.error("点位列表为空")
        raise ValueError("选定的点位列表为空")

    # 检查 hand_map 是否变更
    last_hand_map = getattr(config, "last_hand_map", None)
    if last_hand_map != config.hand_rod_fishing_map:
        config.hand_rod_last_position_index = -1  # 重置 last_position_index
        logger.info(f"hand_map 变更：{last_hand_map} -> {config.hand_rod_fishing_map}，重置 hand_rod_last_position_index 为 -1")
        config.last_hand_map = config.hand_rod_fishing_map  # 更新 last_hand_map

    # 计算下一个索引
    last_index = getattr(config, "hand_rod_last_position_index", -1)
    next_index = (last_index + 1) % len(positions)

    item=positions[next_index]
    func=f"position_{item['point_id'][:2]}_{item['point_id'][2:]}"
    func=getattr(sys.modules[__name__], func)
    # meters=item["meters"]

    # 调用函数
    func()    

    # 更新状态
    config.hand_rod_last_position_index = next_index
    logger.info(f"已更新 config.hand_rod_last_position_index = {next_index}")

    # return int(meters)

def fish_mode_change():
    """
    根据 auto_mode 判断是否需要重启
    """
    now = time.time()

    # === 运行满 1 小时后重启 ===
    if config.hand_rod_fishing_mode ==1:
        elapsed = (now - config.current_fish_start_time)/ 60  # 转分钟
        if elapsed >= 60:
            logger.info("⏰ 系统时间已运行 %.1f 分钟，执行重启！（auto_mode=%s）", elapsed, config.auto_mode)
            config.need_restart = True
            return True
        return False

# 全天手杆钓鱼
def all_day_hand_rod_fishing():
    """全天手杆钓鱼"""
    logger.info("🎣 开始全天手杆")
    if config.stop_event.is_set():
        return
    goToMap()
    if config.stop_event.is_set():
        return
    #前往目的地
    sleep_time(random.uniform(1.41, 1.52))
    hand_next_position()

    #模式为0，1，计时开始
    if config.hand_rod_fishing_mode ==1:
        config.current_fish_start_time=time.time()    
    # 钓鱼
    sleep_time(random.uniform(1.41, 1.52))
    shougan()

def reconfigure_rod():
    """竿子状态异常，重新配置鱼竿"""

    def wait_random(min_max=(0.52, 0.62)):
        sleep_time(random.uniform(*min_max))

    def paste_text(text):
        utils.key_down('Left Ctrl')
        wait_random((0.05, 0.1))
        pyperclip.copy(text)
        utils.press_key('v')
        wait_random((0.05, 0.1))
        utils.key_up('Left Ctrl')

    def stopped():
        return config.stop_event.is_set()

    # === 打开鱼竿配置界面 ===
    if stopped():
        return
    utils.press_key('v', 0.1)
    wait_random((0.81, 0.92))
    utils.move_mouse_random_in_region((1006, 129, 875, 927))

    # === 需要配置的部位 (region, 名称) ===
    parts = [
        (config.region_hand_rod_main_line, config.hand_rod_main_line_name),
        (config.region_hand_rod_float, config.hand_rod_float_name),
        (config.region_hand_rod_sink, config.hand_rod_sink_name),
        (config.region_hand_rod_leader_line, config.hand_rod_leader_line_name),
        (config.region_hand_rod_hook, config.hand_rod_hook_name),
        (config.region_hand_rod_bait1, config.hand_rod_bait_name1),
        (config.region_hand_rod_bait2, config.hand_rod_bait_name2),
    ]

    # === 循环配置每个部位 ===
    for region, name in parts:
        if stopped():
            return
        if not name:  # 没有配置就跳过
            continue

        # 点击部位区域
        wait_random()
        utils.move_mouse_random_in_region(region)
        wait_random()
        utils.click_left_mouse()

        # 点击输入框
        if stopped():
            return
        wait_random()
        utils.move_mouse_random_in_region((324, 104, 222, 23))  # 输入框区域
        wait_random()
        utils.click_left_mouse()
        wait_random()
        utils.click_left_mouse()

        # 粘贴名字
        if stopped():
            return
        wait_random()
        paste_text(name)
        wait_random((1.22, 1.32))

        # 检查是否为空装备
        if stopped():
            return
        empty_region = {"left": 859, "top": 606, "width": 190, "height": 23}
        if utils.check_template_in_region(empty_region, 'empty.png', threshold=0.95):
            wait_random()
            utils.press_key('Esc', 0.1)
            wait_random()
            continue

        # 选择第一个结果
        utils.move_mouse_random_in_region((285, 203, 166, 200))
        if stopped():
            return
        wait_random()
        utils.click_left_mouse()
        sleep_time(0.1)
        utils.click_left_mouse()
        wait_random((0.5, 0.6))

    # === 关闭界面 ===
    utils.press_key('v', 0.1)
    wait_random((1.22, 1.32))

def shougan():
    total_mouse_movement = 0  # 记录总的鼠标x轴移动距离
    #抛竿
    def throw_rod():
        if utils.check_template_in_region(config.region_hook_status,'handerror.png'):
            sleep_time(random.uniform(0.41, 0.52))
            reconfigure_rod()
        if utils.check_template_in_region(config.region_cast_rod,'cast_rod.png'):
            utils.mouse_up_left()
            utils.key_up('Left Shift')
            sleep_time(random.uniform(0.41, 0.52))
            nonlocal total_mouse_movement
            # 还原视角：将鼠标移动回初始位置
            if total_mouse_movement != 0:
                print("正在还原视角...")
                utils.move_mouse_relative_smooth(
                    -total_mouse_movement, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50),
                    interrupt_checker=lambda: getattr(config, 'running', True)
                )
                total_mouse_movement = 0
                print("视角已还原")
            sleep_time(random.uniform(0.41, 0.52))
            t=1.8*(random.uniform(config.hand_rod_power,config.hand_rod_power+5)/100)
            utils.click_left_mouse(t)
            return True
        return False
    # 检测是否上鱼-静水
    def check_fish_still():
        while not config.stop_event.is_set():

            screenshot = None

            # screenshot = dxgi.grab_region(config.region_hand_rod_bite)
            # if screenshot is None:
                # logger.info(f"[⚠️] 截图失败: region={config.region_hand_rod_bite}")
                # continue

            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite1.png', threshold=0.5, screenshot=screenshot, use_gray=False):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite2.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite3.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite4.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite5.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite6.png', threshold=0.5, screenshot=screenshot, use_gray=False):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite7.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite8.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite9.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite10.png', threshold=0.5, screenshot=screenshot, use_gray=False):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite11.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite12.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite13.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite14.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite15.png', threshold=0.91, screenshot=screenshot):
                return True
            if utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png'):
                return True
            
            sleep_time(random.uniform(0.21, 0.22))
        return False
    # 检测是否上鱼-漂流
    def check_fish_drifting():
        start_time = time.time()
        inner_timeout = config.drifting_total_duration  # 50秒

        # === 新增：专用退出事件 ===
        move_stop_event = threading.Event()

        # === 新增：视角移动线程 ===
        def move_task():
            print("视角移动线程启动")
            nonlocal total_mouse_movement
            for _ in range(2):  # 总共移动两次
                if config.stop_event.is_set() or move_stop_event.is_set():
                    break
                wait_time = random.uniform(13, 15)
                for _ in range(int(wait_time * 10)):  # 0.1秒检查一次退出
                    if config.stop_event.is_set() or move_stop_event.is_set():
                        return
                    time.sleep(0.1)
                if not config.stop_event.is_set() and not move_stop_event.is_set():
                    print("视角移动中...")
                    utils.move_mouse_relative_smooth(400, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
                    total_mouse_movement += 400  # 记录移动距离

        move_thread = threading.Thread(target=move_task, daemon=True)
        move_thread.start()

        try:
            # === 原本逻辑保持不变 ===
            while not config.stop_event.is_set():
                inner_elapsed = time.time() - start_time
                if inner_elapsed >= inner_timeout:
                    print("漂流检测超时，重新抛竿")
                    return True
                screenshot=None
                # screenshot = dxgi.grab_region(config.region_hand_rod_bite)
                # if screenshot is None:
                #     logger.info(f"[⚠️] 截图失败: region={config.region_hand_rod_bite}")
                #     continue

                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite1.png', threshold=0.5, screenshot=screenshot, use_gray=False):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite2.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite3.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite4.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite5.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite6.png', threshold=0.5, screenshot=screenshot, use_gray=False):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite7.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite8.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite9.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite10.png', threshold=0.5, screenshot=screenshot, use_gray=False):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite11.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite12.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite13.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite14.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_fish(config.region_hand_rod_bite, 'hand_rod_bite15.png', threshold=0.91, screenshot=screenshot):
                    return True
                if utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png'):
                    return True

                sleep_time(random.uniform(0.21, 0.22))

            return False

        finally:
            # === 函数退出时确保线程退出 ===
            move_stop_event.set()
            move_thread.join(timeout=1)
    #抬竿收鱼
    def lift_rod():
        utils.mouse_down_left()
        # utils.key_down('Left Shift')
        start_time = time.time()
        inner_timeout = 10  # 20秒
        is_up_left = False
        #不断检测是否需要入护
        while not config.stop_event.is_set():
            inner_elapsed = time.time() - start_time
            if inner_elapsed >= inner_timeout:
                if not is_up_left:
                    utils.mouse_up_left()
                    is_up_left = True
                # return True
            # 鱼是不是已经收上来了
            if utils.check_template_in_region(config.region_keepnet, 'keepnet.png'):
                return True
            if utils.check_template_in_region(config.region_cast_rod,'cast_rod.png'):
                return False
            if utils.check_template_in_region(config.region_hook_status,'handerror.png'):
                return False
        return False
    #处理收上来的鱼
    def handle_fish():
        utils.mouse_up_left()
        utils.key_up('Left Shift')
        try:
            # === OCR识别阶段 ===
            t_ocr_start = time.time()
            fish_name, fish_info, weight = None, None, None

            fish_name = ocr.recognize_text_from_black_bg(config.region_fish_name, min_confidence=0.7)
            fish_info = ocr.recognize_text_from_black_bg(config.region_fish_info, min_confidence=0.7)

            fish_name = ''.join(fish_name).strip()
            fish_info = ''.join(fish_info).strip()

            if not fish_name or not fish_info:
                logger.info("信息识别不到！")
                utils.press_key('Space')
                return

            weight = utils.parse_weight(fish_info)
            if weight is not None:
                logger.info(f"🎣 检测到鱼名: {fish_name}, 鱼信息: {fish_info}")
            else:
                logger.info("信息识别不到！")
                utils.press_key('Space')
                return
            
            logger.debug(f"⏱️ OCR识别耗时: {time.time() - t_ocr_start:.3f} 秒")

        except Exception as e:
            logger.error(f"❗ 识别或判断出错: {e}")

        # === 模板颜色判断阶段 ===
        t_color_check = time.time()
        region = config.region_fish_name
        is_green = utils.find_template_in_regions(region, 'green.png', confidence=0.95)
        is_yellow = utils.find_template_in_regions(region, 'yellow.png', confidence=0.95)
        is_blue = utils.find_template_in_regions(region, 'blue.png', confidence=0.95)
        logger.debug(f"⏱️ 达标检测耗时: {time.time() - t_color_check:.3f} 秒")
        
        # === 鱼类判断逻辑阶段 ===
        t_judge = time.time()
        should_keep = False
        if is_green:
            logger.info("✅ 检测到达标鱼")
            should_keep = True
        elif is_yellow:
            logger.info("⭐ 检测到达标星鱼")
            utils.press_key('F12')
            sleep_time(random.uniform(1.2, 1.3))
            should_keep = True
        elif is_blue:
            logger.info("💠 检测到蓝冠鱼")
            utils.press_key('F12')
            sleep_time(random.uniform(1.2, 1.3))
            should_keep = True
        else:
            logger.info("❌ 检测不达标的鱼")
            if config.is_cut_fish:
                #切鱼肉
                if 500<=weight<3000:
                    should_keep = True
                    config.cut_fish_type = 3
            if config.keep_underperforming_fish:
                should_keep = True        

        logger.debug(f"⏱️ 鱼类判断耗时: {time.time() - t_judge:.3f} 秒")    
        
        # === 执行键盘指令阶段 ===
        t_press = time.time()
        if should_keep:
            logger.info(">> 入护 ✅")
            sleep_time(random.uniform(0.1, 0.2))
            utils.press_key('Space')
        else:
            logger.info(">> 扔掉 ❌")
            sleep_time(random.uniform(0.1, 0.2))
            utils.press_key('Backspace')

        logger.debug(f"⏱️ 按键执行耗时: {time.time() - t_press:.3f} 秒")
    #钓鱼主流程
    while not config.stop_event.is_set():
        if fish_mode_change():
            return
        #先抛竿
        if not throw_rod():
            continue
        #等待饵沉入水底
        t=1.8*(random.uniform(config.hand_rod_power,config.hand_rod_power+5)/100)
        time.sleep(random.uniform(t+1,t+1.2))
        #检测是否上鱼
        if config.water_status==1:
            if check_fish_still():
                #抬竿收鱼
                if lift_rod():
                    handle_fish()
        else:
            if check_fish_drifting():
                #抬竿收鱼
                if lift_rod():
                    handle_fish()
