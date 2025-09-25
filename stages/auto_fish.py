import threading
import config
from stages.adjust_reel_settings import adjust_reel_settings
from stages.cast_rod import cast_rod
from stages.change_bait import change_bait
from stages.check_player_vitals import check_player_vitals
from stages.check_reel_type import check_reel_type
from stages.move_to_bow import move_to_bow
from stages.put_fish_in_keepnet import put_fish_in_keepnet
from stages.reel_line import reel_line
from stages.set_friction_from_slider import set_friction_from_slider
from stages.set_rod_status import set_rod_status



#自动钓鱼
def auto_fish():
    """
    开启自动钓鱼主流程
    """

    if config.stop_event.is_set():
        return

    # === 初始化阶段 ===
    if not config.stop_event.is_set():
        move_to_bow()

    if not config.stop_event.is_set():
        check_reel_type()

    if not config.stop_event.is_set():
        adjust_reel_settings()

    # === 后台功能线程 ===
    start_daemon_thread(check_player_vitals, "check_player_vitals")
    start_daemon_thread(set_friction_from_slider, "set_friction_from_slider")
    start_daemon_thread(change_bait, "change_bait")
    start_daemon_thread(cast_rod, "cast_rod")
    start_daemon_thread(set_rod_status, "set_rod_status")
    start_daemon_thread(reel_line, "reel_line")
    start_daemon_thread(put_fish_in_keepnet, "put_fish_in_keepnet")

def start_daemon_thread(target_func, name=None):
    """
    封装线程启动逻辑，添加名称便于调试
    """
    thread = threading.Thread(target=target_func, name=name, daemon=True)
    thread.start()
    