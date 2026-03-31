#!/usr/bin/env python3
"""模型下载脚本

自动下载 easyPDF 所需的 PaddlePaddle 模型
"""
import os
import sys
from pathlib import Path

print("=" * 60)
print("easyPDF 模型下载脚本")
print("=" * 60)
print("\n正在下载所需模型，这可能需要几分钟...")
print("模型总大小约 400-500 MB\n")

try:
    # 导入 PaddleX
    print("1/2 正在下载布局检测模型 (PP-DocLayout_plus-L)...")
    from paddlex import create_model
    layout_model = create_model("PP-DocLayout_plus-L", device="cpu")
    print("✓ 布局检测模型下载完成\n")

except Exception as e:
    print(f"✗ 布局检测模型下载失败: {e}\n")
    print("请检查网络连接或手动下载模型")
    sys.exit(1)

try:
    # 导入 PaddleOCR
    print("2/2 正在下载 OCR 模型 (PP-OCRv5)...")
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(
        text_detection_model_name="PP-OCRv5_server_det",
        text_recognition_model_name="PP-OCRv5_server_rec",
        enable_mkldnn=False,
        cpu_threads=2,
    )
    print("✓ OCR 模型下载完成\n")

except Exception as e:
    print(f"✗ OCR 模型下载失败: {e}\n")
    print("请检查网络连接或手动下载模型")
    sys.exit(1)

print("=" * 60)
print("✅ 所有模型下载完成！")
print("=" * 60)

# 提示模型位置
print("\n📍 模型已下载到 PaddlePaddle 缓存目录：")
home = Path.home()
print(f"  - 布局模型: {home}/.paddlex/")
print(f"  - OCR 模型: {home}/.paddleocr/")

print("\n📝 后续步骤：")
print("  1. 从缓存目录复制模型到项目 models/ 目录")
print("  2. 或在 config/settings.yaml 中配置缓存目录的绝对路径")
print("  3. 或直接运行程序，会自动使用缓存中的模型")

print("\n💡 推荐做法（创建符号链接）：")
print("  cd models")
print(f"  ln -s {home}/.paddlex/PP-DocLayout_plus-L_infer ./")
print(f"  ln -s {home}/.paddleocr/PP-OCRv5_server_det_infer ./")
print(f"  ln -s {home}/.paddleocr/PP-OCRv5_server_rec_infer ./")

print("\n🚀 现在可以运行：")
print("  python run.py --pdf pdfs/your.pdf")
print()
