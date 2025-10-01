from collections import deque
import random
import time
from stages.check_assembly import check_assembly
from utils import sleep_time, start_daemon_thread
from ocr_global import ocr
import pyperclip
import config
from stages.adjust_reel_settings import adjust_reel_friction, adjust_reel_settings,adjust_reel_speed
from stages.check_fishnet_status import check_fishnet_status
from stages.check_player_vitals import check_player_vitals
from stages.cut_fish import cut_fish
from stages.move_to_bow import move_to_bow
from stages.return_destination import return_destination
from stages.set_friction_from_slider import set_friction_from_slider
import utils
from logger import logger  # 确保你的 logger 已 setup
import re

#打状态
def get_fish_status():
    """
    渔杆打状态（优化版）
    """

    last_values = deque(maxlen=10)

    status_type = config.status_type
    is_locked = False

    # 每类状态行为配置
    status_action_map = {
        1: {"sleep": (1, 1.1), "click": (0.3, 0.31)},
        2: {"sleep": (1.2, 1.3), "click": (0.7, 0.8)},
        3: {"sleep": (1.5, 1.8), "click": (0.8, 1.0)},
        4: [  # 多个方案
            {"sleep": (1, 1.1), "click": (0.3, 0.31)},
            {"sleep": (1.2, 1.3), "click": (0.7, 0.8)},
            {"sleep": (1.5, 1.8), "click": (0.8, 1.0)},
            ],
        5:{"sleep": (0, 1), "click": (0, 1)},
        6:{"sleep": (config.status_sleep, config.status_sleep+0.1), "click": (config.status_click, config.status_click+0.01)}    
    }

    # if status_type == 4:
    #     action = random.choice(status_action_map[4])
    # else:
    #     action = status_action_map.get(status_type)


    # 检测频率控制
    last_ocr_time = 0
    ocr_interval = 1
    cast_line_meters = None
    hook_detected = False
    fish_bite_detected=False
    hook_start_time = None
    stop_value=0
    #第一次沉底后收线时间
    is_status_detected_first=True
    while not config.stop_event.is_set():
        now = time.time()

        # 🐟 检查鱼咬钩
        fish_bite_detected = utils.check_template_in_region(
            config.region_fish_bite, 'fish_bite.png'
        )
        if fish_bite_detected:
            return True

        # 🐟 入护检测
        if utils.check_template_in_region(config.region_keepnet, 'keepnet.png'):
            return True
        
         # 🎯 hook 状态图标检测
        hook_detected = utils.check_template_in_region(
            config.region_hook_status, 'hook_status.png',0.7
        )

        # 🎯 OCR 限速（读取出线米数）
        if now - last_ocr_time > ocr_interval:
            try:
                text = ocr.recognize_text_from_black_bg(
                    config.region_cast_line_meters, min_confidence=0.7
                )
                cast_line_meters = utils.get_cast_line_meters(text)
                if cast_line_meters:
                    last_values.append(cast_line_meters)
                last_ocr_time = now
            except Exception as e:
                cast_line_meters = None

        # === 非卡米逻辑（图标触发） ===
        if hook_detected:

            # if not is_locked:
            if hook_start_time is None:
                hook_start_time = now  # 第一次检测到图标
                continue
            if now - hook_start_time < config.sleep_when_on_status:
                continue
            hook_start_time = None  # 重置时间戳

            logger.info("开始打状态")
            
            utils.renew_ticket_blocking()
            config.is_important_action=True
            utils.mouse_up_left()
            config.is_important_action=False
            if not is_locked:
                utils.click_left_mouse()  # 锁轮

            #第一次沉底后收线时间
            if config.reeling_time_after_status_detected>0 and is_status_detected_first:
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse(config.reeling_time_after_status_detected)
                is_status_detected_first=False

            is_locked = True
            hook_not_detected_count = 0
            max_not_detected = 30
            while not config.stop_event.is_set():
                
                # 检测状态图标
                hook_found = utils.check_template_in_region(
                    config.region_hook_status, 'hook_status.png',0.7
                )
                if hook_found:
                    hook_not_detected_count = 0
                    if config.status_type!=5:
                        if status_type == 4:
                            action = random.choice(status_action_map[4])
                        else:
                            action = status_action_map.get(status_type)
                        if action:
                            if config.is_shift:
                                sleep_time(random.uniform(*action["sleep"]))
                                utils.key_down('Left Shift')
                                utils.click_right_mouse(random.uniform(*action["click"]))
                                utils.key_up('Left Shift')
                            else:
                                sleep_time(random.uniform(*action["sleep"]))
                                utils.click_right_mouse(random.uniform(*action["click"]))
                else:
                    # 检测鱼咬钩
                    fish_bite = utils.check_template_in_region(
                    config.region_fish_bite, 'fish_bite.png'
                    )
                    if fish_bite:
                        return True
                    hook_not_detected_count += 1
                    if is_locked and hook_not_detected_count >= max_not_detected :
                        utils.press_key('Enter')
                        is_locked = False
                        logger.info("放线出状态")
                        break

                sleep_time(random.uniform(0.01, 0.02))   # 内层打状态的检测频率

        # === 卡米逻辑（米数稳定） ===
        elif cast_line_meters is not None and config.cast_line_meters != 0 and cast_line_meters >= config.cast_line_meters:
            logger.info("开始打状态（卡米）")
            utils.click_left_mouse()

            is_mouse_down_left=False
            #如果是拖掉打电梯，调整收线速度
            if config.trolling_status_type==2 and config.is_trolling_mode:
                adjust_reel_speed(config.trolling_reeling_speed)

            last_ocr_time1 = 0
            ocr_interval1 = 1
            cast_line_meters1 = None

            while not config.stop_event.is_set():
                
                now1 = time.time()

                # 🎯 OCR 限速（读取出线米数）
                if now1 - last_ocr_time1 > ocr_interval1:
                    try:
                        text = ocr.recognize_text_from_black_bg(
                            config.region_cast_line_meters, min_confidence=0.7
                        )
                        cast_line_meters1 = utils.get_cast_line_meters(text)
                        last_ocr_time1 = now1
                    except Exception as e:
                        cast_line_meters1 = None

                if config.is_trolling_mode and cast_line_meters1 and  cast_line_meters1<=config.trolling_unlock_meters and config.trolling_status_type==2:
                    utils.mouse_up_left()
                    adjust_reel_speed(50)
                    utils.press_key('Enter')
                    break

                if config.trolling_status_type==2 and config.is_trolling_mode and not is_mouse_down_left:
                    utils.mouse_down_left()
                    is_mouse_down_left=True

                fish_bite = utils.check_template_in_region(
                    config.region_fish_bite, 'fish_bite.png'
                )
                if fish_bite:
                    utils.mouse_up_left()
                    return True
                
                if config.status_type!=5:
                    if status_type == 4:
                        action = random.choice(status_action_map[4])
                    else:
                        action = status_action_map.get(status_type)
                    if action:
                        if config.is_shift:
                            sleep_time(random.uniform(*action["sleep"]))
                            utils.key_down('Left Shift')
                            utils.click_right_mouse(random.uniform(*action["click"]))
                            utils.key_up('Left Shift')
                        else:
                            sleep_time(random.uniform(*action["sleep"]))
                            utils.click_right_mouse(random.uniform(*action["click"]))

                sleep_time(random.uniform(0.01, 0.02))
            
        # === 无状态长时间无动作，判断收线或放线 ===
        elif cast_line_meters is not None:
            hook_start_time = None  # 图标中断了，重置计时
            # 检测鱼咬钩
            fish_bite = utils.check_template_in_region(
            config.region_fish_bite, 'fish_bite.png'
            )
            if fish_bite:
                return True
            #长时间无状态，开始收线
            if len(last_values) >=10:
                if all(x == last_values[0] for x in last_values):
                    logger.warning(f"⚠️ 米数静止：{list(last_values)}")
                    stop_value=last_values[0]
                    logger.info("⏪ 收线等待状态")
                    utils.renew_ticket_blocking()
                    config.is_important_action=True
                    utils.mouse_down_left()
                    config.is_important_action=False
                    is_locked = True
                last_values.clear()
            #收线过多，开始放线
            if stop_value!=0 and cast_line_meters<=stop_value-10:
                if is_locked:
                    logger.info("⏩ 收线过多，开始放线")
                    utils.renew_ticket_blocking()
                    config.is_important_action=True
                    utils.mouse_up_left()
                    utils.press_key('Enter')
                    config.is_important_action=False
                    is_locked = False
                    stop_value=0

        sleep_time(0.05)  # 主循环节流

    return False

