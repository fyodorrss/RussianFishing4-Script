import time
import random
import config
from utils import sleep_time
import utils
from logger import logger 

#切鱼的流程
def cut_fish_process(fish_block_type):
    # 进入切鱼界面
    sleep_time(random.uniform(0.2, 0.3))
    utils.press_key('n')
    sleep_time(random.uniform(0.2, 0.3))
    utils.press_key_sc('PageDown')
    sleep_time(random.uniform(0.2, 0.3))
    utils.press_key_sc('PageDown')
    sleep_time(random.uniform(1.1, 1.2))
    # 映射不同类型到对应的图片名
    cut_fish_map = {
        1: 'lqxy.png',
        2: 'qy.png',
        3: 'fishmeat.png'
    }
    template_name = cut_fish_map.get(config.cut_fish_type)

    result = utils.find_template_in_regions(config.region_cut_fish_area, template_name, confidence=0.95)

    if isinstance(result, list) and result and isinstance(result[0], dict) and len(result) == 1:
        region = (result[0]["left"]+2, result[0]["top"]+2, result[0]["width"]-2, result[0]["height"]-2)
        utils.move_mouse_random_in_region(region)
        sleep_time(random.uniform(0.2, 0.3))
        utils.click_left_mouse()

        if config.cut_fish_type==3:
            sleep_time(random.uniform(0.2, 0.3))
            utils.move_mouse_random_in_region((946, 329, 850, 63))
        else:
            # 选择鱼刀
            sleep_time(random.uniform(0.2, 0.3))
            utils.move_mouse_random_in_region((946, 541, 850, 63))
        sleep_time(random.uniform(0.2, 0.3))
        utils.click_left_mouse()
        sleep_time(random.uniform(0.2, 0.3))
        utils.move_mouse_random_in_region((285, 203, 166, 273))
        sleep_time(random.uniform(0.2, 0.3))
        utils.click_left_mouse()
        sleep_time(0.1)
        utils.click_left_mouse()

        # 选择鱼块类型
        block_positions = {
            1: (1059, 329, 96, 96),
            2: (1059, 329, 96, 96),
            3: (1173, 329, 96, 96),
            4: (1287, 329, 96, 96),
        }

        if fish_block_type not in block_positions and config.cut_fish_type!=3:
            logger.warning("⚠️ 切鱼出错，类型出错。")
            sleep_time(random.uniform(0.2, 0.3))
            utils.press_key('Esc')
            return
        
        if fish_block_type !=1 and config.cut_fish_type!=3:
            #切指定鱼块
            sleep_time(random.uniform(0.2, 0.3))
            utils.move_mouse_random_in_region(block_positions[fish_block_type])
            sleep_time(random.uniform(0.2, 0.3))
            utils.click_left_mouse()
        #选择鱼的入口
        if config.cut_fish_type==3:
            sleep_time(random.uniform(0.2, 0.3))
            utils.move_mouse_random_in_region((946, 507, 850, 63))
        else:
            sleep_time(random.uniform(0.2, 0.3))
            utils.move_mouse_random_in_region((946, 719, 850, 63))
        sleep_time(random.uniform(0.2, 0.3))
        utils.click_left_mouse()
        #第一个选择区域
        sleep_time(random.uniform(0.2, 0.3))
        utils.move_mouse_random_in_region((284, 171, 246, 172))
        sleep_time(random.uniform(0.2, 0.3))
        utils.click_left_mouse()
        sleep_time(0.1)
        utils.click_left_mouse()
        #制作按钮
        sleep_time(random.uniform(0.2, 0.3))
        utils.move_mouse_random_in_region((773, 973, 120, 36))
        sleep_time(random.uniform(0.2, 0.3))
        utils.click_left_mouse()
        #定义超时
        max_move_time = 30  # 最长移动时间 2 分钟
        start_time = time.time()
        while not config.stop_event.is_set() and time.time() - start_time < max_move_time:
            if utils.check_template_in_region(config.region_sure,"sure.png") or utils.check_template_in_region(config.region_sure,"sure_other.png"):
                sleep_time(random.uniform(0.2, 0.3))
                utils.press_key('Space')
                break
            if utils.check_template_in_region(config.region_fail_sure,'fail_sure.png'):
                sleep_time(random.uniform(0.2, 0.3))
                utils.move_mouse_random_in_region((900, 556, 120, 36))#确定按钮
                sleep_time(random.uniform(0.2, 0.3))
                utils.click_left_mouse()
                break
            sleep_time(random.uniform(0.2, 0.3))
        sleep_time(random.uniform(0.2, 0.3))
        utils.press_key('Esc')
        sleep_time(random.uniform(0.2, 0.3))
        utils.press_key('Esc')
      
    else:
        logger.warning("⚠️ 切鱼出错，未能识别图像。")
        sleep_time(random.uniform(0.2, 0.3))
        utils.press_key('Esc')
#切鱼的主函数
def cut_fish():
    """
    切鱼
    """
    if config.cut_fish_type == 1:  # 绿青鳕
        cut_fish_process(fish_block_type=config.current_fish_block_types1)

    elif config.cut_fish_type == 2:  # 鲭鱼
        cut_fish_process(fish_block_type=config.fish_block_types2)

    elif config.cut_fish_type == 3: #鱼肉
        cut_fish_process(None)


    #切完鱼重置cut_fish_type
    config.cut_fish_type = 0    
