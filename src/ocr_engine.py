"""OCR 识别模块"""
import cv2
import numpy as np
from typing import List, Optional
from paddleocr import PaddleOCR

from .config import config
from .logger import logger


class OCREngine:
    """OCR 识别引擎"""

    def __init__(self):
        """初始化 OCR 模型"""
        logger.info("正在加载 OCR 模型...")

        ocr_config = config.get("ocr", {})
        self.model = PaddleOCR(
            enable_mkldnn=ocr_config.get("enable_mkldnn", False),
            cpu_threads=ocr_config.get("cpu_threads", 2),
            use_doc_orientation_classify=ocr_config.get("use_doc_orientation_classify", False),
            use_doc_unwarping=ocr_config.get("use_doc_unwarping", False),
            use_textline_orientation=ocr_config.get("use_textline_orientation", False),
            text_detection_model_name="PP-OCRv5_server_det",
            text_recognition_model_name="PP-OCRv5_server_rec",
            text_detection_model_dir=config.ocr_det_model_dir,
            text_recognition_model_dir=config.ocr_rec_model_dir,
        )

        self.max_width = config.get("processing.max_crop_width", 2000)
        logger.info("OCR 模型加载完成")

    def recognize_region(self, image: np.ndarray, bbox: List[int]) -> str:
        """
        识别图片中指定区域的文字

        Args:
            image: 输入图片 (numpy array)
            bbox: 边界框 [x1, y1, x2, y2]

        Returns:
            识别出的文本
        """
        x1, y1, x2, y2 = bbox

        # 裁剪区域
        crop = image[y1:y2, x1:x2]
        if crop.size == 0:
            return ""

        # 缩放过大的图片
        h, w = crop.shape[:2]
        if w > self.max_width:
            scale = self.max_width / w
            new_w = int(w * scale)
            new_h = int(h * scale)
            crop = cv2.resize(crop, (new_w, new_h))
            logger.debug(f"区域缩放: {w}x{h} -> {new_w}x{new_h}")

        # OCR 识别
        try:
            ocr_result = self.model.predict(crop)
            if ocr_result and len(ocr_result) > 0 and "rec_texts" in ocr_result[0]:
                texts = ocr_result[0]["rec_texts"]
                recognized_text = "".join(t.strip() for t in texts)
                return recognized_text
            else:
                return ""

        except Exception as e:
            logger.error(f"OCR 识别失败: {e}")
            return ""

    def recognize_image(self, image_path: str) -> List[str]:
        """
        识别整张图片的文字

        Args:
            image_path: 图片路径

        Returns:
            识别出的文本行列表
        """
        try:
            result = self.model.ocr(image_path, cls=False)
            if not result or not result[0]:
                return []

            texts = []
            for line in result[0]:
                if len(line) >= 2:
                    text = line[1][0] if isinstance(line[1], tuple) else line[1]
                    if text:
                        texts.append(text.strip())

            return texts

        except Exception as e:
            logger.error(f"图片 OCR 失败 {image_path}: {e}")
            return []
