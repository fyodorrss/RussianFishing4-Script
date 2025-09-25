import config
import utils
from utils import sleep_time
import random
import time
from logger import logger


def run_loop():
    random_click_and_space()
    
def random_click_and_space(
    duration_minutes=500,
    interval_range=(0.07, 0.12),
    region=(845, 976, 33, 24),
    move_interval_range=(6, 15)  # 鼠标移动的随机间隔（秒）
):
    """
    在指定区域内随机移动并执行鼠标点击 + 按下空格，持续指定时间。
    """
    end_time = time.time() + duration_minutes * 60
    logger.info(f"▶️ 连点器启动，持续 {duration_minutes} 分钟...")

    # 初始化下次移动时间
    next_move_time = time.time() + random.uniform(*move_interval_range)

    while time.time() < end_time and not config.stop_event.is_set():
        # 判断是否该移动
        if time.time() >= next_move_time:
            utils.move_mouse_random_in_region(region)
            sleep_time(random.uniform(0.05, 0.07))
            # 重新设置下次移动时间
            next_move_time = time.time() + random.uniform(*move_interval_range)

        # 点击
        utils.click_left_mouse()
        sleep_time(random.uniform(0.04, 0.06))

        # 缺少材料
        if utils.check_template_in_region(config.region_missing_materials, "missingingredients.png"):
            logger.warning("🔁 检测到缺少材料，停止脚本")
            utils.stop_program()
            return

        # 制作失败
        if utils.check_template_in_region(config.region_fail_sure, "failsure.png"):
            logger.warning("🔁 检测到制作失败，点击空格继续")
            utils.key_down('space')
            sleep_time(random.uniform(0.04,0.05))
            utils.key_up('space')
            # 继续循环，不退出

        # 随机间隔
        sleep_time(random.uniform(*interval_range))

    logger.info("✅ 连点器结束。")