#收线
def reel_in_fish():
    """
    鱼上钩收线逻辑（限频识别 + 降低 CPU 占用）
    """
    hook_not_detected_count = 0
    max_not_detected_threshold = 30
    last_values = deque(maxlen=10)
    is_mouse_down_right = False
    is_press_right_off= False
    ocr_interval = 1  # 每 0.6 秒识别一次 cast line meters
    last_ocr_time = 0
    cached_cast_line_meters = None
    cached_keepnet_detected = False
    press_right_count=0
    max_cast_line_meters_count=0
    #电轮自动切换收线方式
    speed=0
    zero_speed_threshold = 12
    high_speed_threshold = 30
    switch_threshold_count = 5
    # 状态变量
    current_mode = "electric"  # manual or electric
    zero_speed_count = 0
    high_speed_count = 0
    is_release=False
    current_mode_gear_ratio="fast"
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
            #电轮收线速度
            if config.reel_type == 3:
                text = ocr.recognize_text_from_black_bg(config.region_electric_reel_speed, min_confidence=0.7)
                if text and len(text) == 1:
                    s = text[0].strip()
                    match = re.search(r'^-?\d+(?:\.\d+)?$', s)  # 只匹配纯数字或浮点数，如 8、12.5、-3.2
                    if match:
                        speed = float(s)
                if speed < zero_speed_threshold:
                    zero_speed_count += 1
                    high_speed_count = 0
                elif speed > high_speed_threshold:
                    high_speed_count += 1
                    zero_speed_count = 0
                else:
                    zero_speed_count = 0
                    high_speed_count = 0
            #出线米数            
            if cached_cast_line_meters is not None:
                last_values.append(cached_cast_line_meters)
            last_ocr_time = now

        # 检测咬钩（每帧都检测）
        fish_bite_detected = utils.check_template_in_region(config.region_fish_bite, 'fish_bite.png')

        # 🎣 咬钩逻辑
        if fish_bite_detected:
            hook_not_detected_count = 0  # 清零未检测计数

            if not config.is_reeling_line:
                logger.info("🎣 开始收线")
                if config.reel_type ==  3:
                    utils.click_left_mouse()
                    sleep_time(0.1)
                    utils.click_left_mouse()
                    current_mode = "electric"
                else:
                    utils.mouse_down_left()
                    utils.key_down('Left Shift')
                config.is_reeling_line = True    

            else:

                # if config.tension_value>0.7:
                #     #满红停止收线
                #     if not is_release:
                #         utils.key_up('Left Shift')
                #         utils.mouse_up_left()
                #         is_release = True
                # else:
                #     # 开始收线
                #     if is_release:
                #         utils.key_down('Left Shift')
                #         utils.mouse_down_left()
                #         is_release = False

                # 已在收线中，继续判断线长
                if cached_cast_line_meters is not None:

                    #电轮切换收线方式
                    if config.reel_type == 3 and cached_cast_line_meters>=10:

                        # 切换到手动收线
                        if zero_speed_count >= switch_threshold_count and current_mode != "manual":
                            utils.key_down('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))
                            utils.press_key('Space')
                            utils.key_up('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))

                            current_mode = "manual"
                            utils.mouse_down_left()
                            utils.key_down('Left Shift')
                            logger.info("✅ 切换为手动收线")

                        # 切换到电动收线（前先释放原有按键）
                        elif high_speed_count >= switch_threshold_count and current_mode != "electric":
                            # 释放原有按键
                            utils.mouse_up_left()
                            utils.key_up('Left Shift')

                            utils.key_down('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))
                            utils.press_key('Space')
                            utils.key_up('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))

                            current_mode = "electric"
                            utils.click_left_mouse()
                            time.sleep(0.1)
                            utils.click_left_mouse()
                            logger.info("⚡️ 切换为电动收线")    

                    #鼓轮切换传动比
                    if config.reel_type==2 and cached_cast_line_meters>=10 and config.is_open_gear_ratio:     
                        if config.tension_value<=config.gear_ratio and current_mode_gear_ratio!="fast":
                            utils.key_down('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))
                            utils.press_key('Space')
                            utils.key_up('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))
                            current_mode_gear_ratio="fast"
                        elif config.tension_value>config.gear_ratio and current_mode_gear_ratio!="slow":
                            utils.key_down('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))
                            utils.press_key('Space')
                            utils.key_up('Left Ctrl')
                            time.sleep(random.uniform(0.25, 0.35))
                            current_mode_gear_ratio="slow"


                    #出线指定米数直接小退
                    if cached_cast_line_meters>config.max_cast_line_meters:
                        max_cast_line_meters_count+=1
                        if max_cast_line_meters_count>4:
                            logger.warning("出线超过指定米数，准备小退")
                            adjust_reel_friction(28)
                            config.need_restart=True
                            return False
                    
                    #力度条过大取消抬竿收鱼
                    if config.tension_value>0.75:
                        is_press_right_off=True

                    # 非电轮子抬竿收线
                    press_right_count+=1
                    if config.reel_type == 1 and press_right_count>25 and 0<config.tension_value<0.4 and not is_mouse_down_right and not is_press_right_off:
                       utils.click_right_mouse(random.uniform(1.4, 1.5))
                       press_right_count=0

                    #抬竿子的操作
                    m= 0  if config.reel_type == 3 and current_mode == "electric" else 5
                    if cached_cast_line_meters <= m and not is_mouse_down_right:
                        utils.mouse_down_right()
                        is_mouse_down_right = True
                          
                    # 大鱼伸出抄网
                    if len(last_values) >= 10 and all(x == last_values[0] for x in last_values):
                        if cached_cast_line_meters ==0:
                            logger.warning(f"⚠️ 收线疑似中断，值: {last_values[0]} 米")
                            if not config.is_space:
                                utils.press_key('Space')
                                config.is_space = True
                        #如果伸出了抄网，并且不是0米
                        else:
                            if config.is_space:
                                utils.press_key('Space')
                                config.is_space = False


        # ❌ （脱钩）
        else:
            hook_not_detected_count += 1
            if hook_not_detected_count >= max_not_detected_threshold:
                logger.info("🐟 鱼疑似脱钩，重置状态")

                utils.mouse_up_left()
                utils.key_up('Left Shift')
                utils.mouse_up_right()

                if cached_cast_line_meters==0:
                    utils.click_left_mouse(0.05)
                else:
                    utils.press_key('Enter')

                if utils.check_template_in_region(config.region_cast_rod,'cast_rod.png'):
                   utils.click_left_mouse(0.05)

                # 重置状态
                is_mouse_down_right = False
                config.is_reeling_line = False
                hook_not_detected_count = 0
                last_values.clear()

                if config.is_space:
                    utils.press_key('Space')
                    config.is_space = False

                # 重回打状态
                if get_fish_status():
                    logger.info("🎣 又有鱼上钩了")
                    continue
                else:
                    logger.info("🐟 鱼已跑，退出当前流程")
                    return False

        # 动态 sleep：咬钩时快点，平常慢点
        sleep_time(random.uniform(0.0485, 0.05))

    return False

#鱼入护
def process_fish_and_decide():
    """
    获取鱼的信息，并决定是否入护
    """
    # utils.renew_ticket_blocking()
    config.is_important_action = True
    st_total = time.time()

    logger.info("🔄 开始入护流程")

    utils.mouse_up_left()
    utils.key_up('Left Shift')
    utils.mouse_up_right()
    config.is_reeling_line = False

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

        def should_keep_fish_by_rule(name: str, w: float):
            rules = {
                '大西洋鯖': lambda x: x >= 300,
                '大西洋鲭': lambda x: x >= 300,
                '大西洋': lambda x: x >= 300,
                '黑线鳕': lambda x: x >= 1500,
                '短角大杜父鱼': lambda x: x >= 600,
            }
            return rules.get(name, lambda x: True)(w)

        if is_green:
            logger.info("✅ 检测到达标鱼")
            should_keep = True
            # if not should_keep_fish_by_rule(fish_name, weight):
            #     should_keep = False
            #     logger.info(f"{fish_name} 不符合最小重量要求，被扔掉")
            if  config.is_cut_fish:
                if (fish_name =="大西洋鲭" or fish_name =="大西洋鯖" or fish_name =="大西洋"):
                    t = config.fish_block_types2
                    w = weight
                    if t == 1 and 300 <= w < 400:
                        config.cut_fish_type = 2
                    elif t == 2 and 300 <= w < 400:
                        config.cut_fish_type = 2
                    elif t == 3:
                        if w >= 600:
                            config.cut_fish_type = 2
                    elif t == 4:
                        if w >= 800 and w < 1500:
                            config.cut_fish_type = 2
                if fish_name == '绿青鳕' and weight < 3000 and config.is_cut_low_quality_fish:
                    config.cut_fish_type = 1
                    logger.info("🎯 绿青鳕不超过3kg，有鱼可以切")

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
            if  config.is_cut_fish:
                if fish_name == '绿青鳕':
                    t = config.fish_block_types1
                    w = weight
                    if t == 1 and w >= 300:
                        config.cut_fish_type = 1
                        config.current_fish_block_types1 = 1
                        should_keep = True
                    elif t == 2 and w >= 300:
                        config.cut_fish_type = 1
                        config.current_fish_block_types1 = 2
                        should_keep = True
                    elif t == 3:
                        if w >= 600:
                            config.cut_fish_type = 1
                            config.current_fish_block_types1 = 3
                            should_keep = True
                        elif w >= 300:
                            config.cut_fish_type = 1
                            config.current_fish_block_types1 = 2
                            should_keep = True
                    elif t == 4:
                        if w >= 800 and w<1500:
                            config.cut_fish_type = 1
                            config.current_fish_block_types1 = 4
                            should_keep = True
                        elif w >= 600:
                            config.cut_fish_type = 1
                            config.current_fish_block_types1 = 3
                            should_keep = True
                        elif w >= 300:
                            config.cut_fish_type = 1
                            config.current_fish_block_types1 = 2
                            should_keep = True

        logger.debug(f"⏱️ 鱼类判断耗时: {time.time() - t_judge:.3f} 秒")

        # === 执行键盘指令阶段 ===
        t_press = time.time()
        if should_keep:
            logger.info(">> 入护 ✅")
            utils.press_key('Space')
        else:
            logger.info(">> 扔掉 ❌")
            utils.press_key('Backspace')
        logger.debug(f"⏱️ 按键执行耗时: {time.time() - t_press:.3f} 秒")

    except Exception as e:
        logger.error(f"❗ 识别或判断出错: {e}")

    config.is_important_action = False
    logger.debug(f"✅ 总耗时: {time.time() - st_total:.3f} 秒")

#更换拟饵
def check_and_replace_damaged_bait():
    """
    判断拟饵是否损坏并自动更换（处理前两页所有损坏拟饵）
    """
    while not config.stop_event.is_set():

        check_assembly(on_sea=True)

        if utils.check_template_in_region(region=config.region_damaged_lure, template_path="damagedlure.png"):
            #续费船票的时候阻塞
            utils.renew_ticket_blocking()
            #防止被自动续费船票的操作打断操作
            config.is_important_action=True
            #打开鱼竿配置界面
            sleep_time(random.uniform(0.22, 0.32))
            utils.press_key('v', 0.1)
            #移动到可以滚动的地方
            sleep_time(random.uniform(0.22, 0.32))
            utils.move_mouse_random_in_region((1006, 129, 875, 927))

            #更换引线
            ratio = utils.analyze_tension_color_percentage(config.region_leader_line_damage_bar)
            if ratio:
                green = ratio['green']
                yellow = ratio['yellow']
                red = ratio['red']
            tension_value = max(green, yellow, red)
            logger.info(f"引线损坏值:{1 - tension_value:.3f}")
            if tension_value<1-config.change_leader_line_max_value and tension_value!=0:
                logger.info(f"引线损耗超过{config.change_leader_line_max_value*100}%,更换引线.")
                #获取引线名称
                leader_line_name = ocr.recognize_text_from_black_bg(region=config.region_leader_line_name,fill_black=True,is_preprocess=True)
                if leader_line_name:
                    # 拼接数组为完整字符串
                    leader_line_name = ' '.join(leader_line_name).strip()
                    # 提取“公斤”前的整数或小数
                    match = re.search(r'(\d+(?:\.\d+)?)\s*公斤', leader_line_name)
                    if match:
                        num_str = match.group(1)
                        weight = float(num_str)
                        leader_line_name = int(weight) if weight.is_integer() else weight
                                    
                pyperclip.copy(leader_line_name)
                #进入更换引线的界面
                sleep_time(random.uniform(0.22, 0.32))
                utils.move_mouse_random_in_region(config.region_leader_line_damage_bar)
                utils.click_left_mouse()
                #输入引线名称
                sleep_time(random.uniform(0.22, 0.32))
                utils.move_mouse_random_in_region((324, 104, 222, 23))  # 输入框的位置
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse()
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse()
                #粘贴损坏的损坏引线的名称
                sleep_time(random.uniform(0.22, 0.32))
                utils.key_down('Left Ctrl')
                sleep_time(random.uniform(0.22, 0.32))
                utils.press_key('v')
                sleep_time(random.uniform(0.22, 0.32))
                utils.key_up('Left Ctrl')    
                sleep_time(random.uniform(1.22, 1.32))
                #如果为空
                region = {"left": 859, "top": 606, "width": 190, "height": 23}
                if (utils.check_template_in_region(region,'empty.png',threshold=0.95)):
                    # utils.move_mouse_random_in_region((285, 203, 166, 200))
                    # sleep_time(random.uniform(0.22, 0.32))
                    # utils.click_left_mouse()
                    sleep_time(random.uniform(0.22, 0.32))
                    utils.press_key('Esc',0.1)
                    sleep_time(random.uniform(0.22, 0.32))
                    utils.press_key('Esc',0.1)
                    continue

                #移动到第一个选择区域
                sleep_time(random.uniform(0.22, 0.32))
                utils.move_mouse_random_in_region((285, 203, 166, 200))
                #双击
                sleep_time(random.uniform(0.22, 0.32))
                utils.click_left_mouse()
                sleep_time(0.1)
                utils.click_left_mouse()
                sleep_time(random.uniform(0.22, 0.32))
            

            #在指定区域找到损坏的拟饵，最多两处
            damaged_regions = utils.find_template_in_regions(config.region_check_damaged_bait_area, 'damaged.png', confidence=0.95)
            if len(damaged_regions) > 0:
                logger.info(f"检测到{len(damaged_regions)}处损坏的拟饵。")
                for i, r in enumerate(damaged_regions):
                    logger.debug(f"匹配{i + 1}: {r}")

                    #计算损坏的拟饵名称区域         
                    region = {"left": 1073, "top": r["top"] - 39, "width": 700, "height": 39}

                    #识别损坏的拟饵名称
                    sleep_time(random.uniform(0.22, 0.32))
                    damaged_bait_name = ocr.recognize_text_from_black_bg(region=region, fill_black=True, is_preprocess=True)

                    if len(damaged_bait_name) > 0:
                        damaged_bait_name = ' '.join([item for item in damaged_bait_name]).strip()       
                        
                        #吸引成分特殊处理                       
                        texts = ['BLU', 'RED', 'FLU', 'GRN', 'ORN', 'ROS', 'WHT', 'YEL']
                        for text in texts:
                            if text in damaged_bait_name and "WTA Fire Tubes" in damaged_bait_name:
                                damaged_bait_name = text
                                break
                        
                        if 'Handmade' in damaged_bait_name:
                            damaged_bait_name=damaged_bait_name.replace("Handmade", "Handmade ")
                            
                        logger.info(f"损坏的拟饵名称: {damaged_bait_name}")
                        pyperclip.copy(damaged_bait_name)  # 将损坏的拟饵名称复制到剪贴板

                        #更换拟饵
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.move_mouse_random_in_region((region["left"], region["top"], 100, region["height"]))
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.move_mouse_random_in_region((324, 104, 222, 23))  # 输入框的位置
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()

                        #粘贴损坏的拟饵名称
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.key_down('Left Ctrl')
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.press_key('v')
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.key_up('Left Ctrl')    
                        sleep_time(random.uniform(1.22, 1.32))
                        
                        region = {"left": 859, "top": 606, "width": 190, "height": 23}
                        if (utils.check_template_in_region(region,'empty.png',threshold=0.95)):
                            # utils.move_mouse_random_in_region((285, 203, 166, 200))
                            # sleep_time(random.uniform(0.22, 0.32))
                            # utils.click_left_mouse()
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.press_key('Esc',0.1)
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.press_key('Esc',0.1)
                            continue

                        #移动到选择区域
                        if damaged_bait_name == "RED":
                            cout = 0
                            max_attempts = 10  # 最大尝试次数
                            damaged_regions_red=[]
                            while not config.stop_event.is_set() and cout < max_attempts:
                                cout += 1
                                damaged_regions_red = utils.find_template_in_regions(
                                    config.region_check_damaged_bait_area_red, 'redtubes.png', confidence=0.95)
                                if len(damaged_regions_red) > 0:
                                    drr = damaged_regions_red[0]
                                    utils.move_mouse_random_in_region((drr["left"], drr["top"], drr["width"], drr["height"]))
                                    break
                                else:
                                    sleep_time(random.uniform(0.22, 0.32))
                                    utils.press_key_sc('PageDown')  # 向下滚动换页
                                    sleep_time(random.uniform(0.22, 0.32))
                            #没找到合适的饵
                            if len(damaged_regions_red) == 0:
                                sleep_time(random.uniform(0.22, 0.32))
                                utils.press_key('Esc',0.1)
                                # sleep_time(random.uniform(0.22, 0.32))
                                # utils.press_key('Esc',0.1)     
                                # continue

                        elif 'Handmade' in damaged_bait_name:
                            cout = 0
                            max_attempts = 10  # 最大尝试次数
                            damaged_regions_rubber=[]
                            while not config.stop_event.is_set() and cout < max_attempts:
                                cout += 1
                                damaged_regions_rubber = utils.find_template_in_regions(
                                    config.region_check_damaged_bait_area_red, 'rubber.png', confidence=0.95)
                                if len(damaged_regions_rubber) > 0:
                                    drr = damaged_regions_rubber[-1]
                                    utils.move_mouse_random_in_region((drr["left"], drr["top"], drr["width"], drr["height"]))
                                    break
                                else:
                                    sleep_time(random.uniform(0.22, 0.32))
                                    utils.press_key_sc('PageDown') # 向下滚动换页
                                    sleep_time(random.uniform(0.22, 0.32))
                            #没找到合适的饵
                            if len(damaged_regions_rubber) == 0:
                                sleep_time(random.uniform(0.22, 0.32))
                                utils.press_key('Esc',0.1)
                                # sleep_time(random.uniform(0.22, 0.32))
                                # utils.press_key('Esc',0.1)
                                # continue

                        else:
                            #移动到第一个选择区域
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.move_mouse_random_in_region((285, 203, 166, 200))
                        
                        #双击
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.click_left_mouse()
                        sleep_time(0.1)
                        utils.click_left_mouse()
                    else:
                        logger.warning("未识别到损坏的拟饵名称")
                        sleep_time(random.uniform(0.22, 0.32))
                        utils.press_key('Esc',0.1)  
                        continue

            # ------------------ 翻页 ------------------
            for i in range(2):
                #移动到可以滚动的地方
                sleep_time(random.uniform(0.22, 0.32))
                utils.move_mouse_random_in_region((1006, 129, 875, 927))  # 假设这是可以滚动的区域

                #向下翻页
                sleep_time(random.uniform(0.22, 0.32))
                utils.press_key_sc('PageDown')
                if i==0:
                    sleep_time(random.uniform(0.22, 0.32))
                    utils.press_key_sc('PageDown')
                else:    
                    sleep_time(random.uniform(0.22, 0.32))
                sleep_time(random.uniform(0.52, 0.52))

                #在第二页找到损坏的拟饵
                damaged_regions_second = utils.find_template_in_regions(config.region_check_damaged_bait_area, 'damaged.png', confidence=0.95)
                if len(damaged_regions_second) > 0:
                    logger.info(f"检测到第二页有{len(damaged_regions_second)}处损坏的拟饵。")
                    for i, r in enumerate(damaged_regions_second):
                        logger.debug(f"匹配{i + 1}: {r}")

                        #计算损坏的拟饵名称区域         
                        region = {"left": 1073, "top": r["top"] - 39, "width": 700, "height": 39}

                        #识别损坏的拟饵名称
                        sleep_time(random.uniform(0.22, 0.32))
                        damaged_bait_name_second = ocr.recognize_text_from_black_bg(region=region, fill_black=True, is_preprocess=True)
                        if len(damaged_bait_name_second) > 0:
                            damaged_bait_name_second = ' '.join([item for item in damaged_bait_name_second]).strip()

                            #海洋珠特殊处理
                            texts = ['BLK', 'BLU', 'RED', 'FLU', 'GRN', 'ORN', 'ROS', 'WHT', 'YEL']
                            for text in texts:
                                if text in damaged_bait_name_second and "WTA Color beads" in damaged_bait_name_second:
                                    damaged_bait_name_second = text
                                    break
                            
                            #泡沫特殊处理         
                            if 'Handmade' in damaged_bait_name_second:
                                damaged_bait_name_second=damaged_bait_name_second.replace("Handmade", "Handmade ")
                                # #获取随机胶鱼橡饵
                                # prefix = "Handmade 泡沫橡胶鱼"
                                # model_number = random.randint(1, 5)
                                # model_str = f"{model_number:03d}" 
                                # damaged_bait_name_second=prefix + model_str
                                
                            logger.info(f"损坏的拟饵名称: {damaged_bait_name_second}")
                            pyperclip.copy(damaged_bait_name_second)  # 将损坏的拟饵名称复制到剪贴板    

                            #更换拟饵
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.move_mouse_random_in_region((region["left"], region["top"], 100, region["height"]))
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.move_mouse_random_in_region((324, 104, 222, 23))  # 输入框的位置
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()
                            
                            #粘贴损坏的拟饵名称
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.key_down('Left Ctrl')
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.press_key('v')
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.key_up('Left Ctrl')    
                            sleep_time(random.uniform(1.22, 1.32))

                            region = {"left": 859, "top": 606, "width": 190, "height": 23}
                            if (utils.check_template_in_region(region,'empty.png',threshold=0.95)):
                                # utils.move_mouse_random_in_region((285, 203, 166, 200))
                                # sleep_time(random.uniform(0.22, 0.32))
                                # utils.click_left_mouse()
                                sleep_time(random.uniform(0.22, 0.32))
                                utils.press_key('Esc',0.1)
                                sleep_time(random.uniform(0.22, 0.32))
                                utils.press_key('Esc',0.1)
                                continue

                            #移动到选择区域,泡沫饵修复
                            if 'Handmade' in damaged_bait_name_second:
                                cout = 0
                                max_attempts = 10  # 最大尝试次数
                                damaged_regions_rubber=[]
                                while not config.stop_event.is_set() and cout < max_attempts:
                                    cout += 1
                                    damaged_regions_rubber = utils.find_template_in_regions(
                                        config.region_check_damaged_bait_area_red, 'rubber.png', confidence=0.95)
                                    if len(damaged_regions_rubber) > 0:
                                        drr = damaged_regions_rubber[-1]
                                        utils.move_mouse_random_in_region((drr["left"], drr["top"], drr["width"], drr["height"]))
                                        break
                                    else:
                                        sleep_time(random.uniform(0.22, 0.32))
                                        utils.press_key_sc('PageDown') # 向下滚动换页
                                        sleep_time(random.uniform(0.22, 0.32))
                                #没找到合适的饵
                                if len(damaged_regions_rubber) == 0:
                                    sleep_time(random.uniform(0.22, 0.32))
                                    utils.press_key('Esc',0.1)
                                    # sleep_time(random.uniform(0.22, 0.32))
                                    # utils.press_key('Esc',0.1)
                                    # continue
                            else:
                                #移动到第一个选择区域
                                sleep_time(random.uniform(0.22, 0.32))
                                utils.move_mouse_random_in_region((285, 203, 166, 200))

                            #双击
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.click_left_mouse()
                            sleep_time(0.1)
                            utils.click_left_mouse()
                        else:
                            logger.warning("未识别到损坏的拟饵名称")
                            sleep_time(random.uniform(0.22, 0.32))
                            utils.press_key('v', 0.1)  # 关闭界面
                            continue

            sleep_time(random.uniform(0.22, 0.32))
            utils.press_key('v', 0.1)  # 关闭界面
            
            sleep_time(random.uniform(1.52, 1.62))
            #重新抛竿,修补错误
            if config.is_cast_rod and utils.check_template_in_region(config.region_cast_rod,'cast_rod.png'):
                utils.click_left_mouse(random.uniform(0.08, 0.11))
            #防止被自动续费船票的操作打断操作
            config.is_important_action=False
        sleep_time(random.uniform(2, 2.1))

#拖钓模式
def trolling_fish():
    #阻塞行为
    utils.renew_ticket_blocking()
    #防止被自动续费船票的操作打断操作
    config.is_important_action=True
    sleep_time(random.uniform(1.52, 1.62))
    #开启拖钓
    utils.press_key('j')
    
    if config.direction==1:
        #默认向右转圈
        utils.key_down('d')
        #默认向右后方抛竿
        utils.move_mouse_relative_smooth(1150, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    elif config.direction==2:
        #默认向左转圈
        utils.key_down('a')
        #默认向左后方抛竿
        utils.move_mouse_relative_smooth(-850, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
    else:
        utils.move_mouse_relative_smooth(500, 0, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))

    sleep_time(random.uniform(1.52, 1.62))

    config.is_important_action=False

"""
自动钓鱼,单线程版本
"""
def auto_fish_single():
    """
    开启自动钓鱼主流程
    """
    if config.stop_event.is_set():
        return
    # === 初始化阶段 ===
    if not config.stop_event.is_set():
        if config.is_trolling_mode:
            trolling_fish()
        else:
            move_to_bow()

    # 拿出鱼竿
    if config.is_fly_ticket:
        sleep_time(random.uniform(0.42, 0.52))
        utils.key_down('U')
        sleep_time(random.uniform(0.42, 0.52))
        cout = 0
        max_attempts = 10  # 最大尝试次数
        flyrod_regions=[]
        while not config.stop_event.is_set() and cout < max_attempts:
            cout += 1
            flyrod_regions=utils.find_template_in_regions(config.FlyRodRegionScreenshot, 'flyrod.png', confidence=0.95)
            if len(flyrod_regions) > 0:
                drr=flyrod_regions[0]
                utils.move_mouse_random_in_region((drr["left"], drr["top"], drr["width"], drr["height"]))
                break
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse(0.1)
        sleep_time(random.uniform(0.42, 0.52))
        utils.key_up('U')
        
        #配置鱼杆
        sleep_time(random.uniform(2, 2.1))
        utils.press_key('v')
        #修改钓组
        sleep_time(random.uniform(1.42, 1.52))
        utils.move_mouse_random_in_region((1105,258,80,17))
        sleep_time(random.uniform(0.42, 0.52))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.42, 0.52))
        utils.move_mouse_random_in_region((1039,421,159,47))
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

    # if not config.stop_event.is_set():
    #     utils.renew_ticket_blocking()
    #     #防止被自动续费船票的操作打断操作
    #     config.is_important_action=True
    #     check_reel_type()
    #     config.is_important_action=False

    if not config.stop_event.is_set():
        utils.renew_ticket_blocking()
        #防止被自动续费船票的操作打断操作
        # config.is_important_action=True
        # adjust_reel_settings()
        # config.is_important_action=False
        config.is_important_action=True
        sleep_time(random.uniform(0.41, 0.52))
        utils.move_mouse_relative_smooth(0, 280, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
        sleep_time(random.uniform(0.41, 0.52))
        adjust_reel_settings()
        utils.move_mouse_relative_smooth(0, -280, duration=random.uniform(0.4, 0.6), steps=random.randint(30, 50), interrupt_checker=lambda: getattr(config, 'running', True))
        sleep_time(random.uniform(0.41, 0.52))
        config.is_important_action=False

    # # === 后台功能线程 ===
    start_daemon_thread(check_player_vitals)
    start_daemon_thread(set_friction_from_slider)
    start_daemon_thread(check_and_replace_damaged_bait)
    
    #自动钓鱼的过程改成单线程
    while not config.stop_event.is_set():
        """
        收起鱼叉
        """
        if config.is_space and not config.stop_event.is_set():
            utils.renew_ticket_blocking()
            config.is_important_action=True
            config.is_space = False
            utils.click_left_mouse(random.uniform(1, 1.1))
            utils.press_key('Space')
            config.is_important_action=False
            
        """
        开始抛竿
        """
        config.is_cast_rod=False
        if utils.check_template_in_region(config.region_cast_rod,'cast_rod.png') and not config.stop_event.is_set():
             #检查要不要切鱼
            if not config.stop_event.is_set():
                #阻塞行为，续票完成后再执行下面的操作
                utils.renew_ticket_blocking()
                config.is_important_action=True
                cut_fish()
                config.is_important_action=False
            #检查是不是满护了
            if not config.stop_event.is_set():
                if not check_fishnet_status():
                    logger.info("🧺 鱼护已满，小退")
                    return
            if not config.stop_event.is_set():
                #抛竿前判断要不要回坑
                if not return_destination():
                    #阻塞行为，续票完成后再执行下面的操作
                    utils.renew_ticket_blocking()
                    config.is_important_action=True
                    utils.click_left_mouse(random.uniform(0.08, 0.11))
                    config.is_cast_rod=True
                    logger.info("✅ 已经抛竿")
                    config.is_important_action=False
                else: continue
        #重新检测
        else:continue
        
        """
        打状态
        """
        if not get_fish_status():
            break

        """
        鱼上钩收线
        """
        if not reel_in_fish():
            break

        """
        鱼入护
        """
        process_fish_and_decide()
    

   