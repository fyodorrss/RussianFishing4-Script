import math
import cv2
import keyboard
import numpy as np
import time
import random
import ctypes
import os
import threading
import pyautogui
import config
import re
from collections import Counter, deque
from PIL import Image
import win32api
import win32con
from logger import logger

# ------------------ 通过 SendInput 实现模拟键盘和鼠标 ------------------
# 常量定义
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

MOUSEEVENTF_LEFTDOWN  = 0x0002
MOUSEEVENTF_LEFTUP    = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP   = 0x0010

MOUSEEVENTF_WHEEL = 0x0800

KEYEVENTF_KEYUP = 0x0002

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000

KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_EXTENDEDKEY = 0x0001

# 根据指针大小确定 ULONG_PTR
ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong
PUL = ctypes.POINTER(ctypes.c_ulong)

# 结构体定义
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ULONG_PTR)
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        # 兼容两种写法，使用 ULONG_PTR 指针
        ("dwExtraInfo", ULONG_PTR)
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_short)
    ]

class _INPUTunion(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("union", _INPUTunion)
    ]

# 绑定 SendInput 函数
SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = [ctypes.c_uint, ctypes.POINTER(INPUT), ctypes.c_int]
SendInput.restype = ctypes.c_uint

# 虚拟键码映射表
def get_virtual_key(key):
    """
    根据输入的按键名称返回对应的虚拟键值。
    参数:
        key_name (str): 按键名称（例如，"1", "A", "F1", "Left Shift"）。
    返回:
        tuple: (虚拟键值十六进制, 虚拟键值十进制, 按键描述) 或 (None, None, 错误消息)。
    """
    # 扩展的虚拟键值映射
    vk_map = {
        # 数字键 (主键盘)
        "1": (0x31, 49, "Number 1"),
        "2": (0x32, 50, "Number 2"),
        "3": (0x33, 51, "Number 3"),
        "4": (0x34, 52, "Number 4"),
        "5": (0x35, 53, "Number 5"),
        "6": (0x36, 54, "Number 6"),
        "7": (0x37, 55, "Number 7"),
        "8": (0x38, 56, "Number 8"),
        "9": (0x39, 57, "Number 9"),
        "0": (0x30, 48, "Number 0"),
        
        # 字母键 (A-Z)
        "A": (0x41, 65, "Letter A"),
        "B": (0x42, 66, "Letter B"),
        "C": (0x43, 67, "Letter C"),
        "D": (0x44, 68, "Letter D"),
        "E": (0x45, 69, "Letter E"),
        "F": (0x46, 70, "Letter F"),
        "G": (0x47, 71, "Letter G"),
        "H": (0x48, 72, "Letter H"),
        "I": (0x49, 73, "Letter I"),
        "J": (0x4A, 74, "Letter J"),
        "K": (0x4B, 75, "Letter K"),
        "L": (0x4C, 76, "Letter L"),
        "M": (0x4D, 77, "Letter M"),
        "N": (0x4E, 78, "Letter N"),
        "O": (0x4F, 79, "Letter O"),
        "P": (0x50, 80, "Letter P"),
        "Q": (0x51, 81, "Letter Q"),
        "R": (0x52, 82, "Letter R"),
        "S": (0x53, 83, "Letter S"),
        "T": (0x54, 84, "Letter T"),
        "U": (0x55, 85, "Letter U"),
        "V": (0x56, 86, "Letter V"),
        "W": (0x57, 87, "Letter W"),
        "X": (0x58, 88, "Letter X"),
        "Y": (0x59, 89, "Letter Y"),
        "Z": (0x5A, 90, "Letter Z"),
        
        # 功能键 (F1-F12)
        "F1": (0x70, 112, "Function F1"),
        "F2": (0x71, 113, "Function F2"),
        "F3": (0x72, 114, "Function F3"),
        "F4": (0x73, 115, "Function F4"),
        "F5": (0x74, 116, "Function F5"),
        "F6": (0x75, 117, "Function F6"),
        "F7": (0x76, 118, "Function F7"),
        "F8": (0x77, 119, "Function F8"),
        "F9": (0x78, 120, "Function F9"),
        "F10": (0x79, 121, "Function F10"),
        "F11": (0x7A, 122, "Function F11"),
        "F12": (0x7B, 123, "Function F12"),
        
        # 控制键
        "Left Shift": (0xA0, 160, "Left Shift"),
        "Right Shift": (0xA1, 161, "Right Shift"),
        "Left Ctrl": (0xA2, 162, "Left Control"),
        "Right Ctrl": (0xA3, 163, "Right Control"),
        "Left Alt": (0xA4, 164, "Left Alt"),
        "Right Alt": (0xA5, 165, "Right Alt"),
        "Enter": (0x0D, 13, "Enter"),
        "Esc": (0x1B, 27, "Escape"),
        "Space": (0x20, 32, "Spacebar"),
        "Tab": (0x09, 9, "Tab"),
        "Backspace": (0x08, 8, "Backspace"),
        "Caps Lock": (0x14, 20, "Caps Lock"),
        
        # 符号键 (主键盘)
        "`": (0xC0, 192, "Backtick"),
        "-": (0xBD, 189, "Minus"),
        "=": (0xBB, 187, "Equals"),
        "[": (0xDB, 219, "Left Bracket"),
        "]": (0xDD, 221, "Right Bracket"),
        "\\": (0xDC, 220, "Backslash"),
        ";": (0xBA, 186, "Semicolon"),
        "'": (0xDE, 222, "Single Quote"),
        ",": (0xBC, 188, "Comma"),
        ".": (0xBE, 190, "Period"),
        "/": (0xBF, 191, "Slash"),
        
        # 导航键
        "Left Arrow": (0x25, 37, "Left Arrow"),
        "Up Arrow": (0x26, 38, "Up Arrow"),
        "Right Arrow": (0x27, 39, "Right Arrow"),
        "Down Arrow": (0x28, 40, "Down Arrow"),
        "Home": (0x24, 36, "Home"),
        "End": (0x23, 35, "End"),
        "Page Up": (0x21, 33, "Page Up"),
        "Page Down": (0x22, 34, "Page Down"),
        "Delete": (0x2E, 46, "Delete"),
        "Insert": (0x2D, 45, "Insert"),
        
        # 小键盘数字键
        "NumPad 0": (0x60, 96, "NumPad 0"),
        "NumPad 1": (0x61, 97, "NumPad 1"),
        "NumPad 2": (0x62, 98, "NumPad 2"),
        "NumPad 3": (0x63, 99, "NumPad 3"),
        "NumPad 4": (0x64, 100, "NumPad 4"),
        "NumPad 5": (0x65, 101, "NumPad 5"),
        "NumPad 6": (0x66, 102, "NumPad 6"),
        "NumPad 7": (0x67, 103, "NumPad 7"),
        "NumPad 8": (0x68, 104, "NumPad 8"),
        "NumPad 9": (0x69, 105, "NumPad 9"),
        
        # 小键盘运算符
        "NumPad +": (0x6B, 107, "NumPad Plus"),
        "NumPad -": (0x6D, 109, "NumPad Minus"),
        "NumPad *": (0x6A, 106, "NumPad Multiply"),
        "NumPad /": (0x6F, 111, "NumPad Divide"),
        "NumPad .": (0x6E, 110, "NumPad Decimal"),
        
        # 其他键
        "Num Lock": (0x90, 144, "Num Lock"),
        "Scroll Lock": (0x91, 145, "Scroll Lock"),
        "logger.info Screen": (0x2C, 44, "logger.info Screen"),
        "Pause": (0x13, 19, "Pause")
    }
    
  # 处理输入：如果是整数，转换为字符串
    if isinstance(key, int):
        key = str(key)
    
    # 规范化输入：仅对字母键应用 title()
    if isinstance(key, str):
        if key.isalpha():
            key = key.strip().title()
        else:
            key = key.strip()
    else:
        return None, None, f"错误: 输入 '{key}' 无效，必须是字符串或整数"

    if key in vk_map:
        hex_vk, dec_vk, desc = vk_map[key]
        return hex_vk
    return None, None, f"错误: 按键 '{key}' 未在 vk_map 中找到"

