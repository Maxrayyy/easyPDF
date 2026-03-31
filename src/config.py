"""配置管理模块"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """配置管理类"""

    def __init__(self, config_path: str = None):
        """
        初始化配置

        Args:
            config_path: 配置文件路径，默认使用项目根目录下的 config/settings.yaml
        """
        if config_path is None:
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "settings.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.project_root = Path(__file__).parent.parent

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get(self, key_path: str, default=None):
        """
        获取配置值

        Args:
            key_path: 配置键路径，如 "models.layout_model_dir"
            default: 默认值

        Returns:
            配置值
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def resolve_path(self, path: str) -> Path:
        """
        解析路径，如果是相对路径则相对于项目根目录

        Args:
            path: 路径字符串

        Returns:
            Path 对象
        """
        path = Path(path)
        if path.is_absolute():
            return path
        else:
            return self.project_root / path

    @property
    def layout_model_dir(self) -> str:
        return self.get("models.layout_model_dir")

    @property
    def ocr_det_model_dir(self) -> str:
        return self.get("models.ocr_det_model_dir")

    @property
    def ocr_rec_model_dir(self) -> str:
        return self.get("models.ocr_rec_model_dir")

    @property
    def default_pdf(self) -> str:
        return self.get("paths.default_pdf")

    @property
    def output_dir(self) -> Path:
        return self.resolve_path(self.get("paths.output_dir"))

    @property
    def temp_image_dir(self) -> Path:
        return self.resolve_path(self.get("paths.temp_image_dir"))


# 全局配置实例
config = Config()
