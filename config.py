
# === 可配置参数 ===
# === 热键配置 ===
START_HOTKEY = 'F6'
STOP_HOTKEY = 'F8'
# EXIT_HOTKEY = 'F10'



destination=(469,337)#34坑位
dist=32#回坑最大的距离
# destination=(367,454)#30坑位
# dist=18
# destination=(307,173)#41坑位
# dist=45
#1为纺车轮，2为鼓轮，3为电轮
reel_type=3
#1为轻微，2为强烈，3为阶梯，4为随机，5为摆烂，6为自定义
status_type=1
#自定义状态，status_sleep为抬竿间隔，status_click为右键按住时间
is_shift=True
status_sleep=2
status_click=2

#沉底后延迟时间
sleep_when_on_status=0
#沉底后收线时间
reeling_time_after_status_detected=0

#补充船票的数量
ticket_target_count=3

fishing_rod_btn=1#鱼竿按键默认为1
stamina_btn=4#补充体力值的按键默认为4
hunger_btn=5#补充饥饿的按键默认5

change_leader_line_max_value=0.3#损耗多少更换引线


cast_line_meters=0 #卡米

#出线多少米小退
max_cast_line_meters=120

#是否为鼓轮
is_MN=False

#是否切鱼块
is_cut_fish=True
#是否切3k以下的绿青鳕鱼块
is_cut_low_quality_fish=False

#绿青鳕鱼块种类，1是小块，2是鱼柳，3是大块
#小块和鱼柳需要大于300克，大块需要大于600克
fish_block_types1 = 2
#鲭块种类，1是小块，2是鱼柳，默认是鱼柳
fish_block_types2 = 2

#是不是飞机票
is_fly_ticket=False

#开启拖钓模式
is_trolling_mode=False

#拖掉转圈方向,1为向右转圈，2为左转圈,3为直线
direction=1

#拖掉打状态的方式,1为卡米强抽,2为打电梯
trolling_status_type=1

#打电梯的收线速度
trolling_reeling_speed=20

#打电梯的放线米数
trolling_unlock_meters=15

#点锁设置
is_open_lock_unlock=True
#单独开启点锁功能
open_lock_unlock_alone=False
#降摩擦的值
max_lock_unlock_value=0.6
#升摩擦的值
min_lock_unlock_value=0

#鼓轮切换传动比
is_open_gear_ratio=True
gear_ratio = 0.3


#水底和路亚钓鱼参数
#是否为彩虹线
is_rainbow_line=True
#是否保留不达标的鱼
keep_underperforming_fish=False
#路亚模式，1是白河路亚，2是老奥打狗
lure_mode=1
#水底轮子收线速度
bottom_reel_speed=50
#水底轮子摩擦力
bottom_reel_friction=25
#路亚轮子收线速度
lure_reel_speed=25
#路亚轮子摩擦力
lure_reel_friction=23
#放下竿子的按键
put_down_rod_key='x'
#点位
laoao_points=[]
hupo_points=[]
ahetubahe_points=[]
tonghu_points=[]
baihe_lure_points=[]
aier_lure_points=[]


#路亚鱼竿名称
lure_rod_name='S68ML'
#自动模式：0为全天水底，1为全天路亚，2为白天路亚，晚上水底,3为只有水底，4为只有路亚
auto_mode=3
#水底的地图：0为旧奥斯特罗格湖，1为琥珀湖，2铜湖，3阿赫图巴河
bottom_map=0
#路亚的地图：0为旧奥斯特罗格湖，1为白河,2为埃尔克湖
lure_map=1
#auto_mode为3的时候的卡米数
only_bottom_meters=10
#沉底时间
sink_time=12

lure_rod_power=70
lure_rod_reeling_duration=1.1
lure_rod_stop_duration=0.5

#手竿
#水面状态，1为平静，2为波动
water_status=2
#抛竿的力度
hand_rod_power=70
#漂流状态下等待的总时长
drifting_total_duration=90

