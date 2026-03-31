"""easyPDF - PDF 文本提取工具"""

__version__ = "1.0.0"
__author__ = "easyPDF Team"

from .text_extractor import TextExtractor
from .config import config

__all__ = ["TextExtractor", "config"]
