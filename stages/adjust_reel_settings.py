import config
from utils import sleep_time
from ocr_global import ocr
import utils
from logger import logger  # 新增导入

#预先调整收线速度和摩擦力
def adjust_reel_settings(speed=50,friction=29):
    """
    调整收线速度和摩擦力
    """
    # 1.调节收线速度
    adjust_reel_speed(speed)
    # 2.调节摩擦力
    adjust_reel_friction(friction)

#设置收线速度
def adjust_reel_speed(speed=50):
    """
    按住 'R' 键打开收线速度菜单，快速滚动至目标速度值
    speed: 1~50
    """
    sleep_time(0.5)      
    utils.key_down('R')  # 按住R键打开菜单
    sleep_time(0.2)    

    # 读取当前收线速度值（尝试多次提高成功率）
    current_value = None
    for _ in range(20):
        s = ocr.recognize_text_from_black_bg_first(config.region_adjust_reel_settings_area, 0.6,scale=1.0)
        if s and s.isdigit():
            s_int = int(s)
            if 0 < s_int <= 50:
                current_value = int(s)
                break
        sleep_time(0.05)

    if current_value is None:
        logger.warning("⚠️ 无法识别当前收线速度，停止调整")
        utils.key_up('R')
        return

    logger.info(f"当前收线速度: {current_value}, 目标: {speed}")

    diff = speed - current_value
    if diff == 0:
        logger.info("收线速度已是目标值")
        utils.key_up('R')
        return

    scroll_up = diff > 0
    steps = abs(diff)

    for _ in range(steps):
        utils.slow_scroll(up=scroll_up, steps=1)
        # 如果游戏对快速滚动敏感，这里可以加个微小延时
        sleep_time(0.03)

    utils.key_up('R')  # 释放R键
    
#设置摩擦力
def adjust_reel_friction(friction=29):
    if friction>29:
        friction = 29
    # 1. 调出菜单（只滚一次）
    sleep_time(0.5)  
    menu_opened = False
    if not menu_opened:
        utils.slow_scroll(up=False, steps=1)  # 向下滚出菜单
        menu_opened = True

    sleep_time(0.2)        

    # 2. 读取当前摩擦力值
    current_value = None
    for _ in range(20):  # OCR尝试多次提高成功率
        f = ocr.recognize_text_from_black_bg_first(config.region_adjust_reel_settings_area, 0.6,scale=1.0)
        if f and f.isdigit():
            f_int = int(f)
            if 0 < f_int <= 29:
                current_value = int(f)
                break
        sleep_time(0.05)

    if current_value is None:
        logger.warning("⚠️ 无法识别当前摩擦力，停止调整")
        return

    logger.info(f"当前摩擦力值: {current_value}, 目标: {friction}")

    # 3. 计算差距和方向
    diff = friction - current_value
    if diff == 0:
        logger.info("摩擦力已在目标值，无需调整")
        return

    scroll_up = diff > 0
    steps = abs(diff)

    # 4. 快速滚动到目标
    for _ in range(steps):
        utils.slow_scroll(up=scroll_up, steps=1)
        # 可根据情况加短暂延时，防止UI不刷新或过快
        sleep_time(0.03)

#设置卡米数
def adjust_reel_meters(meters=10):
    # 1. 调出菜单（只滚一次）
    sleep_time(0.5)  
    
    utils.key_down('Left Ctrl')  # 按住R键打开菜单
    menu_opened = False
    if not menu_opened:
        utils.press_key('NumPad +')
        menu_opened = True

    sleep_time(0.2)    

    # 2. 读取当前卡米数
    current_value = None
    for _ in range(10):  # OCR尝试多次提高成功率
        f = ocr.recognize_text_from_black_bg_first(config.region_adjust_reel_settings_meters_area, min_confidence=0.2,scale=1.0,is_preprocess=False).replace('.','')
        print(f)
        if f and f.isdigit():
            current_value = int(f)
            break
            
        sleep_time(0.05)

    if current_value is None:
        logger.warning("⚠️ 无法识别当前卡米数，停止调整")
        utils.key_up('Left Ctrl') 
        return

    logger.info(f"当前卡米数: {current_value}, 目标: {meters}")

    # 3. 计算差距和方向
    diff = meters - current_value
    if diff == 0:
        logger.info("卡米数已在目标值，无需调整")
        utils.key_up('Left Ctrl') 
        return

    scroll_up = diff > 0
    steps = abs(diff)

    # 4. 快速滚动到目标
    for _ in range(steps):
        if scroll_up:
            utils.press_key('NumPad +')
        else:
            utils.press_key('NumPad -')
        # 可根据情况加短暂延时，防止UI不刷新或过快
        sleep_time(0.1)

    utils.key_up('Left Ctrl')  # 释放R键    