#需要更换的主线名称
hand_rod_main_line_name=''
#需要更换的漂浮物名称
hand_rod_float_name=''
#需要更换的沉子的名称
hand_rod_sink_name=''
#需要更换的引线的名称
hand_rod_leader_line_name=''
#需要更换的钩子的名称
hand_rod_hook_name=''
#需要更换的饵料名称1
hand_rod_bait_name1=''
#需要更换的饵料名称2
hand_rod_bait_name2=''

#手杆的钓鱼模式，1为全天手杆-自动卖鱼-换点，2为只有手杆
hand_rod_fishing_mode=1
#全天手杆的地图，1为唯唯诺诺河钓雅罗鱼，2为北顿钓黑海
hand_rod_fishing_map=1


#游戏重启配置
#模式1为steam端，2为独立端
game_mode=1
steam_path = r'C:\Program Files (x86)\Steam\steam.exe'
standalone_path = r'C:\Games\RF4_CN\RF4Launcher.exe'

#模式类型，1为手杆钓鱼，2为水底和路亚，3为海图搬砖,4为连点器
mode_type=1

min_sleep_time=3
max_sleep_time=4


# === 控制标志 ===
import threading
stop_event = threading.Event()
stop_event.clear()
named_threads={}
_stopping=False
program_stopped = True
program_starting = False  # 表示程序正在启动
# running = False  # 主程序是否在运行
need_restart=False #是否需要重新启动程序
need_restart_sign=False#重新启动程序的标志
need_back = True #是否需要回城
# is_electric_reel=False #是不是电轮
is_reeling_line=False #是不是正在收线
is_need_renew_ticket=False #是否需要续费船票
is_important_action=False #是否为重要的操作期间
is_mouse_down_right=False #是否按下右键抬竿子
is_space=False #是否拿出鱼叉
is_cast_rod=False #是否抛竿


# ------------------ 不可配置参数 ------------------
cut_fish_type = 0 #切鱼的类型0是没鱼切，1是绿青，2是鲭鱼，3为鱼块默认为0
current_fish_block_types1 =2 #当前需要切的绿青鳕鱼块种类
fps=60#与桌面帧数相关
tension_value=0#拉力条大小
current_position=None#当前的位置
income_once = []  # 用于记录每次卖鱼和咖啡厅获得的银币数
income = []  # 用于记录每次卖鱼获得的银币数
auto_change_pit=False
auto_pits=[]
current_fish_mode=None
import time

# ========== 每日休息相关 ==========
# 下一次休息的开始时间戳（秒）
next_rest_time = None  

# 休息时长（秒）
rest_duration = 0  

# 今天是否已经完成休息
rest_done_today = False  



# ------------------ 全局参数 ------------------
TARGET_WINDOW_TITLE = "Russian Fishing 4"  # 目标窗口名称

# ------------------ 截图参数 ------------------
# 鱼标志截图
FishRegionScreenshot = {"left": 1854, "top": 791, "width": 28, "height": 17}  # 鱼标志截图

#飞机竿区域
FlyRodRegionScreenshot = {"left": 395, "top": 46, "width": 1510, "height": 1033}

# 地图选择区域
MapPickerRegionScreenshot = {"left": 971, "top": 426, "width": 378, "height": 48} #地图选择入口截图区域
MapPickerRegionScreenshotFly = {"left": 971, "top": 500, "width": 378, "height": 48} #飞机票地图选择入口截图区域
testnuoweihai=(843,919,234,128)#测试
MapPickerRegionScreenshotClick=(971,426,378,48)#选择地图的入口
LaoaoMapPickerRegionScreenshotClick=(843,619,234,128)#老奥地图入口
BaiheMapPickerRegionScreenshotClick=(1097,619,234,128)#白河地图入口
HupohuMapPickerRegionScreenshotClick=(1097,769,234,128)#琥珀湖地图入口
TonghuMapPickerRegionScreenshotClick=(81,919,234,128)#铜湖地图入口

AierMapPickerRegionScreenshotClick=(335,619,234,128)#埃尔克湖地图入口
weiyouMapPickerRegionScreenshotClick=(589,619,234,128)#惟有诺克河地图入口
BeidunMapPickerRegionScreenshotClick=(335,769,234,128)#北顿涅茨河地图入口