# 线程锁，保证多线程调用安全
_send_lock = threading.Lock()

def _send_input(inputs):
    with _send_lock:
        n_inputs = len(inputs)
        arr = (INPUT * n_inputs)(*inputs)
        sent = SendInput(n_inputs, arr, ctypes.sizeof(INPUT))
        if sent == 0:
            err = ctypes.windll.kernel32.GetLastError()
            raise RuntimeError(f"SendInput failed with error code: {err}")
        return sent

def key_down(vk_code):
    """按下按键，不松开"""
    vk_code=get_virtual_key(vk_code)
    ki = KEYBDINPUT(wVk=vk_code, wScan=0, dwFlags=0, time=0, dwExtraInfo=ULONG_PTR(0))
    inp = INPUT(type=INPUT_KEYBOARD, union=_INPUTunion(ki=ki))
    return _send_input([inp])

def key_up(vk_code):
    """松开按键"""
    vk_code=get_virtual_key(vk_code)
    ki = KEYBDINPUT(wVk=vk_code, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=ULONG_PTR(0))
    inp = INPUT(type=INPUT_KEYBOARD, union=_INPUTunion(ki=ki))
    return _send_input([inp])

def press_key(vk_code,hold_time=0.05):
    """按下并松开按键（完整按键事件）"""
    key_down(vk_code)
    time.sleep(hold_time)  # 保持按下时间
    key_up(vk_code)

# 扫描码映射表
scan_code_map = {
    # 字母
    'A': (0x1E, False), 'B': (0x30, False), 'C': (0x2E, False), 'D': (0x20, False),
    'E': (0x12, False), 'F': (0x21, False), 'G': (0x22, False), 'H': (0x23, False),
    'I': (0x17, False), 'J': (0x24, False), 'K': (0x25, False), 'L': (0x26, False),
    'M': (0x32, False), 'N': (0x31, False), 'O': (0x18, False), 'P': (0x19, False),
    'Q': (0x10, False), 'R': (0x13, False), 'S': (0x1F, False), 'T': (0x14, False),
    'U': (0x16, False), 'V': (0x2F, False), 'W': (0x11, False), 'X': (0x2D, False),
    'Y': (0x15, False), 'Z': (0x2C, False),

    # 数字主键区
    '0': (0x0B, False), '1': (0x02, False), '2': (0x03, False), '3': (0x04, False),
    '4': (0x05, False), '5': (0x06, False), '6': (0x07, False), '7': (0x08, False),
    '8': (0x09, False), '9': (0x0A, False),

    # 功能键
    'Enter': (0x1C, False),
    'Escape': (0x01, False),
    'Backspace': (0x0E, False),
    'Tab': (0x0F, False),
    'Space': (0x39, False),
    'CapsLock': (0x3A, False),

    # F1-F12
    'F1': (0x3B, False), 'F2': (0x3C, False), 'F3': (0x3D, False), 'F4': (0x3E, False),
    'F5': (0x3F, False), 'F6': (0x40, False), 'F7': (0x41, False), 'F8': (0x42, False),
    'F9': (0x43, False), 'F10': (0x44, False), 'F11': (0x57, False), 'F12': (0x58, False),

    # 导航和控制键
    'Insert': (0x52, True), 'Delete': (0x53, True), 'Home': (0x47, True), 'End': (0x4F, True),
    'PageUp': (0x49, True), 'PageDown': (0x51, True),
    'LeftArrow': (0x4B, True), 'UpArrow': (0x48, True),
    'RightArrow': (0x4D, True), 'DownArrow': (0x50, True),

    # 修饰键
    'LeftShift': (0x2A, False), 'RightShift': (0x36, False),
    'LeftCtrl': (0x1D, False), 'RightCtrl': (0x1D, True),
    'LeftAlt': (0x38, False), 'RightAlt': (0x38, True),

    # 小键盘（NumPad）
    'Num0':     (0x52, False),
    'Num1':     (0x4F, False),
    'Num2':     (0x50, False),
    'Num3':     (0x51, False),
    'Num4':     (0x4B, False),
    'Num5':     (0x4C, False),
    'Num6':     (0x4D, False),
    'Num7':     (0x47, False),
    'Num8':     (0x48, False),
    'Num9':     (0x49, False),
    'NumDot':   (0x53, False),   # 小键盘小数点
    'NumAdd':   (0x4E, False),   # 小键盘 +
    'NumSub':   (0x4A, False),   # 小键盘 -
    'NumMul':   (0x37, False),   # 小键盘 *
    'NumDiv':   (0x35, True),    # 小键盘 /
    'NumEnter': (0x1C, True),    # 小键盘回车（扩展键）
}

