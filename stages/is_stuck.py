from collections import deque
import config
from logger import logger
from utils import sleep_time
import navigator 

#障碍物判断
def is_stuck():
    current_pos = None  # 先定义为空值
    CHECK_INTERVAL = 0.5           # 每隔多少秒检查一次
    MAX_HISTORY = 360              # 保留最近1200次坐标
    static_positions = deque(maxlen=MAX_HISTORY)
    while not config.stop_event.is_set():
        current_pos =  config.current_position
        # current_pos =  navigator.get_current_position()
        if current_pos:    
            static_positions.append(current_pos)
            # 只有当数组满了再判断是否都相同
            if len(static_positions) == MAX_HISTORY:
                if all(pos == static_positions[0] for pos in static_positions):
                    logger.warning(f"🚨 坐标在最近 {MAX_HISTORY} 次都未变化，疑似卡住: {current_pos}")
                    #清空
                    static_positions.clear()

                    #如果是海上
                    if current_pos[0]>230:
                        logger.warning(f"🚨 在海上，忽略卡住信息")
                        continue
                    
                    #准备重启
                    config.need_restart=True

        sleep_time(CHECK_INTERVAL)

    logger.warning("检测卡住线程已经退出")