MapPickerConfirmButtonRegionClick=(83,485,154,54)#地图进入按钮
MapLimitRegionScreenshot={"left": 727, "top": 399, "width": 106, "height": 102}#地图限制区域

# 退出游戏按钮区域
QuitGameButtonRegionScreenshot = {"left": 1372, "top": 687, "width": 116, "height": 116}  # 退出游戏按钮区域
QuitGameButtonRegionClick = (1372, 687, 116, 51)  # 退出游戏按钮点击区域

# 飞机票退出游戏按钮区域
QuitGameButtonRegionScreenshotFly = {"left": 1372, "top": 761, "width": 116, "height": 116}  # 退出游戏按钮区域
QuitGameButtonRegionClickFly = (1372, 761, 105, 40)  # 退出游戏按钮点击区域

QuitConfirmButtonRegionClick = (764, 546, 185, 37)  # 确认退出按钮区域

# Steam登录和独立登录区域
SteamLoginRegionScreenshot = {"left": 859, "top": 714, "width": 202, "height": 34}  # Steam登录区域
StandaloneLoginRegionScreenshot = {"left": 859, "top": 714, "width": 202, "height": 34}  # 独立登录区域
SteamLoginRegionClick = (859, 714, 202, 34)  # Steam登录点击区域
StandaloneLoginRegionClick = (859, 714, 202, 34)  # 独立登录点击区域
LoginErrorRegionScreenshot= {"left": 909, "top": 457, "width": 102, "height": 30}  # 登录错误区域
LossGameConnectRegionScreenshot= {"left": 848, "top": 457, "width": 224, "height": 70}  # 游戏失去连接区域
LossGameConnectRegionClick= (868, 566, 184, 36)  # 游戏失去连接按钮区域
GiftRegionScreenshot= {"left": 250, "top": 20, "width": 1493, "height": 135}  # 礼物区域
ServerLossRegionScreenshot= {"left": 858, "top": 453, "width": 204, "height": 36}  # 服务器未响应
ServerLossRegionClick=(868,566,184,36)
StandaloneLoginMenuRegionClick=(1358,760,158,44)

SellFishLoadingLogoRegionScreenshot={"left": 1090, "top": 600, "width": 151, "height": 40} #加载的logo

ShopTitleRegionScreenshot={"left": 902, "top": 19, "width": 116, "height": 42} #商店名字

LoadingLogoRegionScreenshot={"left": 1065, "top": 600, "width": 151, "height": 40} #加载的logo-购买船票

CoffeeFishBasketEmptyRegionScreenshot={"left": 1044, "top": 394, "width": 275, "height": 150}#空鱼护的log-咖啡厅

FishBasketEmptyRegionScreenshot={"left": 1037, "top": 391, "width": 252, "height": 156}#空鱼护的log

TicketCountDisplayRegionScreenshot = {"left": 1383, "top": 284, "width": 50, "height": 30} #船票数量显示区域

DisplayTicketOptionsRegionScreenshot = {"left": 885, "top": 60, "width": 150, "height": 40} #选票的界面

RenewTicketTipRegionScreenshot = {"left": 1608, "top": 968, "width": 284, "height": 80} #续费船票的提示区域

region_stamina = (188, 955, 150, 8)#体力值识别区域
region_hunger  = (188, 986, 150, 8)#饥饿值识别区域

region_cast_rod = {"left": 532, "top": 1016, "width": 165, "height": 27}       # 检测是否抛竿的区域

region_hook_status = {"left": 530, "top": 1023, "width": 82, "height": 17}     # 鱼钩沉底的检测区域

region_cast_line_meters = {"left": 1113, "top": 1006, "width": 276, "height": 36}  # 出线米数检测区域（识别文字）

region_electric_reel_speed = {"left": 1339, "top": 957, "width": 45, "height": 21}  # 电轮收线速度区域

region_fish_bite = {"left": 532, "top": 1006, "width": 36, "height": 36}        # 鱼咬钩的检测区域

region_reel_name = {"left": 1073, "top": 327, "width": 700, "height": 39}       # 鱼轮类型检查区域