def create_key_input(scancode, extended=False, keyup=False):
    flags = KEYEVENTF_SCANCODE
    if extended:
        flags |= KEYEVENTF_EXTENDEDKEY
    if keyup:
        flags |= KEYEVENTF_KEYUP
    ki = KEYBDINPUT(wVk=0, wScan=scancode, dwFlags=flags, time=0, dwExtraInfo=0)
    return INPUT(type=INPUT_KEYBOARD, union=_INPUTunion(ki=ki))

def key_down_sc(keyname):
    if keyname not in scan_code_map:
        raise ValueError(f"按键名 {keyname} 不支持或拼写错误")
    scancode, extended = scan_code_map[keyname]
    inp = create_key_input(scancode, extended, keyup=False)
    _send_input([inp])

def key_up_sc(keyname):
    if keyname not in scan_code_map:
        raise ValueError(f"按键名 {keyname} 不支持或拼写错误")
    scancode, extended = scan_code_map[keyname]
    inp = create_key_input(scancode, extended, keyup=True)
    _send_input([inp])

def press_key_sc(keyname, press_time=0.05):
    """
    按下指定扫描码按键，保持 press_time 秒，再松开
    :param keyname: 按键名称，如 'PageDown'
    :param press_time: 按下保持时间，单位秒，默认50毫秒
    """
    key_down_sc(keyname)
    time.sleep(press_time)
    key_up_sc(keyname)

# === 左键操作 ===
def click_left_mouse(hold_time=0.01):
    mouse_down_left()
    time.sleep(hold_time) 
    mouse_up_left()

def mouse_down_left():
    mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ULONG_PTR(0))
    inp = INPUT(INPUT_MOUSE, _INPUTunion(mi=mi))
    SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

def mouse_up_left():
    mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ULONG_PTR(0))
    inp = INPUT(INPUT_MOUSE, _INPUTunion(mi=mi))
    SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

# === 右键操作 ===
def click_right_mouse(hold_time=0.001):
    mouse_down_right()
    time.sleep(hold_time) 
    mouse_up_right()

def mouse_down_right():
    mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_RIGHTDOWN, 0, ULONG_PTR(0))
    inp = INPUT(INPUT_MOUSE, _INPUTunion(mi=mi))
    SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

def mouse_up_right():
    mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_RIGHTUP, 0, ULONG_PTR(0))
    inp = INPUT(INPUT_MOUSE, _INPUTunion(mi=mi))
    SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


# === 滚轮操作 ===
def mouse_wheel(delta):
    """
    模拟鼠标滚轮滚动

    :param delta: 滚动量，正值向上滚，负值向下滚。
                  一般一个刻度为120（Windows默认）
    """
    # 构造鼠标输入结构体，dx, dy 不移动，mouseData 代表滚动量
    mi = MOUSEINPUT(0, 0, delta, MOUSEEVENTF_WHEEL, 0, 0)
    inp = INPUT(INPUT_MOUSE, _INPUTunion(mi=mi))
    return _send_input([inp])

# def slow_scroll(up=True, steps=10, min_delay=0.05, max_delay=0.1):
#     delta = 12 if up else -12  # 每次滚动12单位，约为1/10个刻度
#     for _ in range(steps):
#         mouse_wheel(delta)
#         time.sleep(random.uniform(min_delay, max_delay))

def slow_scroll(up=True, steps=3, fps=config.fps):
    """
    更强力的滚轮模拟，适配帧驱动游戏输入
    :param up: True=向上, False=向下
    :param frames: 持续几帧
    :param fps: 游戏帧率，用于推算 sleep
    """
    delta = 12 if up else -12
    frame_interval = 1 / fps

    for _ in range(steps):
        mouse_wheel(delta)
        time.sleep(frame_interval)

# 获取刷新率
def get_refresh_rate():
    dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    return dm.DisplayFrequency


# === 移动到区域随机位置 ===
def send_absolute_mouse_move(x, y):
    """将鼠标移动到屏幕绝对坐标 (x, y)，使用归一化后的绝对输入"""
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    # 限制边界
    x = min(max(int(x), 0), screen_width - 1)
    y = min(max(int(y), 0), screen_height - 1)

    abs_x = int(x * 65535 / (screen_width - 1))
    abs_y = int(y * 65535 / (screen_height - 1))

    mi = MOUSEINPUT(
        dx=abs_x,
        dy=abs_y,
        mouseData=0,
        dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        time=0,
        dwExtraInfo=ULONG_PTR(0)
    )
    inp = INPUT(type=INPUT_MOUSE, union=_INPUTunion(mi=mi))
    _send_input([inp])

def smooth_move_to(target_x, target_y, duration=random.uniform(0.4, 0.6), steps=50, jitter=False):
    """平滑移动鼠标到目标位置（屏幕坐标），使用 SendInput 的绝对模式"""
    start_x, start_y = win32api.GetCursorPos()
    distance = ((target_x - start_x) ** 2 + (target_y - start_y) ** 2) ** 0.5
    if steps is None:
        steps = max(15, int(distance / 4))

    def ease_out_quad(t):
        return 1 - (1 - t) * (1 - t)

    for i in range(1, steps + 1):
        t = i / steps
        progress = ease_out_quad(t)
        cur_x = start_x + (target_x - start_x) * progress
        cur_y = start_y + (target_y - start_y) * progress

        if jitter:
            offset = 3  # 抖动幅度
            cur_x += random.uniform(-offset, offset) * math.sin(t * math.pi)
            cur_y += random.uniform(-offset, offset) * math.cos(t * math.pi)

        send_absolute_mouse_move(cur_x, cur_y)
        time.sleep(duration / steps)

