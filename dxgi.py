import ctypes
import os
import sys
import threading
from ctypes import *
import numpy as np
from logger import logger  # 新增导入日志模块

def get_resource_path(relative_path):
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

# 加载 DLL
dll_path = get_resource_path("Dll1.dll")
dxgi = ctypes.CDLL(dll_path)

# dll_path = os.path.abspath("Dll1.dll")
# dxgi = ctypes.WinDLL(dll_path)

# 函数签名定义
dxgi.InitDuplicator.restype = c_bool
dxgi.FreeDuplicator.restype = None

dxgi.GetDesktopFrameRegion.argtypes = [
    c_int, c_int, c_int, c_int,
    POINTER(POINTER(c_uint8)),
    POINTER(c_int), POINTER(c_int), POINTER(c_int),
    c_int  
]

dxgi.GetDesktopFrameRegion.restype = c_bool

dxgi.FreeBuffer.argtypes = [POINTER(c_uint8)]
dxgi.FreeBuffer.restype = None

# 加锁，确保线程安全
dxgi_lock = threading.Lock()

# 初始化 DXGI
if not dxgi.InitDuplicator():
    logger.error("初始化 DXGI 失败")
    exit(1)

# 封装截图结果
class DXGIScreenshot:
    def __init__(self, width, height, stride, pixels):
        self.width = width
        self.height = height
        self.stride = stride
        self.pixels = pixels

    def __array__(self, dtype=None):
        arr = np.frombuffer(self.pixels, dtype=np.uint8)
        arr = arr[:self.height * self.stride]
        arr = arr.reshape((self.height, self.stride // 4, 4))
        arr = arr[:, :self.width, :]  # 截取有效宽度
        return arr

# 线程安全截图函数
def grab_region(region: dict, timeout_ms=0):
    required_keys = {"left", "top", "width", "height"}
    if not isinstance(region, dict) or not required_keys.issubset(region.keys()):
        raise ValueError("region must be a dict with keys: 'left', 'top', 'width', 'height'")

    left = int(region["left"])
    top = int(region["top"])
    width = int(region["width"])
    height = int(region["height"])

    buffer_ptr = POINTER(c_uint8)()
    stride = c_int()
    out_width = c_int()
    out_height = c_int()

    with dxgi_lock:
        success = dxgi.GetDesktopFrameRegion(
            left, top, width, height,
            byref(buffer_ptr), byref(stride),
            byref(out_width), byref(out_height),
            timeout_ms
        )

        if not success or not buffer_ptr:
            return None

        size_bytes = stride.value * out_height.value
        raw_data = ctypes.string_at(buffer_ptr, size_bytes)
        dxgi.FreeBuffer(buffer_ptr)

    return DXGIScreenshot(out_width.value, out_height.value, stride.value, raw_data)

