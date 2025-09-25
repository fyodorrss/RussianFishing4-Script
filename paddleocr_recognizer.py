import os
import sys
import threading
import cv2
import numpy as np
import re
from typing import Optional, Tuple, List
from paddleocr import PaddleOCR
import dxgi
from logger import logger

def get_resource_path(relative_path):
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

class PaddleocrRecognizer:
    def __init__(self, region: Tuple[int, int, int, int]):
        """
        初始化坐标识别器
        region: (left, top, width, height)
        """
        self.region = region

        self.ocr = PaddleOCR(
        use_doc_orientation_classify=False, 
        use_doc_unwarping=False, 
        use_textline_orientation=False,
        text_detection_model_name="PP-OCRv5_mobile_det",
        text_recognition_model_name="PP-OCRv5_mobile_rec",
        cpu_threads	=1,
        text_detection_model_dir=get_resource_path("./weights/PP-OCRv5_mobile_det"),
        text_recognition_model_dir=get_resource_path("./weights/PP-OCRv5_mobile_rec"),
        # text_detection_model_dir=get_resource_path("./weights/PP-OCRv5_server_det"),
        # text_recognition_model_dir=get_resource_path("./weights/PP-OCRv5_server_rec"),
        # enable_mkldnn=False
        )
        
        self.coord_pattern = re.compile(r'(\d+)\s*[:：]\s*(\d+)')  # 支持 123:456、123：456

        self.lock = threading.Lock()

        # 日志
        self.logger =logger

    def safe_ocr(self, image):
        with self.lock:
            return self.ocr.predict(image)

    def parse_coordinate(self, text: str) -> Optional[Tuple[int, int]]:
        """
        尝试解析坐标格式 X:Y，允许识别错误导致的 X.Y 或 X：Y。
        先去掉空格再匹配，仅支持纯坐标格式。
        """
        coord_pattern = re.compile(r'^(\d+)[.:：](\d+)$')
        text = text.replace(' ', '')  # 去除所有空格
        match = coord_pattern.match(text)
        if match:
            try:
                x = int(match.group(1))
                y = int(match.group(2))
                return x, y
            except ValueError:
                self.logger.debug(f"坐标数字转换失败: {text}")
                return None
        else:
            self.logger.debug(f"不匹配坐标格式: {text}")
            return None

    def screenshot(self, region: Optional[dict] = None, fill_black: bool = False, is_preprocess=False,scale = 2.0):
      
        # 1. 获取截图区域
        if region is None:
            left, top, width, height = self.region
        else:
            left, top, width, height = region["left"], region["top"], region["width"], region["height"]

        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = dxgi.grab_region(monitor)
        img_cv = np.array(sct_img)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGRA2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        base_dir = os.path.dirname(os.path.abspath(__file__))

        if fill_black:
            template_names = ["info_icon1.png", "info_icon2.png"]
            threshold = 0.85
            matched_areas = []

            for template_name in template_names:
                full_path = os.path.join(base_dir, "images", template_name)
                if not os.path.exists(full_path):
                    self.logger.warning(f"[警告] 模板文件不存在: {full_path}")
                    continue

                template = cv2.imread(full_path, 0)
                if template is None:
                    self.logger.warning(f"[跳过] 无法读取模板图像: {full_path}")
                    continue

                w, h = template.shape[::-1]
                result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(result >= threshold)

                for pt in zip(*loc[::-1]):
                    if any(abs(pt[0] - x) < w and abs(pt[1] - y) < h for (x, y) in matched_areas):
                        continue
                    matched_areas.append(pt)

                    # # 涂黑
                    # cv2.rectangle(img_cv, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), -1)

                    # 用周围颜色填充（原实现）
                    roi = img_cv[pt[1]:pt[1]+h, pt[0]:pt[0]+w]
                    mean_color = cv2.mean(roi)[:3]
                    fill_color = tuple(map(int, mean_color))
                    cv2.rectangle(img_cv, pt, (pt[0] + w, pt[1] + h), fill_color, -1)

                    self.logger.debug(f"[遮挡] 使用模板 {template_name} 遮挡图标 at: {pt}")

            if matched_areas:
                self.logger.debug(f"[遮挡] 共遮挡 {len(matched_areas)} 个图标区域")
            else:
                self.logger.debug(f"[遮挡] 未发现需要遮挡的图标")

        # 放大
        img_cv = cv2.resize(img_cv, (int(img_cv.shape[1] * scale), int(img_cv.shape[0] * scale)), interpolation=cv2.INTER_LANCZOS4)
        
        if is_preprocess:
            # 预处理
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # binary = cv2.dilate(binary, np.ones((2, 2), np.uint8), iterations=1)
            img_cv = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        # # 保存调试图像
        # debug_dir = os.path.join(base_dir, "debug_images")
        # os.makedirs(debug_dir, exist_ok=True)
        # # 时间戳精确到微秒，避免同一秒内覆盖
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        # debug_path = os.path.join(debug_dir, f"processed_{timestamp}.png")
        # if cv2.imwrite(debug_path, img_cv):
        #     self.logger.info(f"[调试] 已保存处理图像: {debug_path}")
        # else:
        #     self.logger.error(f"[调试] 保存图像失败: {debug_path}")

        return img_cv
    
    def recognize_text_from_black_bg(self, region: dict, min_confidence: float = 0.8, fill_black: bool = False, is_preprocess=False,scale = 2.0) -> List[str]:
        """
        识别黑底白字区域的所有文本（中英文数字混合），放大两倍并保存截图。
        :param region: 截图区域 dict，例如 {"left": 100, "top": 200, "width": 300, "height": 100}
        :param min_confidence: 最小置信度过滤阈值
        :return: 文本列表
        """
        try:
            processed = self.screenshot(region=region, fill_black=fill_black, is_preprocess=is_preprocess,scale=scale)

            if processed is None or processed.size == 0:
                self.logger.warning("截图为空")
                return []

            # OCR 识别（支持中英文数字）
            try:
                results = self.safe_ocr(processed)
            except Exception as e:
                self.logger.error(f"OCR 执行失败，跳过本次识别: {e}")
                return []

            if not results:
                self.logger.info("未识别出任何文本")
                return []

            # 提取文本
            texts = []
            for item in results:
                rec_texts = item.get("rec_texts", [])
                rec_scores = item.get("rec_scores", [])
                for text, conf in zip(rec_texts, rec_scores):
                    # self.logger.info(f"[识别] 文本: '{text}', 置信度: {conf:.2f}")
                    if conf >= min_confidence:
                        texts.append(text)

            return texts

        except Exception:
            self.logger.exception("识别黑底白字文本失败")
            return []

    def recognize_text_from_black_bg_first(self, region: dict, min_confidence: float = 0.8, fill_black: bool = False, is_preprocess=False, scale = 2.0) -> Optional[str]:
        """
        黑底白字识别：返回置信度最高的文本（满足 min_confidence），失败返回 None
        :param region: 截图区域 dict，例如 {"left": 100, "top": 200, "width": 300, "height": 100}
        :param min_confidence: 最低置信度阈值
        :return: 最佳文本字符串 或 None
        """
        try:
            processed = self.screenshot(region=region, fill_black=fill_black, is_preprocess=is_preprocess,scale=scale)

            if processed is None or processed.size == 0:
                self.logger.warning("截图为空")
                return ''

            # OCR 识别
            try:
                results = self.safe_ocr(processed)
            except Exception as e:
                self.logger.error(f"OCR 执行失败，跳过本次识别: {e}")
                return None

            if not results:
                self.logger.info("未识别出任何文本")
                return ''
            # 筛选置信度最高的文本
            best_text = ''
            best_conf = 0.0
            for item in results:
                rec_texts = item.get("rec_texts", [])
                rec_scores = item.get("rec_scores", [])
                for text, conf in zip(rec_texts, rec_scores):
                    # self.logger.info(f"[识别] 文本: '{text}', 置信度: {conf:.2f}")
                    if conf >= min_confidence and conf > best_conf:
                        best_conf = conf
                        best_text = text

            return best_text if best_text else ''

        except Exception:
            self.logger.exception("识别黑底文本（单条）失败")
            return ''
    
    def recognize_coordinate_once(self, min_confidence: float = 0.8) -> Optional[List[int]]:
        """执行一次坐标识别，返回 [X, Y] 或 None（置信度仅用于打印）"""
        try:
            image = self.screenshot()
            if image is None:
                self.logger.warning("❌ 截图返回 None")
                return None
            if not isinstance(image, np.ndarray):
                self.logger.error(f"❌ 截图返回非 ndarray 类型: {type(image)}")
                return None
            if image.size == 0:
                self.logger.warning("❌ 截图内容为空（size == 0）")
                return None

            try:
                results = self.safe_ocr(image)
            except Exception as e:
                self.logger.error(f"OCR 执行失败，跳过本次识别: {e}", exc_info=True)
                return None

            if not results:
                return None

            coords = []
            confs = []

            for item in results:
                rec_texts = item.get("rec_texts", [])
                rec_scores = item.get("rec_scores", [])
                for text, conf in zip(rec_texts, rec_scores):
                    parsed = self.parse_coordinate(text)
                    if parsed:
                        coords.append(parsed)
                        confs.append(conf)

            if not coords:
                return None

            # 选择置信度最高的坐标
            best_index = confs.index(max(confs))
            best_coord = coords[best_index]
            best_conf = confs[best_index]

            if best_conf > min_confidence:
                return [best_coord[0], best_coord[1]]
            else:
                self.logger.info(f"坐标置信度 {best_conf:.2f} 低于阈值 {min_confidence}")
                return None

        except Exception:
            self.logger.exception("🔥 recognize_coordinate_once 整体异常（可能非 OCR 内部问题）")
            return None
