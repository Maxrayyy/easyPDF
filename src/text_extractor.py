"""文本提取模块"""
import json
from pathlib import Path
from typing import List, Dict, Any

from .config import config
from .logger import logger
from .pdf_processor import PDFProcessor
from .layout_detector import LayoutDetector
from .ocr_engine import OCREngine


class TextExtractor:
    """文本提取器"""

    def __init__(self):
        """初始化文本提取器"""
        self.pdf_processor = PDFProcessor()
        self.layout_detector = LayoutDetector()
        self.ocr_engine = OCREngine()

    def extract_from_pdf(
        self,
        pdf_path: str,
        output_path: str,
        first_page: int = None,
        last_page: int = None,
        output_format: str = "txt",
        cleanup: bool = False
    ) -> Dict[str, Any]:
        """
        从 PDF 提取文本

        Args:
            pdf_path: PDF 文件路径
            output_path: 输出文件路径
            first_page: 起始页码
            last_page: 结束页码
            output_format: 输出格式 (txt, json, markdown)
            cleanup: 是否清理临时文件

        Returns:
            提取结果统计
        """
        # 设置默认值
        if first_page is None:
            first_page = config.get("processing.first_page", 1)
        if last_page is None:
            last_page = config.get("processing.last_page")

        # 转换 PDF 为图片
        image_infos = self.pdf_processor.pdf_to_images(
            pdf_path, first_page, last_page
        )

        # 提取每一页的文本
        all_pages_data = []
        total_regions = 0
        failed_pages = []

        for image_path, page_num in image_infos:
            logger.info(f"正在处理第 {page_num} 页...")

            try:
                page_data = self._extract_page(image_path, page_num)
                all_pages_data.append(page_data)
                total_regions += len(page_data["regions"])

            except Exception as e:
                logger.error(f"第 {page_num} 页处理失败: {e}")
                failed_pages.append(page_num)

        # 保存结果
        self._save_output(all_pages_data, output_path, output_format)

        # 清理临时文件
        if cleanup:
            self.pdf_processor.cleanup_images(config.temp_image_dir)

        # 返回统计
        stats = {
            "total_pages": len(image_infos),
            "success_pages": len(all_pages_data),
            "failed_pages": failed_pages,
            "total_regions": total_regions,
            "output_path": output_path
        }

        logger.info(f"提取完成: {stats['success_pages']}/{stats['total_pages']} 页")
        logger.info(f"输出文件: {output_path}")

        return stats

    def _extract_page(self, image_path: str, page_num: int) -> Dict[str, Any]:
        """
        提取单页文本

        Args:
            image_path: 图片路径
            page_num: 页码

        Returns:
            页面数据
        """
        # 加载图片
        image = self.pdf_processor.load_image(image_path)

        # 检测布局
        regions = self.layout_detector.detect(image_path)

        # 排序区域
        regions = self.layout_detector.sort_regions(regions)

        # OCR 识别每个区域
        page_texts = []
        for region in regions:
            text = self.ocr_engine.recognize_region(image, region["bbox"])
            if text:
                page_texts.append({
                    "text": text,
                    "bbox": region["bbox"],
                    "label": region["label"]
                })

        return {
            "page_num": page_num,
            "regions": page_texts
        }

    def _save_output(
        self,
        pages_data: List[Dict[str, Any]],
        output_path: str,
        output_format: str
    ):
        """
        保存提取结果

        Args:
            pages_data: 页面数据列表
            output_path: 输出路径
            output_format: 输出格式
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if output_format == "json":
            self._save_as_json(pages_data, output_file)
        elif output_format == "markdown":
            self._save_as_markdown(pages_data, output_file)
        else:
            self._save_as_txt(pages_data, output_file)

    def _save_as_txt(self, pages_data: List[Dict[str, Any]], output_file: Path):
        """保存为纯文本格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for page_data in pages_data:
                page_num = page_data["page_num"]

                # 页面分隔符
                if config.get("output.add_page_separator", True):
                    template = config.get("output.page_separator_template", "\n===== 第 {page_num} 页 =====\n")
                    f.write(template.format(page_num=page_num))

                # 写入文本
                for region in page_data["regions"]:
                    f.write(region["text"])
                    f.write("\n\n")

    def _save_as_json(self, pages_data: List[Dict[str, Any]], output_file: Path):
        """保存为 JSON 格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pages_data, f, ensure_ascii=False, indent=2)

    def _save_as_markdown(self, pages_data: List[Dict[str, Any]], output_file: Path):
        """保存为 Markdown 格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for page_data in pages_data:
                page_num = page_data["page_num"]

                # 页面标题
                f.write(f"## 第 {page_num} 页\n\n")

                # 写入文本
                for region in page_data["regions"]:
                    label = region["label"]
                    text = region["text"]

                    if label == "paragraph_title":
                        f.write(f"### {text}\n\n")
                    else:
                        f.write(f"{text}\n\n")