region_leader_line_name = {"left": 1073, "top": 511, "width": 700, "height": 39}   # 引线名称区域

region_keepnet = {"left": 806, "top": 971, "width": 49, "height": 21}          # 入护图标区域

region_sure = {"left": 937, "top": 971, "width": 49, "height": 21}          # 确定图标区域

region_fail_sure = {"left": 900, "top": 556, "width": 120, "height": 36}          # 未成功确定图标区域

region_fish_name = {"left": 440, "top": 70, "width": 1040, "height": 54}        # 鱼的名称区域

region_fish_info = {"left": 717, "top": 132, "width": 482, "height": 30}       # 鱼的详情信息

region_coffee_shop_task_fish_count = {"left": 267, "top": 578, "width": 108, "height": 28}    # 咖啡店任务鱼的任务量

region_coffee_shop_task_sign = {"left": 118, "top": 165, "width": 108, "height": 38}    # 咖啡店任务页面标志

region_fish_quantity = {"left": 1845, "top": 811, "width": 47, "height": 15}   # 鱼护详情信息
region_fish_quantity_other = {"left": 116, "top": 251, "width": 62, "height": 25}   # 鱼护详情信息

region_damaged_lure = {"left": 530, "top": 1019, "width": 67, "height": 22}   # 拟饵损坏的图片模板

region_check_damaged_bait_area = {"left": 1006, "top": 129, "width": 875, "height": 927}  # 检查拟饵损坏的区域

region_check_assembly_area = {"left": 533, "top": 1020, "width": 77, "height": 20}  # 检查拟饵组装的区域

region_check_damaged_bait_area_red = {"left": 264, "top": 152, "width": 1393, "height": 801}  # 检查拟饵损坏的区域-red

region_adjust_reel_settings_area = {"left": 936, "top": 963, "width": 48, "height": 40}  # 检查摩擦力和收线速度的大小区域
region_adjust_reel_settings_meters_area = {"left": 936, "top": 963, "width": 48, "height": 23}  # 检查卡米数的区域
# region_adjust_reel_settings_meters_area_fix = {"left": 936, "top": 963, "width": 48, "height": 31}  # 检查卡米数的区域

region_cut_fish_area = {"left": 390, "top": 128, "width": 130, "height": 951}  # 切鱼的区域

region_fishing_tension_bar = (535,1048,848,9)  # 拉鱼的拉力条区域

region_leader_line_damage_bar = (1001,582,864,3)  # 引线损坏情况

# 咖啡厅价格区域（172, 347, 212, 36）
CafePriceRegionScreenshot = {"left": 172, "top": 347, "width": 212, "height": 36}
# 鱼市价格区域（164, 322, 176, 28）
FishMarketPriceRegionScreenshot = {"left": 164, "top": 322, "width": 176, "height": 28}

#水底和路亚钓鱼参数
GameTimeRegionScreenshotmain={"left": 1745, "top": 112, "width": 136, "height": 36}

GameTimeRegionScreenshot={"left": 971, "top": 482, "width": 184, "height": 66}
GameTimeRegionScreenshotFly={"left": 971, "top": 556, "width": 184, "height": 66}


#手杆上鱼的检测区域
region_hand_rod_bite = {"left": 881, "top": 835, "width": 158, "height": 158}

#手杆主线配置区域
region_hand_rod_main_line = (1001, 327, 64, 44)
#手杆漂浮配置区域
region_hand_rod_float = (1001, 409, 64, 44)
#手杆沉子配置区域
region_hand_rod_sink = (1001, 491, 64, 44)
#手杆引线配置区域
region_hand_rod_leader_line = (1001, 583, 64, 44)
#手杆鱼钩配置区域
region_hand_rod_hook = (1001, 675, 64, 44)
#手杆鱼饵配置区域
region_hand_rod_bait1 = (1001, 767, 64, 44)
#手杆鱼饵配置区域2
region_hand_rod_bait2 = (1001, 859, 64, 44)


#缺少材料区域
region_missing_materials = {"left": 846, "top": 471, "width": 121, "height": 32}