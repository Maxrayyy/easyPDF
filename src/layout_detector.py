"""布局检测模块"""
import os
from typing import List, Dict, Any
from paddlex import create_model

from .config import config
from .logger import logger


class LayoutDetector:
    """布局检测器"""

    def __init__(self):
        """初始化布局检测模型"""
        os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"

        logger.info("正在加载布局检测模型...")
        self.model = create_model(
            model_name="PP-DocLayout_plus-L",
            model_dir=config.layout_model_dir,
            device=config.get("processing.device", "cpu")
        )
        logger.info("布局检测模型加载完成")

        self.target_labels = config.get("layout.target_labels", ["text", "paragraph_title"])

    def detect(self, image_path: str) -> List[Dict[str, Any]]:
        """
        检测图片中的布局区域

        Args:
            image_path: 图片路径

        Returns:
            检测到的文本区域列表，每个区域包含 bbox 和 label
        """
        try:
            layout_result = list(self.model.predict(image_path))
            if not layout_result:
                logger.warning(f"未检测到布局: {image_path}")
                return []

            result0 = layout_result[0]

            # 兼容不同版本的输出格式
            if "pred" in result0 and "boxes" in result0["pred"]:
                boxes = result0["pred"]["boxes"]
            else:
                boxes = result0.get("boxes", [])

            # 过滤目标区域
            text_regions = []
            for box in boxes:
                label = box.get("label", "")
                if label in self.target_labels:
                    x1, y1, x2, y2 = map(int, box["coordinate"])
                    text_regions.append({
                        "bbox": [x1, y1, x2, y2],
                        "label": label,
                        "score": box.get("score", 1.0)
                    })

            logger.debug(f"检测到 {len(text_regions)} 个文本区域")
            return text_regions

        except Exception as e:
            logger.error(f"布局检测失败 {image_path}: {e}")
            return []

    @staticmethod
    def sort_regions(regions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        对区域按阅读顺序排序（从上到下，从左到右）

        Args:
            regions: 区域列表

        Returns:
            排序后的区域列表
        """
        return sorted(
            regions,
            key=lambda r: (
                (r["bbox"][1] + r["bbox"][3]) / 2,  # y 中心
                r["bbox"][0]                          # x 起始
            )
        )
