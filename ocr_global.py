import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"


import threading
from concurrent.futures import ThreadPoolExecutor
from paddleocr_recognizer import PaddleocrRecognizer

DEFAULT_REGION = (1754, 975, 78, 28)
MAX_WORKERS = 4

class OCRManager:
    def __init__(self, max_workers=MAX_WORKERS, default_region=DEFAULT_REGION):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._thread_local = threading.local()
        self._default_region = default_region

    def _init_recognizer(self):
        if not hasattr(self._thread_local, "recognizer"):
            # logger.info(f"[Thread-{threading.get_ident()}] 创建新的 PaddleocrRecognizer 实例")
            self._thread_local.recognizer = PaddleocrRecognizer(
                region=self._default_region
            )
        return self._thread_local.recognizer

    def _run_in_thread(self, func, *args, **kwargs):
        """
        将方法调用提交到线程池执行，确保调用的 PaddleocrRecognizer 来自当前线程缓存
        """
        def task():
            recognizer = self._init_recognizer()
            method = getattr(recognizer, func)
            return method(*args, **kwargs)

        future = self._executor.submit(task)
        return future.result()

    def __getattr__(self, name):
        """
        代理调用 PaddleocrRecognizer 的方法，并自动提交线程池执行
        """
        def method(*args, **kwargs):
            return self._run_in_thread(name, *args, **kwargs)
        return method

    def shutdown(self):
        self._executor.shutdown(wait=True)



ocr = None

def recreate_ocr_manager():
    global ocr
    ocr = OCRManager()

# 全局单例对象，直接调用它的方法即可线程池安全执行
ocr = OCRManager()
