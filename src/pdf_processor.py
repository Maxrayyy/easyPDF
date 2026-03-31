"""PDF 处理模块"""
import cv2
from pathlib import Path
from typing import List, Tuple
from pdf2image import convert_from_path

from .config import config
from .logger import logger


class PDFProcessor:
    """PDF 处理器"""

    def __init__(self):
        """初始化 PDF 处理器"""
        self.temp_dir = config.temp_image_dir
        self.dpi = config.get("processing.dpi", 300)

    def pdf_to_images(
        self,
        pdf_path: str,
        first_page: int = None,
        last_page: int = None,
        output_dir: str = None
    ) -> List[Tuple[str, int]]:
        """
        将 PDF 转换为图片

        Args:
            pdf_path: PDF 文件路径
            first_page: 起始页码（从 1 开始）
            last_page: 结束页码
            output_dir: 输出目录，默认使用配置中的临时目录

        Returns:
            图片路径和页码的列表 [(image_path, page_num), ...]
        """
        if output_dir is None:
            output_dir = self.temp_dir

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"正在转换 PDF: {pdf_path}")
        logger.info(f"页码范围: {first_page} - {last_page}")
        logger.info(f"输出目录: {output_path}")

        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=first_page,
                last_page=last_page
            )

            image_infos = []
            for i, img in enumerate(images):
                page_num = (first_page or 1) + i
                image_path = output_path / f"page_{page_num}.png"
                img.save(str(image_path), "PNG")
                image_infos.append((str(image_path), page_num))
                logger.debug(f"已保存: {image_path}")

            logger.info(f"成功转换 {len(images)} 页")
            return image_infos

        except Exception as e:
            logger.error(f"PDF 转换失败: {e}")
            raise

    @staticmethod
    def load_image(image_path: str):
        """
        加载图片

        Args:
            image_path: 图片路径

        Returns:
            图片数组 (numpy.ndarray)
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"无法加载图片: {image_path}")
        return image

    @staticmethod
    def cleanup_images(image_dir: str):
        """
        清理临时图片

        Args:
            image_dir: 图片目录
        """
        try:
            image_path = Path(image_dir)
            if image_path.exists():
                for img_file in image_path.glob("*.png"):
                    img_file.unlink()
                logger.info(f"已清理临时图片: {image_dir}")
        except Exception as e:
            logger.warning(f"清理图片失败: {e}")
