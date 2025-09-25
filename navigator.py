import random
import pyautogui
import time
import math
import config
from utils import sleep_time
import utils
from ocr_global import ocr
from logger import logger


direction_region = {
    "left": 1776,
    "top": 843,
    "width": 27,
    "height": 15
}

def get_current_position():
    st=time.time()
    while not config.stop_event.is_set() and time.time()-st<3:
        results = ocr.recognize_coordinate_once()
        if results:
            x_coord, y_coord = results
            if x_coord is not None and y_coord is not None:
                if 0 < x_coord < 1000 and 0 < y_coord < 1000:
                    current_position = (x_coord, y_coord)
                    # logger.info(f"识别到当前位置: {current_position}")
                    #更新当前位置
                    config.current_position=current_position
                    return current_position
        sleep_time(random.uniform(0.5, 0.6))
    return None


def check_direction_n():
    try:
        direction = ocr.recognize_text_from_black_bg_first(region=direction_region)
        if direction == 'N':
            logger.debug("检测到N方向")
            return True
        # logger.info("未检测到N方向")
        return False
        
    except Exception as e:
        logger.error(f"方向识别异常: {str(e)}")
        return False

def calculate_angle(current_pos, destination):
    dx = destination[0] - current_pos[0]
    dy = destination[1] - current_pos[1]
    angle_rad = math.atan2(dx, dy)
    angle_deg = math.degrees(angle_rad)
    return abs(angle_deg)  
    
def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def turn_to_north():
    sleep_time(3)
    logger.debug("开始转向北方...")
    
    logger.debug("按住W键2秒...")
    pyautogui.keyDown('w')
    sleep_time(2)
    pyautogui.keyUp('w')
    
    logger.debug("按住a键转向...")
    pyautogui.keyDown('a')
    max_move_time = 90
    start_time = time.time()
    while not config.stop_event.is_set() and time.time() - start_time < max_move_time:
        if check_direction_n():
            logger.debug("已转向北方")
            break
        sleep_time(random.uniform(0.1, 0.2))
    pyautogui.keyUp('a')

    utils.press_key('g', 0.05)
    utils.press_key('g', 0.05)

def turn_to_destination(destination):
    sleep_time(3)
    logger.info("开始转向目的地...")
    
    current_pos = get_current_position()
    if not config.stop_event.is_set() and current_pos:
        dx = destination[0] - current_pos[0]
        angle = calculate_angle(current_pos, destination)

        if dx == 0 and angle == 0:
            logger.debug("目的地在正北方向，无需转向")
            turn_key = None
        elif dx == 0 and angle == 180:
            logger.debug("目的地在正南方向，左转和右转都行...")
            turn_key = 'd'
        elif dx > 0:
            logger.debug("目的地在东边，右转...")
            turn_key = 'd'
        elif dx < 0:
            logger.debug("目的地在西边，左转...")
            turn_key = 'a'
        else:
            turn_key = None

        logger.debug(f"计算的角度: {angle:.2f}度")
        logger.debug(f"转向键: {turn_key}")
        logger.info(f"当前坐标: {current_pos}, 目的地坐标: {destination}")

        turn_time = angle * (10 / 90)
        logger.debug(f"转向时间: {turn_time:.2f}秒")

        if turn_key:
            logger.debug("按住W键2秒...")
            pyautogui.keyDown('w')
            sleep_time(2)
            pyautogui.keyUp('w')

            pyautogui.keyDown(turn_key)
            sleep_time(turn_time)
            pyautogui.keyUp(turn_key)
        else:
            logger.info("无需转向，跳过转向步骤")

        logger.info("按G键熄火...")
        utils.press_key('g', 0.05)
        utils.press_key('g', 0.05)


def move_to_destination(destination):
    sleep_time(3)
    logger.debug("开始前进到目的地...")
    
    logger.debug("按住Shift+W全速前进...")
    pyautogui.keyDown('shift')
    pyautogui.keyDown('w')
    sleep_time(5)
    pyautogui.keyUp('w')
    pyautogui.keyUp('shift')

    max_move_time = 300
    start_time = time.time()
    previous_distance = None
    
    while not config.stop_event.is_set() and time.time() - start_time < max_move_time:
        current_pos = get_current_position()
        if not current_pos:
            continue

        distance = calculate_distance(current_pos, destination)

        if previous_distance is not None:
            if distance < previous_distance:
                logger.info(f"正在接近目的地，当前距离: {distance:.2f}")
            elif distance > previous_distance+0.2:
                logger.warning(f"可能偏离方向，当前距离: {distance:.2f}")
                logger.info("按G键熄火...")
                utils.press_key('g', 0.05)
                utils.press_key('g', 0.05)
                start_navigation(destination)
                break
        else:
            logger.info(f"初始距离: {distance:.2f}")

        previous_distance = distance

        if distance < 12:
            logger.info("已到达目的地附近")
            logger.info("按G键熄火...")
            utils.press_key('g', 0.05)
            utils.press_key('g', 0.05)
            break

        sleep_time(random.uniform(0.5, 0.6))
    else:
        logger.warning("移动超时，未能到达目的地")
        # logger.info("按G键熄火...")
        # utils.press_key('g', 0.05)
        # utils.press_key('g', 0.05)

def start_navigation(destination):
    try:
        if config.stop_event.is_set():
            logger.warning("导航已被外部中断，取消执行。")
            return
        logger.info("前往目的地")

        #获取当前位置
        st=time.time()
        while not config.stop_event.is_set() and time.time()-st<120:
            current_pos = get_current_position()
            if current_pos:
                break
            sleep_time(random.uniform(0.5, 0.6))

        if current_pos:
            distance = calculate_distance(current_pos, destination)
            logger.info(f"当前距离目的地: {distance:.2f}")
            if distance < 12:
                logger.info("已经在目的地了，无需导航。")
                return
        else:
            logger.warning("无法获取当前位置，取消导航。")
            return

        if not config.stop_event.is_set():
            logger.info("步骤1：转向北方")
            turn_to_north()

        if not config.stop_event.is_set():
            logger.info("步骤2：朝向目的地")
            turn_to_destination(destination)

        if not config.stop_event.is_set():
            logger.info("步骤3：移动到目的地")
            move_to_destination(destination)

        logger.info("✅ 导航流程完成")

    except Exception as e:
        logger.error(f"❌ 导航过程中发生异常: {str(e)}")

    finally:
        for key in ['w', 'a', 'd', 'shift']:
            pyautogui.keyUp(key)
        logger.info("所有按键已释放")

def go_destination():

    start_navigation(config.destination)