def move_mouse_random_in_region(region, duration_range=(0.1, 0.2)):
    """在指定区域内随机目标点进行平滑移动"""
    x, y, w, h = region
    target_x = int(random.triangular(x, x + w, x + w / 2))
    target_y = int(random.triangular(y, y + h, y + h / 2))
    duration = random.uniform(*duration_range)
    smooth_move_to(target_x, target_y, duration=duration)

# === 鼠标相对移动 ===
# 计算贝塞尔曲线某一点
def bezier_point(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y

def move_mouse_relative_smooth(
    dx, dy, 
    duration=0.3, 
    steps=30, 
    max_jitter=1, 
    interrupt_checker=lambda: True
):
    """
    使用贝塞尔曲线+微抖动模拟人类鼠标相对移动。

    :param dx: 相对 X 总位移
    :param dy: 相对 Y 总位移
    :param duration: 总时长（秒）
    :param steps: 移动步数（越高越平滑）
    :param max_jitter: 最大微抖动像素（默认±1）
    :param interrupt_checker: 中断检测函数（返回 False 表示中断）
    """
    # 起点终点
    p0 = (0, 0)
    p2 = (dx, dy)

    # 控制点（中点附近加入随机扰动）
    mid_x = dx / 2 + random.randint(-15, 15)
    mid_y = dy / 2 + random.randint(-15, 15)
    p1 = (mid_x, mid_y)

    # 开始时间
    start_time = time.time()
    last_pos = (0, 0)

    for step in range(1, steps + 1):
        if not interrupt_checker():
            break

        t = step / steps
        target_pos = bezier_point(p0, p1, p2, t)

        # 微抖动模拟
        jitter_x = random.randint(-max_jitter, max_jitter) if step < steps else 0
        jitter_y = random.randint(-max_jitter, max_jitter) if step < steps else 0

        # 计算当前步相对位移
        rel_x = int(round(target_pos[0] + jitter_x - last_pos[0]))
        rel_y = int(round(target_pos[1] + jitter_y - last_pos[1]))

        if rel_x == 0 and rel_y == 0:
            continue

        mi = MOUSEINPUT(
            dx=rel_x,
            dy=rel_y,
            mouseData=0,
            dwFlags=MOUSEEVENTF_MOVE,
            time=0,
            dwExtraInfo=0
        )
        inp = INPUT(type=INPUT_MOUSE, union=_INPUTunion(mi=mi))
        _send_input([inp])

        last_pos = (last_pos[0] + rel_x, last_pos[1] + rel_y)
        time.sleep(duration / steps)

    # 时间补偿：确保整体 duration 精准
    elapsed = time.time() - start_time
    if elapsed < duration:
        time.sleep(duration - elapsed)

# ------------------ 模板匹配函数 ------------------
import dxgi
import sys

def get_resource_path(relative_path):
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)
def load_template(template_path):
    """加载模板图像（带缓存）"""
    # if template_path in template_cache:
    #     return template_cache[template_path]

    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # full_path = os.path.join(base_dir, "images", template_path)
    full_path = get_resource_path(os.path.join("images", template_path))
    template = cv2.imread(full_path, cv2.IMREAD_COLOR)

    if template is None:
        logger.debug(f"❌ 模板 {full_path} 加载失败")
        return None
    
    # template_cache[template_path] = template
    return template

def check_template_in_region(region, template_path, threshold=0.8, screenshot=None):
    """
    检测区域是否包含模板图像
    参数：
        region: (left, top, width, height)
        template_path: 相对 images/ 的模板路径
        threshold: 匹配阈值
        screenshot_cv: 如果已截图传入该区域图像，否则自动截图
    返回：匹配成功 True/False
    """

    # 载入模板
    template = load_template(template_path)
    if template is None:
        return False
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # 区域截图
    if screenshot is None:
        screenshot = dxgi.grab_region(region)
        if screenshot is None:
            logger.info(f"[⚠️] 截图失败: region={region}")
            return False

    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
    screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
    if screenshot_cv is None or screenshot_cv.size == 0:
        logger.info("[⚠️] screenshot_cv 无效")
        return False

    # 尺寸合法性检查
    if (screenshot_cv.shape[0] < template.shape[0]) or (screenshot_cv.shape[1] < template.shape[1]):
        logger.info(f"[⚠️] 区域太小: screenshot={screenshot_cv.shape}, template={template.shape}")
        logger.info(f"[DEBUG] 区域请求: {region}")
        logger.info(f"[DEBUG] 实际截图尺寸: {screenshot_cv.shape}")
        logger.info(f"[DEBUG] 模板尺寸: {template.shape}")
        return False
    # import datetime
    # now = datetime.datetime.now()
    # timestamp = now.strftime("%H%M%S_%f")[:-3]  # 精确到毫秒
    # filename = f"screenshot_{timestamp}.png"
    # cv2.imwrite(filename, np.array(screenshot))
    # logger.info(f"🖼️ 截图已保存：{filename}")

    # 模板匹配
    res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # 打印或保存截图可选
    # if region==config.region_hook_status:
    # logger.info(f"状态模板匹配置信度: {max_val:.3f}")
    
    return max_val >= threshold

