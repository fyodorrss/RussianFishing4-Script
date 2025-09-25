import random
import time
import pyperclip
import config
from logger import logger
import navigator
from stages.check_fishnet_status import get_fish_count_other
from stages.coffee_shop_task import coffee_shop_task_func
from stages.cut_fish import cut_fish
from stages.relogin import relogin
from stages.sell_fish import sell_fish_func
import utils
from utils import sleep_time, stop_program,start_daemon_thread
from stages.adjust_reel_settings import adjust_reel_friction,adjust_reel_meters,adjust_reel_speed
from stages.check_player_vitals import check_player_vitals
from stages.set_friction_from_slider import set_friction_from_slider
from ocr_global import ocr
import dxgi
import tkinter as tk
from tkinter import messagebox
import re
import sys
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
        if random.random() < 0.2:  # 20%长暂停
            sleep_time(random.uniform(5.0, 10.0))
            logger.info("模拟玩家暂停")
        # 向前走
        sleep_time(random.uniform(sleep_min, sleep_max))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(walk_time)
        utils.key_up('w')
        utils.key_up('Left Shift')

#老奥ob点位
def position_48_28():
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (750, 2),
        (-500, 4),
        (-70, 3),
        (130, 6),
        (-780, 23.5),
        (-530, 3.5),
        (340, 3.6),
        (-650, 4.5),
        (-450, 2.8),
        (350, 3.7),
    ]

    for turn, walk in route:
        turn_and_walk(turn, walk)
    
    if not config.stop_event.is_set():  
        # 向左转
        sleep_time(random.uniform(0.23, 0.33))
        utils.move_mouse_relative_smooth(-650, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    # if not config.stop_event.is_set():  
    #     # 向下转
    #     sleep_time(random.uniform(0.23, 0.33))
    #     utils.move_mouse_relative_smooth(0, 250, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

def position_42_32():
    # 定义路线： (转向角度, 前进时长)
    route = [
        (-100, 5),
        (900, 4.5),
        (355, 9.5),
        (620, 11),
        (-30, 6.8),
        (-700, 0.4),
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)
    # if not config.stop_event.is_set():      
    #     # 向下转
    #     sleep_time(random.uniform(0.23, 0.33))
    #     utils.move_mouse_relative_smooth(0, 250, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    
def position_35_29():
    # 定义路线： (转向角度, 前进时长)
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (-230, 10),
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

    if not config.stop_event.is_set():  
        # 向右转
        sleep_time(random.uniform(0.23, 0.33))
        utils.move_mouse_relative_smooth(370, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    # if not config.stop_event.is_set():  
    #     # 向右转
    #     sleep_time(random.uniform(0.23, 0.33))
    #     utils.move_mouse_relative_smooth(0, 250, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

def position_36_28():
    # 定义路线： (转向角度, 前进时长)
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (-230, 10),
        (-380, 1.5),
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)
    
    if not config.stop_event.is_set():
        # 向右转
        sleep_time(random.uniform(0.23, 0.33))
        utils.move_mouse_relative_smooth(670, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    # if not config.stop_event.is_set():
    #     # 向下转
    #     sleep_time(random.uniform(0.23, 0.33))
    #     utils.move_mouse_relative_smooth(0, 250, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

def position_25_41():
    
    # 定义路线： (转向角度, 前进时长)
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (750, 7.3),
        (-500, 1.2),
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

    # if not config.stop_event.is_set():    
    #     # 向下转
    #     sleep_time(random.uniform(0.23, 0.33))
    #     utils.move_mouse_relative_smooth(0, 250, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

def position_23_67():
   # 定义路线： (转向角度, 前进时长)
    route = [
        (-100, 7),
        (100, 4.2),
        (-550, 21.8),
        (-880, 1.8),
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)
    
    # if not config.stop_event.is_set():  
    #     # 向下转
    #     sleep_time(random.uniform(0.52, 0.65))
    #     utils.move_mouse_relative_smooth(0, 250, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

def position_20_34():
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (750, 2),
        (-500, 4),
        (-70, 3),
        (130, 6),
        (800, 3.4),
        (510,0.2)
    ]

    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_35_58():
    route = [
        (-100, 6),
        (-600,8.5),
        (600,1.7)
    ]

    for turn, walk in route:
        turn_and_walk(turn, walk)        

def position_23_45():
    # 定义路线： (转向角度, 前进时长)
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (750, 10),
        (570,2.2),
        (-735,0.7)
        
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_09_50():
    route = [
        (-100, 5),
        (-650, 6),
        (-550, 16),
        (750, 2),
        (-500, 4),
        (-70, 3),
        (130, 6),
        (800, 3.4),
        (-200,10),
        (200,9.5),
        (850,0.85),
        (60,0)
    ]

    for turn, walk in route:
        turn_and_walk(turn, walk)
            
    if not config.stop_event.is_set():  
        sleep_time(random.uniform(0.23, 0.33))
        utils.press_key('a',0.1)        

#铜壶点位
def position_66_55 ():
    # 定义路线
    route = [
        (-450, 5.5),
        (660, 1.6),
    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_56_50 ():
    # 定义路线
    route = [
        (-410, 7.5),
        (350, 2.5),
        (-330, 5.2),
        (380, 2),
        (470, 0.55),
        (50, 0),
    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_44_34 ():
    # 定义路线
    route = [
        (-410, 7.5),
        (350, 2.5),
        (-330, 9.3),
        (270, 8),
        (-850, 18),
        (800,5),
        (850, 0.5),
    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_37_32 ():
    # 定义路线
    route = [
        (-410, 7.5),
        (350, 2.5),
        (-330, 9.3),
        (270, 8),
        (-850, 18),
        (800,12),
        (650, 0.6),

    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_67_59 ():
    # 定义路线
    route = [
        (0, 4.3),
        (-250,0)
    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_67_58 ():
    # 定义路线
    route = [
        (0, 4.5),
        (-250,0),
    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

    if not config.stop_event.is_set():     
        sleep_time(random.uniform(0.23, 0.33))
        utils.key_down('Left Shift')
        utils.key_down('a')
        sleep_time(1)
        utils.key_up('a')
        utils.key_up('Left Shift')    

    if not config.stop_event.is_set():     
        sleep_time(random.uniform(0.23, 0.33))
        utils.move_mouse_relative_smooth(
            80, 0,
            duration=random.uniform(0.4, 0.6),
            steps=random.randint(30, 50),
            interrupt_checker=lambda: getattr(config, 'running', True)
            )

def position_66_59 ():
    # 定义路线
    route = [
        (0, 4.4),
        (-250,0),
    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

    if not config.stop_event.is_set():     
        sleep_time(random.uniform(0.23, 0.33))
        utils.key_down('Left Shift')
        utils.key_down('d')
        sleep_time(0.6)
        utils.key_up('d')

    if not config.stop_event.is_set():     
        sleep_time(random.uniform(0.23, 0.33))
        utils.move_mouse_relative_smooth(
            -100, 0,
            duration=random.uniform(0.4, 0.6),
            steps=random.randint(30, 50),
            interrupt_checker=lambda: getattr(config, 'running', True)
            )    

def bottom_next_position():
    
    if config.bottom_map==0:
        positions=config.laoao_points
    elif config.bottom_map==1:
        positions=config.hupo_points
    elif config.bottom_map==2:
        positions=config.tonghu_points    

    # 检查点位列表是否为空
    if not positions:
        logger.error("点位列表为空")
        raise ValueError("选定的点位列表为空")

    # 检查 bottom_map 是否变更
    last_bottom_map = getattr(config, "last_bottom_map", None)
    if last_bottom_map != config.bottom_map:
        config.bottom_last_position_index = -1  # 重置 last_position_index
        logger.info(f"bottom_map 变更：{last_bottom_map} -> {config.bottom_map}，重置 bottom_last_position_index 为 -1")
        config.last_bottom_map = config.bottom_map  # 更新 last_bottom_map

    # 计算下一个索引
    last_index = getattr(config, "bottom_last_position_index", -1)
    next_index = (last_index + 1) % len(positions)

    if config.need_restart_sign:
        next_index=last_index
        config.need_restart_sign=False

    item=positions[next_index]
    func=f"position_{item['point_id'][:2]}_{item['point_id'][2:]}"
    func=getattr(sys.modules[__name__], func)
    meters=item["meters"]

    # 调用函数
    func()    

    # 更新状态
    config.bottom_last_position_index = next_index
    logger.info(f"已更新 config.bottom_last_position_index = {next_index}, 卡米数={meters}")

    return int(meters)

#打狗线路
def dagou_path():

    #先去2167
    # 向左转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(-100, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(7)
    utils.key_up('w')
    utils.key_up('Left Shift')

    # 向左转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(100, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(4.2)
    utils.key_up('w')
    utils.key_up('Left Shift')

    # 向左转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(-550, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(23)
    utils.key_up('w')
    utils.key_up('Left Shift')

    # 向左转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(-700, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(2.5)
    utils.key_up('w')
    utils.key_up('Left Shift')

    # 向右转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(220, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向左转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(-1120, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(5)
    utils.key_up('w')
    utils.key_up('Left Shift')

    # 向右转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(320, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(2.5)
    utils.key_up('w')
    utils.key_up('Left Shift')

    # 向左转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(-220, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(6)
    utils.key_up('w')
    utils.key_up('Left Shift')

      # 向右转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(190, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(6)
    utils.key_up('w')
    utils.key_up('Left Shift')

     # 向左转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(-280, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(13)
    utils.key_up('w')
    utils.key_up('Left Shift')

     # 向右转
    sleep_time(random.uniform(0.52, 0.65))
    utils.move_mouse_relative_smooth(230, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    # 向前走
    sleep_time(random.uniform(0.23, 0.33))
    utils.key_down('Left Shift')
    utils.key_down('w')
    sleep_time(0.5)
    utils.key_up('w')
    utils.key_up('Left Shift')

#白河路亚点位
def position_71_37 ():
    # 定义路线
    route = [
        (-150, 8.5),
        (-600, 4),
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_66_28 ():
   # 路线表（按顺序走）
    route = [
        (-150, 8.5),  # 左转 -150，走 8.5s
        (-100, 6),    # 左转 -100，走 6s
        (50, 6),      # 右转 +50，走 6s
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)
        
    if not config.stop_event.is_set():  
        # 向左转
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(-500, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

def position_65_26 ():
   # 路线表
    route = [
        (-150, 8.5),  # 左转 -150，走 8.5s
        (-100, 6),    # 左转 -100，走 6s
        (50, 9),      # 右转 +50，走 9s
    ]

    # 按顺序执行
    for turn, walk in route:
        turn_and_walk(turn, walk)

def position_73_45 ():
    if not config.stop_event.is_set():  
        # 向左转
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(-600, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    if not config.stop_event.is_set():  
        # 向前走
        sleep_time(random.uniform(0.23, 0.33))
        utils.key_down('Left Shift')
        utils.key_down('w')
        sleep_time(3.5)
        utils.key_up('w')
        utils.key_up('Left Shift')
    if not config.stop_event.is_set():  
        # 向左转
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(-400, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

def position_73_59 ():
    # 路线表（你刚贴的两步）
    route = [
        (1100, 10.6),  # 左转 1100 → 前进 10.6 秒
        (650, 1.5),    # 右转 650 → 前进 1.5 秒
    ]

    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

    if not config.stop_event.is_set():   
        # 向左转
        sleep_time(random.uniform(0.52, 0.65))
        utils.move_mouse_relative_smooth(-80, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

#埃尔克湖点位
def position_65_93 ():
    # 定义路线
    route = [
        (-30, 5),
        (550, 0.8),
    ]
    # 执行路线
    for turn, walk in route:
        turn_and_walk(turn, walk)

def lure_next_position():
    """切换到下一个点位，并更新 config 状态"""
    positions=[]
    if config.lure_map==1:
        positions=config.baihe_lure_points
    elif config.lure_map==2:
        positions=config.aier_lure_points

    # 检查点位列表是否为空
    if not positions:
        logger.error("点位列表为空")
        raise ValueError("选定的点位列表为空")

    # 检查 lure_map 是否变更
    last_lure_map = getattr(config, "last_lure_map", None)
    if last_lure_map != config.lure_map:
        config.lure_last_position_index = -1  # 重置 lure_last_position_index
        logger.info(f"lure_map 变更：{last_lure_map} -> {config.lure_map}，重置 lure_last_position_index 为 -1")
        config.last_lure_map = config.lure_map  # 更新 last_lure_map

    # 计算下一个索引
    last_index = getattr(config, "lure_last_position_index", -1)
    next_index = (last_index + 1) % len(positions)

    if config.need_restart_sign:
        next_index=last_index
        config.need_restart_sign=False

    item=positions[next_index]
    func=f"position_{item['point_id'][:2]}_{item['point_id'][2:]}"
    func=getattr(sys.modules[__name__], func)
    # meters=item["meters"]

    # 调用函数
    func()    

    # 更新状态
    config.lure_last_position_index = next_index
    logger.info(f"已更新 config.lure_last_position_index = {next_index}")

def run_loop():
    if not config.auto_mode in (3,4):
        #进入指定的地图
        goToMap()
        #启动指定模板程序
        if config.current_fish_mode=='bottom':
            fish_bottom()
        else:
            fish_lure()
    else:
        if config.auto_mode==3:
            bottom(config.only_bottom_meters)
        elif config.auto_mode==4:
            lure()    

# 解析 00:00 格式为分钟
def parse_game_time(time_str):
    time_str = time_str.replace('O', '0').replace('o', '0')
    # 提取前面时间部分（支持 "22:13 |16.2°" 这种格式）
    if '|' in time_str:
        time_str = time_str.split('|')[0].strip()
    match = re.match(r'^(\d{2}):(\d{2})$', time_str)
    if not match:
        # logger.warning(f"时间格式错误: {time_str}")
        return None
    return int(match.group(1)) * 60 + int(match.group(2))

# 获取 OCR 游戏分钟数
def get_game_minutes():
    game_time1 = parse_game_time(ocr.recognize_text_from_black_bg_first(region=config.GameTimeRegionScreenshot))
    game_time2 = parse_game_time(ocr.recognize_text_from_black_bg_first(region=config.GameTimeRegionScreenshotFly))
    return game_time1 or game_time2 or None

def fish_mode_change():
    """
    根据 auto_mode 判断是否需要重启，并在游戏时间15:00-15:59重启前等待随机2-3分钟
    """
    # === auto_mode 0 / 1: 游戏时间 15:00 - 16:00 内重启一次 ===
    if config.auto_mode in (0, 1):
        try:
            minutes = parse_game_time(
                ocr.recognize_text_from_black_bg_first(region=config.GameTimeRegionScreenshotmain)
            )
        except ValueError as e:
            logger.warning("⚠️ OCR 时间解析失败: %s", e)
            return False

        if minutes is None:
            logger.debug("OCR 未识别到有效时间，跳过模式检测。")
            return False

        game_hour, game_minute = divmod(minutes, 60)

        # 如果游戏时间在 14:30~16:30 且今天还没重启过
        if ((game_hour == 14 and game_minute >= 30) or (game_hour == 15) or (game_hour == 16 and game_minute <= 30)) \
                and not getattr(config, "has_restarted_today", False):
            logger.info("⏰ 游戏时间 %02d:%02d 处于 14:30~16:30，准备等待1-5分钟后重启！（auto_mode=%s）",
                        game_hour, game_minute, config.auto_mode)

            wait_time = random.uniform(60, 300)  # 1-5 分钟
            logger.info("开始等待 %.2f 秒", wait_time)
            sleep_time(wait_time)

            logger.info("等待结束，执行重启")
            config.has_restarted_today = True
            utils.stop_program()
            utils.delayed_start()
            return True

        # 在 16:30 后重置重启标志
        if game_hour > 16 or (game_hour == 16 and game_minute > 30):
            config.has_restarted_today = False

        return False

    # === auto_mode 2: 白天/晚上切换逻辑 ===
    elif config.auto_mode == 2:
        try:
            minutes = parse_game_time(
                ocr.recognize_text_from_black_bg_first(region=config.GameTimeRegionScreenshotmain)
            )
        except ValueError as e:
            logger.warning("⚠️ OCR 时间解析失败: %s", e)
            return False

        if minutes is None:
            logger.debug("OCR 未识别到有效时间，跳过模式检测。")
            return False

        new_mode = "lure" if 540 <= minutes < 1080 else "bottom"

        if new_mode != config.current_fish_mode:
            logger.info("🎣 模式切换: %s → %s，准备重启！", config.current_fish_mode, new_mode)
            config.current_fish_mode = new_mode
            utils.stop_program()
            utils.delayed_start()
            return True

        return False

    return False

# 进入指定地图
def goToMap():
    fish_quantity=fish_capacity=fish_count=None
    while not config.stop_event.is_set():
        """
        是否在游戏界面
        """
        if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
            logger.info("已在游戏界面。")
            fish_quantity = get_fish_count_other()
            if fish_quantity:
                fish_count, fish_capacity = fish_quantity
                logger.info(f"鱼护当前数量: {fish_count}, 容量: {fish_capacity}")
            else:
                continue
            sleep_time(random.uniform(0.23, 0.24))
            utils.press_key('esc')
            sleep_time(random.uniform(0.25, 0.26))
            break
        
        sleep_time(random.uniform(0.4, 0.5))

    minutes=0

    while not config.stop_event.is_set():
        minutes = get_game_minutes()
        if minutes is not None:
            break
        logger.warning("无法识别游戏时间，重试中...")
        sleep_time(random.uniform(0.4, 0.5))


    if config.auto_mode==0:
        config.current_fish_mode='bottom'
    elif config.auto_mode==1:
        config.current_fish_mode= "lure"
    elif config.auto_mode==2:
        if 540 <= minutes < 1080:
            config.current_fish_mode= "lure"
        else:  
            config.current_fish_mode= "bottom"
    """
    前往指定的地图。
    """
    if config.current_fish_mode=='bottom':
        if config.bottom_map==0:
            mapName='斯特罗格湖'
            region=config.LaoaoMapPickerRegionScreenshotClick
        elif config.bottom_map==1:
            mapName='琥珀湖'
            region=config.HupohuMapPickerRegionScreenshotClick
        elif config.bottom_map==2:
            mapName='铜湖'        
            region=config.TonghuMapPickerRegionScreenshotClick
    else:
        if config.lure_map==0:
            mapName='斯特罗格湖'
            region=config.LaoaoMapPickerRegionScreenshotClick
        elif config.lure_map==1:
            mapName='白河'
            region=config.BaiheMapPickerRegionScreenshotClick
        elif config.lure_map==2:
            mapName='埃尔克湖'
            region=config.AierMapPickerRegionScreenshotClick

    #查看是不是在指定的地图中
    map_name1 = ocr.recognize_text_from_black_bg_first(region=config.MapPickerRegionScreenshotFly)
    map_name2 = ocr.recognize_text_from_black_bg_first(region=config.MapPickerRegionScreenshot)

    #先把鱼卖了
    if fish_count > 0:
        #小退游戏还原状态
        relogin()
        if (map_name1 and '铜湖' in map_name1.replace(" ", "") ) or (map_name2 and '铜湖' in map_name2.replace(" ", "")) :
            #转向咖啡厅
            sleep_time(random.uniform(1.23, 1.33))
            if config.stop_event.is_set():
                return
            utils.move_mouse_relative_smooth(-700, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
            #交任务
            if config.stop_event.is_set():
                return
            coffee_shop_task_func()
            #转向鱼市
            sleep_time(random.uniform(1.23, 1.33))
            if config.stop_event.is_set():
                return
            utils.move_mouse_relative_smooth(1700, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
            #卖鱼
            if config.stop_event.is_set():
                return
            sell_fish_func()
            #复原视角
            sleep_time(random.uniform(1.23, 1.33))
            if config.stop_event.is_set():
                return
            utils.move_mouse_relative_smooth(-1000, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
            sleep_time(random.uniform(1.23, 1.33))

        if (map_name1 and '斯特罗格湖' in map_name1.replace(" ", "") ) or (map_name2 and '斯特罗格湖' in map_name2.replace(" ", "")) :
            #转向咖啡厅
            sleep_time(random.uniform(1.23, 1.33))
            if config.stop_event.is_set():
                return
            route = [
                (920, 3.5)
            ]
            for turn, walk in route:
                turn_and_walk(turn, walk)
            #交任务
            if config.stop_event.is_set():
                return
            coffee_shop_task_func()
            #转向鱼市               
            sleep_time(random.uniform(1.23, 1.33))
            if config.stop_event.is_set():
                return
            route = [
                (750, 3.5)
            ]
            for turn, walk in route:
                turn_and_walk(turn, walk)
            #卖鱼                
            if config.stop_event.is_set():
                return
            sell_fish_func()
            sleep_time(random.uniform(1.23, 1.33))

        if (map_name1 and '白河' in map_name1.replace(" ", "") ) or (map_name2 and '白河' in map_name2.replace(" ", "")) :    
            #转向咖啡厅
            sleep_time(random.uniform(1.23, 1.33))
            if config.stop_event.is_set():
                return
            utils.move_mouse_relative_smooth(-400, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
            #交任务
            if config.stop_event.is_set():
                return
            coffee_shop_task_func()
            #转向鱼市
            sleep_time(random.uniform(1.23, 1.33))
            if config.stop_event.is_set():
                return
            utils.move_mouse_relative_smooth(400, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
            #卖鱼                
            if config.stop_event.is_set():
                return
            sell_fish_func() 
            sleep_time(random.uniform(1.23, 1.33))
        
        if (map_name1 and '埃尔克湖' in map_name1.replace(" ", "") ) or (map_name2 and '埃尔克湖' in map_name2.replace(" ", "")) :    
                #前往咖啡厅
                sleep_time(random.uniform(1.23, 1.33))
                route = [
                    (900, 12.5),
                    (300, 0),
                ]
                # 执行路线
                for turn, walk in route:
                    turn_and_walk(turn, walk)
                #交任务
                if config.stop_event.is_set():
                    return
                coffee_shop_task_func()
                #前往鱼市
                sleep_time(random.uniform(1.23, 1.33))
                route = [
                    (1200, 2.7),
                    (-650, 0)
                ]
                # 执行路线
                for turn, walk in route:
                    turn_and_walk(turn, walk)
                #卖鱼
                if config.stop_event.is_set():
                    return
                sell_fish_func()
                sleep_time(random.uniform(1.23, 1.33))

    if (map_name1 and mapName in map_name1.replace(" ", "") ) or (map_name2 and mapName in map_name2.replace(" ", "")) :
        logger.info("✅ 当前已在指定地图中。")
        if not ((mapName=='白河' or mapName=='铜湖') and fish_count>0):
            relogin()
    else:
        #进菜单
        while not config.stop_event.is_set():
            """
            是否在菜单界面
            """    
            if ocr.recognize_text_from_black_bg_first(region=config.QuitGameButtonRegionScreenshotFly if config.is_fly_ticket else config.QuitGameButtonRegionScreenshot).strip() == "退出":
                break
            """
            是否在游戏界面
            """
            if utils.check_template_in_region(config.FishRegionScreenshot, "fish.png") or navigator.get_current_position():
                logger.info("已在游戏界面。")
                sleep_time(random.uniform(0.23, 0.24))
                utils.press_key('esc')
                sleep_time(random.uniform(0.25, 0.26))
                break
            sleep_time(random.uniform(0.4, 0.5))

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
                break
            sleep_time(random.uniform(0.4, 0.5))

# 拿出物品
def get_item(name):
    #打开物品栏
    if config.stop_event.is_set():
        return
    sleep_time(random.uniform(0.42, 0.52))
    utils.press_key('i')
    # #打开我的最爱
    sleep_time(random.uniform(0.42, 0.52))
    utils.move_mouse_random_in_region((151,426,66,12))
    sleep_time(random.uniform(0.22, 0.32))
    utils.click_left_mouse()
    #输入物品名称（路亚）
    if config.stop_event.is_set():
        return
    sleep_time(random.uniform(0.42, 0.52))
    utils.move_mouse_random_in_region((126,306,202,28))
    if config.stop_event.is_set():
        return
    sleep_time(random.uniform(0.42, 0.52))
    utils.click_left_mouse()
    sleep_time(random.uniform(0.22, 0.32))
    utils.click_left_mouse()
    pyperclip.copy(name)
    if config.stop_event.is_set():
        return
    sleep_time(random.uniform(0.22, 0.32))
    utils.key_down('Left Ctrl')
    sleep_time(random.uniform(0.22, 0.32))
    utils.press_key('v')
    sleep_time(random.uniform(0.22, 0.32))
    utils.key_up('Left Ctrl')    
    sleep_time(random.uniform(1.22, 1.32))
    #拿起第一个物品
    if config.stop_event.is_set():
        return
    utils.move_mouse_random_in_region((451,274,72,72))
    sleep_time(random.uniform(0.22, 0.32))
    utils.click_left_mouse()
    if config.stop_event.is_set():
        return
    sleep_time(random.uniform(0.42, 0.52))
    utils.move_mouse_random_in_region((845, 976, 33, 24))
    sleep_time(random.uniform(0.22, 0.32))
    utils.click_left_mouse()

# 钓鱼函数
def fish_bottom():
    if config.stop_event.is_set():
        return
    logger.info("🎣 开始水底")
    #前往目的地
    sleep_time(random.uniform(1.41, 1.52))
    meters=bottom_next_position()
    baits=[]
    if config.bottom_map==0:
        item=config.laoao_points[config.bottom_last_position_index]
    if config.bottom_map==2:
        item=config.tonghu_points[config.bottom_last_position_index]
        baits=item["baits"]

    #依次拿起竿子1，2，3
    for num in [1, 2, 3]:  # 竿子编号
        if config.stop_event.is_set():
            return
        utils.press_key(num)
        print(f"🎣 已拿起鱼竿 {num}")
        if num==1:
            sleep_time(random.uniform(2.41, 2.52))
        else:
            sleep_time(random.uniform(1.41, 1.52))
        utils.move_mouse_relative_smooth(0, 620, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
        sleep_time(random.uniform(0.41, 0.52))
        #设置收线速度
        adjust_reel_speed(config.bottom_reel_speed)
        sleep_time(random.uniform(0.41, 0.52))
        #设置摩擦力
        if config.bottom_reel_friction>=30:
            adjust_reel_friction(config.bottom_reel_friction-1)
        else:
            adjust_reel_friction(config.bottom_reel_friction)
        sleep_time(random.uniform(0.41, 0.52))
        #设置卡米数
        adjust_reel_meters(meters)
        utils.move_mouse_relative_smooth(0, -620, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
        sleep_time(random.uniform(0.41, 0.52))
        if config.bottom_map==2:
            #设置饵料
            #打开鱼竿配置界面
            if config.stop_event.is_set():
                return
            sleep_time(random.uniform(0.22, 0.32))
            utils.press_key('v', 0.1)
            #移动到可以滚动的地方
            if config.stop_event.is_set():
                return            
            sleep_time(random.uniform(0.81, 0.92))
            utils.move_mouse_random_in_region((1006, 129, 875, 927))
            if config.stop_event.is_set():
                return            
            sleep_time(random.uniform(0.41, 0.52))
            utils.press_key_sc('PageDown')
            sleep_time(random.uniform(0.52, 0.52))
            for i in range(4):
                #点击饵区域
                if config.stop_event.is_set():
                    return                
                sleep_time(random.uniform(0.22, 0.32))
                if i==0: 
                    region=(1001,755,64,44)
                elif i==1:
                    region=(1001,837,64,44)
                elif i==2:
                    region=(1001,919,64,44)
                else:
                    region=(1001,1001,64,44)
                if baits[i]=="":
                    break
                utils.move_mouse_random_in_region(region)
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse()
                if config.stop_event.is_set():
                    return                
                sleep_time(random.uniform(0.22, 0.32))
                utils.move_mouse_random_in_region((324, 104, 222, 23))  # 输入框的位置
                if config.stop_event.is_set():
                    return                
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse()
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse()
                #复制饵料
                pyperclip.copy(baits[i])
                #粘贴饵名称
                if config.stop_event.is_set():
                    return                
                sleep_time(random.uniform(0.22, 0.32))
                utils.key_down('Left Ctrl')
                sleep_time(random.uniform(0.22, 0.32))
                utils.press_key('v')
                sleep_time(random.uniform(0.22, 0.32))
                utils.key_up('Left Ctrl')    
                sleep_time(random.uniform(1.22, 1.32))
                #移动到第一个选择区域
                if config.stop_event.is_set():
                    return
                region = {"left": 859, "top": 606, "width": 190, "height": 23}
                if (utils.check_template_in_region(region,'empty.png',threshold=0.95)):
                    sleep_time(random.uniform(0.22, 0.32))
                    utils.press_key('Esc',0.1)
                    sleep_time(random.uniform(0.22, 0.32))
                    continue

                utils.move_mouse_random_in_region((285, 203, 166, 200))
                if config.stop_event.is_set():
                    return        
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse()
                sleep_time(0.1)
                utils.click_left_mouse()
                sleep_time(random.uniform(0.52, 0.52))

            utils.press_key('v', 0.1)  # 关闭界面
            sleep_time(random.uniform(1.22, 1.32))

        #抛竿子
        t=1.8*(random.uniform(meters*5+5,meters*5+10)/100)
        utils.click_left_mouse(t)

        sleep_time(random.uniform(meters/10*3+0.4, meters/10*3+0.5))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.41, 0.52))
        #放下竿子
        utils.press_key(config.put_down_rod_key)
        sleep_time(random.uniform(2.1, 2.22))
        #向右边挪动两步
        utils.press_key('d',0.1)
        sleep_time(random.uniform(1.8, 1.9))

    utils.press_key('a',0.2)
    sleep_time(random.uniform(0.81, 0.92))

    if not baits or (baits and baits[3]=="") :
        #手抛窝子
        wozi=item["name"]
        if wozi!="":
            get_item(wozi)
            sleep_time(random.uniform(1, 1.1))
            for _ in range(10):
                if config.stop_event.is_set():
                    return
                t=1.8*(random.uniform(meters*5+5,meters*5+10)/100)
                utils.click_left_mouse(t)
                sleep_time(random.uniform(t+1, t+1.1))

    #开始钓鱼    
    bottom(meters)

def fish_lure():
    if config.stop_event.is_set():
        return
    logger.info("开始路亚")
    sleep_time(random.uniform(1.41, 1.52))
    #前往钓鱼点位
    lure_next_position()
    if config.stop_event.is_set():
        return
    #拿出鱼竿
    get_item(config.lure_rod_name)
    sleep_time(random.uniform(2.41, 2.52))
    #视角向下
    utils.move_mouse_relative_smooth(0, 620, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    sleep_time(random.uniform(0.41, 0.52))
    if config.stop_event.is_set():
        return
    #设置收线速度
    adjust_reel_speed(config.lure_reel_speed)
    sleep_time(random.uniform(0.41, 0.52))
    if config.stop_event.is_set():
        return
    #设置摩擦力
    adjust_reel_friction(config.lure_reel_friction)
    sleep_time(random.uniform(0.41, 0.52))
    if config.stop_event.is_set():
        return
    #设置卡米数
    adjust_reel_meters(0)
    utils.move_mouse_relative_smooth(0, -620, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    sleep_time(random.uniform(0.41, 0.52))
    if config.stop_event.is_set():
        return

    #开始路亚钓鱼
    lure()
    
def bottom(meters):
    #补充体力和点锁
    start_daemon_thread(check_player_vitals)
    start_daemon_thread(set_friction_from_slider)
    #抛竿
    def throw_rod():
        if utils.check_template_in_region(config.region_cast_rod,'cast_rod.png'):
            config.is_reeling_line = False
            config.is_space = False
            utils.mouse_up_left()
            utils.key_up('Left Shift')
            utils.mouse_up_right()
            sleep_time(random.uniform(0.41, 0.52))
            # 调整摩擦力
            if config.is_open_lock_unlock:
                adjust_reel_friction(config.bottom_reel_friction)
            #抛竿子
            t=1.8*(random.uniform(meters*5+5,meters*5+10)/100)
            utils.click_left_mouse(t)
            sleep_time(random.uniform(meters/10*3, meters/10*3+0.5))
            utils.click_left_mouse()
            sleep_time(random.uniform(0.41, 0.52))
            utils.press_key(config.put_down_rod_key)
            sleep_time(random.uniform(1.01, 1.12))
            return True
        return False
    #收鱼
    def reel_fish():
        ocr_interval = 1  # 每 0.6 秒识别一次 cast line meters
        last_ocr_time = 0
        max_cast_line_meters_count=0
        cached_cast_line_meters = None
        cached_cast_line_meters_rainbow_time = time.time()
        is_mouse_down_right = False
        config.is_reeling_line = False
        config.is_space=False
        num_count=0
        max_count=2
        while not config.stop_event.is_set():
            now = time.time()

            # 检测入护图像
            cached_keepnet_detected = utils.check_template_in_region(config.region_keepnet, 'keepnet.png')
            if cached_keepnet_detected:
                logger.debug("✅ [提前判断] 入护图像出现，快速切入入护流程")
                return True

            # 限频 OCR 检测
            if now - last_ocr_time >= ocr_interval:
                cached_cast_line_meters = utils.get_cast_line_meters(
                    ocr.recognize_text_from_black_bg(config.region_cast_line_meters, min_confidence=0.7)
                )
                if cached_cast_line_meters is not None and cached_cast_line_meters<=0:
                    num_count+=1
                last_ocr_time = now

            #一进入这个函数就开始收线
            if not config.is_reeling_line:
                if config.bottom_reel_friction>=30:
                    adjust_reel_friction(config.bottom_reel_friction)
                utils.mouse_down_left()
                utils.key_down('Left Shift')
                config.is_reeling_line = True

            #非彩虹线
            if not config.is_rainbow_line:
                if time.time()-cached_cast_line_meters_rainbow_time>2:
                    cached_cast_line_meters=5
                if time.time()-cached_cast_line_meters_rainbow_time>2000:
                    num_count=11

             # 检测咬钩（每帧都检测）
            fish_bite_detected = utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png')    

            # 🎣 咬钩逻辑
            if fish_bite_detected:
                # 已在收线中，继续判断线长，最后0米抬竿子收鱼
                if cached_cast_line_meters is not None:

                    #出线指定米数直接小退
                    if cached_cast_line_meters>config.max_cast_line_meters:
                        max_cast_line_meters_count+=1
                        if max_cast_line_meters_count>30:
                            logger.warning("出线超过指定米数，准备小退")
                            config.need_restart=True
                            return False
                        
                      #抬竿和伸出鱼网收鱼
                    if cached_cast_line_meters <= 5 and not is_mouse_down_right:
                        logger.info("抬竿")
                        utils.mouse_down_right()
                        is_mouse_down_right = True    
                        
                    if not config.is_space and num_count>max_count:
                        logger.info("抄网")
                        utils.press_key('Space')
                        config.is_space = True    

            else:
                #鱼脱钩，把竿子收上来重新抛竿
                if throw_rod():
                    return False
               
            sleep_time(random.uniform(0.03, 0.05))

        utils.mouse_up_left()
        utils.key_up('Left Shift')
        return False
    #把鱼入护
    def handle_fish():
        config.is_reeling_line = False
        utils.mouse_up_left()
        utils.key_up('Left Shift')
        utils.mouse_up_right()
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
            # #切鱼肉
            # if config.is_cut_fish:
            #     #切达标但不值钱的欧鳊
            #     if (fish_name =="欧鳊" or fish_name=='欧蝙'):
            #         if 500 <= weight < 1000:
            #             config.cut_fish_type = 3
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
    #鱼入护后的操作
    def after_handle_fish():
        #重新抛竿子
        while not config.stop_event.is_set():
            if throw_rod():
                #切鱼肉
                cut_fish()
                sleep_time(random.uniform(0.52, 0.65))
                break
            sleep_time(random.uniform(0.04, 0.05))   
    #水底的核心逻辑
    def bottom_core(num):
        """水底钓鱼核心逻辑，支持咬钩累计和鱼跑掉保护"""
        fish_bite_detected = False        

        # 拿起鱼竿
        utils.press_key(num)

        # 等待咬钩的最大时间
        max_bite_wait_time = random.uniform(2.21, 3.53)  
        start_time = time.time()

        while not config.stop_event.is_set() and time.time() - start_time < max_bite_wait_time:
            # 检测鱼是否咬钩
            if utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png'):
                fish_bite_detected = True
                bite_time = time.time()
                break  # 跳出等待阶段
            sleep_time(random.uniform(0.01, 0.02))

        # 如果没咬钩 → 放下竿子
        if not fish_bite_detected:
            # utils.press_key(config.put_down_rod_key)
            return

        # 进入累计阶段，不受 max_bite_wait_time 限制
        required_hold_time = random.uniform(0.51, 0.73)  # 默认 2 秒
        while not config.stop_event.is_set():
            # 每次检查咬钩状态
            bite_still_detected = utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png')
            if not bite_still_detected:
                # 鱼跑掉，放下竿子并退出
                # utils.press_key(config.put_down_rod_key)
                return

            # 计算累计时间
            elapsed = time.time() - bite_time
            if elapsed >= required_hold_time:
                # 已累计到目标时间，执行收鱼
                if reel_fish():
                    handle_fish()
                    after_handle_fish()
                return

            sleep_time(random.uniform(0.01, 0.02))  # 短暂休眠，继续累计

    actions = [1, 2, 3]

    while not config.stop_event.is_set():
        random.shuffle(actions)
        for a in actions:
            if config.stop_event.is_set():
                break
            bottom_core(a)
        if fish_mode_change():
            break
        time.sleep(random.uniform(0.01, 0.02))

def lure():
    #白河打路亚或者老奥打狗
    #补充体力和点锁
    start_daemon_thread(check_player_vitals)
    start_daemon_thread(set_friction_from_slider)
    #抛竿
    def throw_rod():
        if utils.check_template_in_region(config.region_cast_rod,'cast_rod.png'):
            utils.mouse_up_left()
            utils.key_up('Left Shift')
            sleep_time(random.uniform(0.41, 0.52))
            #检测是否需要切换钓鱼方式
            if fish_mode_change():
                return 0
            # 调整摩擦力
            # if config.is_open_lock_unlock:
            #     adjust_reel_friction(config.lure_reel_friction)
            #抛竿
            if config.lure_rod_power<100:
                t=1.8*(random.uniform(config.lure_rod_power,config.lure_rod_power+5)/100)
                utils.click_left_mouse(t)
            else:
                utils.key_down('Left Shift')
                utils.mouse_down_left()
                sleep_time(random.uniform(0.41, 0.52))
                utils.mouse_up_left()
                utils.key_up('Left Shift')
            return 1
        return 2
    #钓鱼
    def reel_fish():
        st=time.time()
        ocr_interval = 1  # 每 0.6 秒识别一次 cast line meters
        last_ocr_time = 0
        max_cast_line_meters_count=0
        cached_cast_line_meters = None
        cached_cast_line_meters_rainbow_time = time.time()
        is_first_time = True
        is_mouse_down_right = False
        config.is_reeling_line = False
        config.is_space=False
        num_count=0
        max_count=10
        is_shift=False  
        is_reeling_line=False
        last_action_time = time.time()
        while not config.stop_event.is_set():
            now = time.time()
        
            # 鱼是不是已经收上来了
            cached_keepnet_detected = utils.check_template_in_region(config.region_keepnet, 'keepnet.png')
            if cached_keepnet_detected:
                return True
          
            # 限频 OCR 检测-识别出线米数
            if now - last_ocr_time >= ocr_interval:
                cached_cast_line_meters = utils.get_cast_line_meters(
                    ocr.recognize_text_from_black_bg(config.region_cast_line_meters, min_confidence=0.7)
                )
                if cached_cast_line_meters is not None and cached_cast_line_meters<=0:
                    num_count+=1
                last_ocr_time = now

            # 有鱼上钩
            fish_bite_detected = utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png')
            if fish_bite_detected:
                #记录第一次进来的时间
                if is_first_time and not config.is_rainbow_line:
                    cached_cast_line_meters_rainbow_time = time.time()
                    is_first_time = False

                if not config.is_reeling_line:
                    #开始匀速收线
                    utils.mouse_up_left()
                    utils.mouse_down_left()
                    config.is_reeling_line = True    

                if not is_shift:    
                    utils.key_down('Left Shift')
                    is_shift=True
           
                #非彩虹线
                if not config.is_rainbow_line:
                    if time.time()-cached_cast_line_meters_rainbow_time>2:
                        cached_cast_line_meters=5
                    if time.time()-cached_cast_line_meters_rainbow_time>2000:
                        num_count=11

                 # 已在收线中，继续判断线长，最后0米抬竿子收鱼
                if cached_cast_line_meters is not None:

                    #出线指定米数直接小退
                    if cached_cast_line_meters>config.max_cast_line_meters:
                        max_cast_line_meters_count+=1
                        if max_cast_line_meters_count>10:
                            logger.warning("出线超过指定米数，准备小退")
                            config.need_restart=True
                            return False
                    
                    #抬竿和伸出鱼网收鱼
                    if cached_cast_line_meters <= 5 and not is_mouse_down_right:
                        logger.info("抬竿")
                        utils.mouse_down_right()
                        is_mouse_down_right = True
                    
                    if not config.is_space and num_count>max_count:
                        logger.info("抄网")
                        utils.press_key('Space')
                        config.is_space = True    
            else:
                num_count=0
                if is_shift:
                    utils.key_up('Left Shift')
                    is_shift=False    
                if is_mouse_down_right:
                    utils.mouse_up_right()
                    is_mouse_down_right = False
                if not is_first_time:
                    is_first_time = True
                if config.is_reeling_line:
                    config.is_reeling_line = False

                #等饵沉底指定时间后收线
                if time.time()-st<config.sink_time:
                    continue
                
                if config.lure_mode==1:
                    if not is_reeling_line:
                        #开始匀速收线
                        utils.mouse_down_left()
                        is_reeling_line = True
                elif config.lure_mode==2:
                    if time.time() - last_action_time >= random.uniform(config.lure_rod_stop_duration, config.lure_rod_stop_duration+0.1):
                        utils.click_left_mouse(random.uniform(config.lure_rod_reeling_duration, config.lure_rod_reeling_duration+0.1))
                        last_action_time = time.time()

            #鱼线收完重新抛竿子
            n=throw_rod()
            if n==1:
                #重置下时间
                st=time.time()
                is_reeling_line=False
            elif n==0:
                break
            
            #延迟
            sleep_time(random.uniform(0.03, 0.05))
        
        utils.mouse_up_left()
        utils.key_up('Left Shift')
        utils.mouse_up_right()
        return False    
    #收鱼
    def handle_fish():
        config.is_reeling_line = False
        config.is_space = False
        utils.mouse_up_left()
        utils.key_up('Left Shift')
        utils.mouse_up_right()
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
        screenshot = dxgi.grab_region(region)
        is_green = utils.check_template_in_region(region, 'green.png', threshold=0.95, screenshot=screenshot)
        is_yellow = utils.check_template_in_region(region, 'yellow.png', threshold=0.95, screenshot=screenshot)
        is_blue = utils.check_template_in_region(region, 'blue.png', threshold=0.95, screenshot=screenshot)
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

    while not config.stop_event.is_set():
        #抛竿
        n=throw_rod()
        if n==2:
            continue
        elif n==0:
            break
        #收线上鱼
        if not reel_fish():
            return
        #把鱼入护
        handle_fish()