def find_template_in_regions(region, template_filename, confidence=0.95):

    # 载入模板
    template = load_template(template_filename)
    if template is None:
        raise FileNotFoundError(f"模板图像加载失败: {template_filename}")
    
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    h, w = template_gray.shape

    # 截图指定区域
    # screenshot = pyautogui.screenshot(region=(region["left"], region["top"], region["width"], region["height"]))
    screenshot = dxgi.grab_region(region)
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
    screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
    

     # 尺寸合法性检查
    if (screenshot_cv.shape[0] < template.shape[0]) or (screenshot_cv.shape[1] < template.shape[1]):
        logger.info(f"[⚠️] 区域太小: screenshot={screenshot_cv.shape}, template={template.shape}")
        logger.info(f"[DEBUG] 区域请求: {region}")
        logger.info(f"[DEBUG] 实际截图尺寸: {screenshot_cv.shape}")
        logger.info(f"[DEBUG] 模板尺寸: {template.shape}")
        return False
    # timestamp = time.strftime("%H%M%S")  # 精简时间戳
    # filename = f"_{timestamp}.png"
    # cv2.imwrite(filename, np.array(screenshot))
    # logger.info(f"🖼️ 截图已保存：{filename}")

    # 模板匹配
    res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)
    
    matches = []
    for pt in zip(*loc[::-1]):
        match_rect = {
            "left": int(region["left"] + pt[0]),
            "top": int(region["top"] + pt[1]),
            "width": int(w),
            "height": int(h)
        }
        matches.append(match_rect)

    return matches

import datetime

def check_fish(region, template_path, threshold=0.6, screenshot=None, save_debug=False, use_gray=True):
    """
    检测区域是否包含模板图像（可选择灰度/彩色匹配，并保存裁剪图用于调试）
    参数：
        region: (left, top, width, height)
        template_path: 模板路径
        threshold: 匹配阈值
        screenshot: 已有截图 (PIL) 否则自动截图
        save_debug: 是否保存裁剪后的调试图
        use_gray: 是否转灰度进行匹配
    """

    # 载入模板
    template = load_template(template_path)
    if template is None:
        return False

    # 截图
    if screenshot is None:
        screenshot = dxgi.grab_region(region)
        if screenshot is None:
            logger.info(f"[⚠️] 截图失败: region={region}")
            return False

    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
    if screenshot_cv is None or screenshot_cv.size == 0:
        logger.info("[⚠️] screenshot_cv 无效")
        return False

    # 尺寸检查
    if (screenshot_cv.shape[0] < template.shape[0]) or (screenshot_cv.shape[1] < template.shape[1]):
        logger.info(f"[⚠️] 区域太小: screenshot={screenshot_cv.shape}, template={template.shape}")
        return False

    # ========= 提取中间 1/2 宽度 =========
    h_t, w_t = template.shape[:2]
    h_s, w_s = screenshot_cv.shape[:2]

    # 模板
    t_x1 = w_t // 4
    t_x2 = 3 * w_t // 4
    template_crop = template[:, t_x1:t_x2]

    # 截图
    s_x1 = w_s // 4
    s_x2 = 3 * w_s // 4
    screenshot_crop = screenshot_cv[:, s_x1:s_x2]

    # ========= 灰度 / 彩色处理 =========
    if use_gray:
        template_proc = cv2.cvtColor(template_crop, cv2.COLOR_BGR2GRAY)
        screenshot_proc = cv2.cvtColor(screenshot_crop, cv2.COLOR_BGR2GRAY)
    else:
        template_proc = template_crop
        screenshot_proc = screenshot_crop

    # ========= 保存裁剪图 =========
    if save_debug:
        os.makedirs("debug_crops", exist_ok=True)
        now = datetime.datetime.now().strftime("%H%M%S_%f")[:-3]  # 毫秒时间戳
        suffix = "gray" if use_gray else "color"
        cv2.imwrite(f"debug_crops/template_{suffix}_{now}.png", template_proc)
        cv2.imwrite(f"debug_crops/screenshot_{suffix}_{now}.png", screenshot_proc)

    # 尺寸检查
    if (screenshot_proc.shape[0] < template_proc.shape[0]) or (screenshot_proc.shape[1] < template_proc.shape[1]):
        logger.info(f"[⚠️] 中间部分太小: screenshot={screenshot_proc.shape}, template={template_proc.shape}")
        return False

    # 模板匹配
    res = cv2.matchTemplate(screenshot_proc, template_proc, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    print(f"🎣 鱼漂模板匹配置信度: {max_val:.3f} (阈值 {threshold})")

    return max_val > threshold



# ------------------ 截图函数用于颜色检测 ------------------
def grab_image_by_dxgi(bbox):
    """
    bbox: dict，包含 'left', 'top', 'width', 'height'
    返回：PIL.Image，跟 mss 生成的 img 一样，使用 Image.frombytes("RGB", size, data)
    """
    screenshot = dxgi.grab_region(bbox)
    if screenshot is None:
        logger.warning("截图为空")
        return None

    # screenshot.pixels 是原始字节数据（BGRA格式）
    # 需要转换为 RGB 格式的字节流，Image.frombytes("RGB", ...) 需要的就是 RGB 原始字节数据
    
    import numpy as np
    import cv2

    # 转成 numpy 数组 (height, stride/4, 4)
    arr = np.frombuffer(screenshot.pixels, dtype=np.uint8)
    arr = arr[:screenshot.height * screenshot.stride]
    arr = arr.reshape((screenshot.height, screenshot.stride // 4, 4))
    arr = arr[:, :screenshot.width, :]  # 截取有效宽度

    # BGRA 转 RGB
    arr_rgb = cv2.cvtColor(arr, cv2.COLOR_BGRA2RGB)

    # 转成连续的字节流
    rgb_bytes = arr_rgb.tobytes()

    # 用 Image.frombytes 构造图像
    img = Image.frombytes("RGB", (screenshot.width, screenshot.height), rgb_bytes)

    return img

# ------------------ 计算体力值或者饥饿值 ------------------
def get_region_colors(region):
    """
    获取区域内所有颜色及其分布
    region: (x, y, width, height)
    """
    x, y, width, height = region
    bbox = {"left": x, "top": y, "width": width, "height": height}
    
    img = grab_image_by_dxgi(bbox)

    # 转换为numpy数组
    img_array = np.array(img)

    # 获取所有像素的RGB值
    if len(img_array.shape) == 3:
        pixels = img_array.reshape(-1, 3)
        colors = [tuple(pixel) for pixel in pixels]
    else:
        colors = img_array.flatten().tolist()

    # 统计颜色频次
    color_count = Counter(colors)
    total_pixels = len(colors)

    # 计算占比并排序
    color_info = []
    for color, count in color_count.most_common():
        percentage = (count / total_pixels) * 100
        color_info.append({
            'color': color,
            'count': count,
            'percentage': percentage
        })

    return color_info

def get_most_unique_color(color_info):
    """
    从颜色列表中找出与其他颜色差异最大的颜色（欧几里得距离和最大）
    """
    def color_distance(c1, c2):
        return np.sqrt(sum((int(a) - int(b)) ** 2 for a, b in zip(c1, c2)))

    max_distance_sum = -1
    most_unique = None

    for base in color_info:
        total_distance = sum(color_distance(base['color'], other['color'])
                             for other in color_info if other != base)
        if total_distance > max_distance_sum:
            max_distance_sum = total_distance
            most_unique = base

    return most_unique

def analyze_region_colors(region):
    """
    综合分析区域颜色,返回体力或者饥饿值
    """
    # logger.info(f"分析区域: {region}")

    # 1. 获取所有颜色（显示前10个）
    all_colors = get_region_colors(region)[:10]
    
    # logger.info("\n=== 所有颜色分布（前10个）===")
    # for color_info in all_colors:
        # r, g, b = color_info['color']
        # logger.info(f"RGB({r:3d}, {g:3d}, {b:3d}): {color_info['percentage']:.2f}%")

    # 2. 分析最独特颜色
    unique = get_most_unique_color(all_colors)
    if unique:
        r, g, b = unique['color']
        # logger.info(f"\n=== 最独特的颜色 ===")
        # logger.info(f"RGB({r:3d}, {g:3d}, {b:3d}): {unique['percentage']:.2f}% （与其他颜色差异最大）")
        return float(f"{unique['percentage']:.2f}")
    else:
        return None    
    
# ------------------ 获取某一区域的绿黄红的颜色占比 ------------------
# ------------------ 计算拉力值 ------------------
def screenshot(region):
    """
    使用 mss 截图指定区域，返回 PIL 图像（RGB）
    region: (left, top, width, height)
    """
    left, top, width, height = region
    # with mss.mss() as sct:
    monitor = {"left": left, "top": top, "width": width, "height": height}
    return grab_image_by_dxgi(monitor)

def analyze_tension_color_percentage(region):
    """
    使用 HSV 分析拉力条颜色比例，返回 {green, yellow, red}
    """
    img = screenshot(region)
    if img is None:
        return None
    img_np = np.array(img)
    img_hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)

    h, s, v = cv2.split(img_hsv)
    total = h.size

    # 绿色范围（60-90°）
    green_mask = ((h >= 30) & (h <= 45) & (s >= 80) & (v >= 80))
    # 黄色范围（40-59°）
    yellow_mask = ((h >= 20) & (h <= 29) & (s >= 80) & (v >= 80))
    # 红色范围（0-15° 或 345-360°）
    red_mask = (((h <= 7) | (h >= 170)) & (s >= 80) & (v >= 80))

    green_ratio = np.count_nonzero(green_mask) / total
    yellow_ratio = np.count_nonzero(yellow_mask) / total
    red_ratio = np.count_nonzero(red_mask) / total

    return {
        'green': round(green_ratio, 3),
        'yellow': round(yellow_ratio, 3),
        'red': round(red_ratio, 3),
    }

# ------------------ 处理鱼的重量信息 ------------------
def parse_weight(text: str):
    """
    处理鱼的信息文字
    """
    #清除空格
    text = text.replace(' ', '')

    # 匹配重量部分：克 或 公斤
    pattern = r'(\d*\.?\d+)\s*(克|公斤)'
    weight_match = re.search(pattern, text)

    if not weight_match:
        return None

    # 转换成统一单位
    weight = float(weight_match.group(1))
    if weight_match.group(2) == '公斤':
        weight *= 1000  # 转成克

    return weight

# ------------------ 优化出线米数 ------------------
def get_cast_line_meters(s):
    """
    优化出线米数
    """
    #提取正好是三个相邻的数字
    # match = re.search(r'(?<!\d)\d{3}(?!\d)', s)
    # if s and len(s)>0:
    #     s = s[0].strip()
    #     if s.isdigit() and len(s) == 3:
    #         return int(s)
    # return None
    if s and len(s)>0:
        match = re.search(r'(?<!\d)\d{3}(?!\d)', s[0].strip())
        return int(match.group()) if match else None
    return None

# ------------------ 咖啡厅交任务 ------------------
# 配置参数
start_x = 451
start_y = 175
width = 262
height = 198
dx = 284  # 每列间距
dy = 224  # 每行间距
cols = 5  # 每行鱼数量

def get_fish_regions(count):
    """返回前 count 条鱼的区域坐标 (x, y, w, h)"""
    regions = []
    for i in range(count):
        row = i // cols
        col = i % cols
        x = start_x + dx * col
        y = start_y + dy * row
        regions.append((x, y, width, height))
    return regions

def ctrl_click_in_regions(regions):
    """在每个区域内 Ctrl+左键点击"""
    key_down('Left Ctrl')
    for region in regions:
        move_mouse_random_in_region(region)
        click_left_mouse()
        time.sleep(0.2)
    key_up('Left Ctrl')

#阻塞函数，需要自动续费船票
def renew_ticket_blocking():
     """
     目前有几种情况需要阻塞+保护：
     1.刚开始驶出码头的时候，操作比较多
     2.到达目的后需要走到船头的操作
     3.还有回坑时回到船上的时候，回坑后走向船头的操作
     4.切鱼前需要阻塞，回坑前也需要阻塞，
     """
     if config.is_need_renew_ticket:
        while not config.stop_event.is_set():
            if not config.is_need_renew_ticket:
                break
            time.sleep(random.uniform(0.5, 0.6))

# === 可中断睡眠 ===
def sleep_time(seconds, check_interval=0.05):
    """
    精准、可中断的睡眠函数，单位秒，支持热键打断。
    内部带有误差补偿机制，根据历史 sleep 偏差自动调整睡眠时长。
    """
    if not hasattr(sleep_time, "_error_history"):
        sleep_time._error_history = deque(maxlen=20)
        sleep_time._compensate = True  # 默认启用补偿

    def get_avg_error():
        history = sleep_time._error_history
        return sum(history) / len(history) if history else 0.0

    # 计算补偿后的睡眠时间
    correction = get_avg_error() if sleep_time._compensate else 0.0
    adjusted_seconds = max(0.01, seconds - correction)

    # 睡眠开始
    start_time = time.time()
    while True:
        if config.stop_event.is_set() or keyboard.is_pressed(config.STOP_HOTKEY):
            stop_program()
            break
        elapsed = time.time() - start_time
        if elapsed >= adjusted_seconds:
            break
        time.sleep(min(check_interval, adjusted_seconds - elapsed))

    # 睡眠结束，记录误差
    actual_sleep = time.time() - start_time
    actual_error = actual_sleep - seconds  # 与原始目标比较
    sleep_time._error_history.append(actual_error)

    # logger.debug(
    #     f"sleep_time({seconds:.2f}) ➤ 实际: {actual_sleep:.3f}s，误差: {actual_error:+.3f}s，"
    #     f"{'补偿' if sleep_time._compensate else '未补偿'}: {correction:+.3f}s"
    # )

# === 全局变量 ===
state_lock = threading.Lock()

# === 启动主程序 ===
def start_program(main_func):
    with state_lock:
        if not config.program_stopped:
            logger.warning("⚠️ 程序已经在运行，忽略启动请求。")
            return
        if config._stopping:
            logger.warning("⚠️ 程序正在停止中，无法启动。")
            return

        # 清理旧线程
        old_thread = config.named_threads.get("main_loop")
        if old_thread and old_thread.is_alive():
            logger.info("⏳ 等待旧主线程退出...")
            old_thread.join(timeout=5)
        config.named_threads.pop("main_loop", None)
   
        # 重置状态
        config.stop_event.clear()
        config.program_stopped = False
        config._stopping = False
        
        config.fps = get_refresh_rate()
        # logger.info(f"🎯 当前刷新率: {config.fps}Hz")
        # logger.info("✅ 程序开始运行")

    # 启动 OCR（可选）
    try:
        from ocr_global import ocr
        ocr.recognize_coordinate_once()
    except Exception as e:
        logger.exception("❌ OCR 初始化失败")
        config.program_stopped = True
        config.program_starting = False  # ✅ 取消启动中状态
        return

        # 启动主线程，注意传入包装过的函数
    def wrapped_main_func():
        logger.debug("🚀 主线程启动")
        config.program_starting = False  # ✅ 在真正开始时，关闭“启动中”状态
        logger.info("✅ 程序正在运行")
        main_func()  # 原本的逻辑

    thread = threading.Thread(target=wrapped_main_func, name="main_loop")
    thread.start()
    config.named_threads["main_loop"] = thread

# === 停止主程序 ===
def stop_program():
    with state_lock:
        if config._stopping:
            logger.debug("⚠️ 正在停止程序，忽略重复调用")
            return
        if config.program_stopped:
            logger.debug("⚠️ 程序已停止，无需再次停止")
            return
        config._stopping = True

    logger.info("🛑 正在停止程序")
    config.stop_event.set()

    # # 停 OCR 线程池
    # try:
    #     from ocr_global import ocr
    #     if ocr:
    #         ocr.shutdown()
    # except Exception as e:
    #     logger.exception(f"❌ OCR shutdown 异常: {e}")

    #清理按键
    cleanup_keys()    

    # 等待所有线程退出
    current_tid = threading.get_ident()
    for name, t in list(config.named_threads.items()):
        if not isinstance(t, threading.Thread) or not t.is_alive():
            continue
        if t.ident == current_tid:
            # logger.warning(f"⚠️ 当前线程 {name} 自己，跳过 join")
            continue
        # logger.info(f"⏳ 等待线程退出: {name}")
        t.join(timeout=5)
        # logger.info(f"✅ 线程已退出: {name}")
    config.named_threads.clear()

    with state_lock:
        config.program_stopped = True
        config._stopping = False
        logger.info("✅ 程序已完全停止")

#优化启动
def delayed_start():
    if config.open_lock_unlock_alone:
        from stages.set_friction_from_slider import set_friction_from_slider_alone
        logger.info(f"🎮 只启动点锁功能。")
        start_program(set_friction_from_slider_alone)
    else:
        if config.mode_type==1:
            if config.program_stopped:
                config.program_starting = True  # ✅ 正在启动
            import corestages_hand  # ⏱ 延迟导入
            start_program(corestages_hand.run_loop)
        elif config.mode_type==2:
            if config.program_stopped:
                config.program_starting = True  # ✅ 正在启动
            import corestages_bottom_lure  # ⏱ 延迟导入
            start_program(corestages_bottom_lure.run_loop)
        elif config.mode_type==3:
            if config.program_stopped:
                config.program_starting = True  # ✅ 正在启动
            import corestages  # ⏱ 延迟导入
            start_program(corestages.run_loop)    
        elif config.mode_type==4:
            if config.program_stopped:
                config.program_starting = True  # ✅ 正在启动
            import corestages_auto_click  # ⏱ 延迟导入
            start_program(corestages_auto_click.run_loop)
                

def start_daemon_thread(target_func, name=None,args=()):

    if name is None:
        name = f"worker_{target_func.__name__}"

    if name in config.named_threads:
        existing = config.named_threads[name]
        if existing.is_alive():
            logger.warning(f"⚠️ 已存在活跃线程 {name}，不重复启动")
            return

    thread = threading.Thread(target=target_func, name=name, args=args, daemon=True)
    config.named_threads[name] = thread
    thread.start()

#重启游戏
def restart_game():
    import subprocess

    # 检查rf4_x64.exe是否运行

    exe_name='rf4_x64.exe'

    check = subprocess.run(
        ["tasklist", "/fi", f"imagename eq {exe_name}"],
        capture_output=True,
        text=True
    )

    if exe_name.lower() in check.stdout.lower():
        logger.info(f"🔄 程序正在运行，准备关闭：{exe_name}")
        kill = subprocess.run(
            ["taskkill", "/im", exe_name, "/f"],
            capture_output=True,
            text=True
        )
        if kill.returncode == 0:
            logger.info(f"✅ 成功关闭程序：{exe_name}")
        else:
            logger.info(f"❌ 关闭程序失败：{exe_name}")
            logger.info(kill.stderr.strip())
            return
        # 等待进程完全退出
        sleep_time(random.uniform(5.23, 5.33))
    else:
        logger.info(f"ℹ️ 程序未在运行：{exe_name}，将直接启动")
    
    #检查RF4Launcher.exe是否运行
    if config.game_mode==2:

        exe_name='RF4Launcher.exe'

        check = subprocess.run(
        ["tasklist", "/fi", f"imagename eq {exe_name}"],
        capture_output=True,
        text=True
        )

        if exe_name.lower() in check.stdout.lower():
            logger.info(f"🔄 程序正在运行，准备关闭：{exe_name}")
            kill = subprocess.run(
                ["taskkill", "/im", exe_name, "/f"],
                capture_output=True,
                text=True
            )
            if kill.returncode == 0:
                logger.info(f"✅ 成功关闭程序：{exe_name}")
            else:
                logger.info(f"❌ 关闭程序失败：{exe_name}")
                logger.info(kill.stderr.strip())
                return
            # 等待进程完全退出
            sleep_time(random.uniform(5.23, 5.33))
        else:
            logger.info(f"ℹ️ 程序未在运行：{exe_name}，将直接启动")    

    exe_path=''
    if config.game_mode==1:
        exe_path=config.steam_path
    else:
        exe_path=config.standalone_path    

    # 启动程序
    if os.path.isfile(exe_path):
        try:
            # 启动游戏
            if config.game_mode==1:
                appid = "766570"
                subprocess.Popen([exe_path, f"steam://rungameid/{appid}"])
            else:    
                subprocess.Popen([exe_path])
                sleep_time(random.uniform(3.04, 3.56))
                move_mouse_random_in_region(region=config.StandaloneLoginMenuRegionClick)
                sleep_time(random.uniform(0.43, 0.535))
                click_left_mouse()
                
            logger.info(f"🚀 成功启动程序：{exe_path}")

            # 置顶窗口
            sleep_time(random.uniform(3.04,3.56))
            import win32gui
            hwnd = win32gui.FindWindow(None, config.TARGET_WINDOW_TITLE)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)              # 置于前台
            else:
                print(f"未找到标题为 '{config.TARGET_WINDOW_TITLE}' 的窗口")

            # 等待出现重新登录界面
            while not config.stop_event.is_set():
                steam_match = check_template_in_region(config.SteamLoginRegionScreenshot, template_path="steamlogin.png")
                standalone_match = check_template_in_region(config.StandaloneLoginRegionScreenshot, template_path="standalonelogin.png")
                fish_match = check_template_in_region(config.FishRegionScreenshot, "fish.png")
                login_error_match = check_template_in_region(config.LoginErrorRegionScreenshot, "loginerror.png")
                if fish_match or login_error_match:
                    break
                if steam_match:
                    logger.info("检测到Steam登录界面，准备重新登录。")
                    sleep_time(random.uniform(0.23, 0.235))
                    move_mouse_random_in_region(region=config.SteamLoginRegionClick)
                    sleep_time(random.uniform(0.23, 0.235))
                    click_left_mouse()
                    break
                if standalone_match:
                    logger.info("检测到独立登录界面，准备重新登录。")
                    sleep_time(random.uniform(0.23, 0.235))
                    move_mouse_random_in_region(region=config.StandaloneLoginRegionClick)
                    sleep_time(random.uniform(0.23, 0.24))
                    click_left_mouse()
                    break
                sleep_time(random.uniform(0.04, 0.06))

        except Exception as e:
            logger.info(f"❌ 启动失败：{e}")
    else:
        logger.info(f"❌ 文件不存在：{exe_path}")

#释放所有按键
def cleanup_keys():
    mouse_up_left()
    mouse_up_right()
    for key in ['w', 'a', 'd', 's','Left Shift','Left Ctrl','u','r']:
        key_up(key)
    for key in ['w', 'a', 'd', 'shift']:
        pyautogui.keyUp(key)

#自动更换坑位
def switch_to_next_auto_pit():
    if not config.auto_pits:
        return

    if not hasattr(config, "auto_pit_index"):
        config.auto_pit_index = 0

    total = len(config.auto_pits)
    attempts = 0

    while attempts < total:
        idx = config.auto_pit_index % total
        pit = config.auto_pits[idx]

        try:
            # 尝试转换为整数（长度可能不足 4 项）
            x = int(pit[0]) if len(pit) > 0 else 0
            y = int(pit[1]) if len(pit) > 1 else 0
            dist = int(pit[2]) if len(pit) > 2 else 0
            cast = int(pit[3]) if len(pit) > 3 else 0
        except Exception as e:
            logger.warning(f"⚠️ 坑位 {idx+1} 数据异常：{e}")
            config.auto_pit_index += 1
            attempts += 1
            continue

        if x > 0 and y > 0 and dist > 0:
            config.destination = (x, y)
            config.dist = dist
            config.cast_line_meters = cast  # ✅ cast 允许为 0

            logger.info(f"✅ 自动切换到坑位 {idx+1}：目的地=({x}, {y})，回坑距离={dist}，卡米数={cast}")
            config.auto_pit_index += 1
            return
        else:
            logger.warning(f"⚠️ 自动跳过无效坑位 {idx+1}: x={x}, y={y}, dist={dist}")
            config.auto_pit_index += 1
            attempts += 1

    logger.warning("❌ 没有找到可用的有效坑位。")
