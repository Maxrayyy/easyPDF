# 模型文件目录

## 📦 所需模型

请将以下 3 个 PaddlePaddle 模型放到此目录：

1. **PP-DocLayout_plus-L_infer** - 文档布局检测模型
2. **PP-OCRv5_server_det_infer** - OCR 检测模型
3. **PP-OCRv5_server_rec_infer** - OCR 识别模型

## 📁 目录结构

```
models/
├── PP-DocLayout_plus-L_infer/
│   ├── inference.pdiparams
│   ├── inference.pdiparams.info
│   └── inference.pdmodel
├── PP-OCRv5_server_det_infer/
│   ├── inference.pdiparams
│   ├── inference.pdiparams.info
│   └── inference.pdmodel
└── PP-OCRv5_server_rec_infer/
    ├── inference.pdiparams
    ├── inference.pdiparams.info
    ├── inference.pdmodel
    └── rec_char_dict.txt
```

## 🔧 设置方法

### 方法 1: 复制或移动模型到此目录

```bash
# 复制模型
cp -r /path/to/PP-DocLayout_plus-L_infer ./models/
cp -r /path/to/PP-OCRv5_server_det_infer ./models/
cp -r /path/to/PP-OCRv5_server_rec_infer ./models/

# 或移动模型
mv /path/to/PP-DocLayout_plus-L_infer ./models/
mv /path/to/PP-OCRv5_server_det_infer ./models/
mv /path/to/PP-OCRv5_server_rec_infer ./models/
```

### 方法 2: 创建符号链接（推荐，节省空间）

```bash
cd models
ln -s /path/to/PP-DocLayout_plus-L_infer ./
ln -s /path/to/PP-OCRv5_server_det_infer ./
ln -s /path/to/PP-OCRv5_server_rec_infer ./
```

### 方法 3: 使用绝对路径

在 `config/settings.yaml` 中直接配置绝对路径：

```yaml
models:
  layout_model_dir: "/absolute/path/to/PP-DocLayout_plus-L_infer"
  ocr_det_model_dir: "/absolute/path/to/PP-OCRv5_server_det_infer"
  ocr_rec_model_dir: "/absolute/path/to/PP-OCRv5_server_rec_infer"
```

## 📥 下载模型

如果你还没有这些模型，可以通过以下方式下载：

### 方法 1: 使用 Python 脚本自动下载（推荐）

创建并运行以下脚本：

```python
# download_models.py
import os
from paddlex import create_model
from paddleocr import PaddleOCR

os.makedirs("models", exist_ok=True)

# 下载布局检测模型
print("正在下载布局检测模型...")
layout_model = create_model("PP-DocLayout_plus-L")
print("布局模型下载完成！")

# 下载 OCR 模型
print("正在下载 OCR 模型...")
ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_server_det",
    text_recognition_model_name="PP-OCRv5_server_rec"
)
print("OCR 模型下载完成！")

print("\n模型已下载到缓存目录")
print("请从缓存目录复制到项目 models/ 目录，或使用绝对路径配置")
```

运行脚本：
```bash
python download_models.py
```

模型会下载到 PaddlePaddle 的缓存目录（通常是 `~/.paddlex/` 或 `~/.paddleocr/`）。

### 方法 2: 使用 wget 直接下载

```bash
cd models

# 下载布局检测模型（约 200 MB）
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0b2/PP-DocLayout_plus-L_infer.tar
tar -xf PP-DocLayout_plus-L_infer.tar
rm PP-DocLayout_plus-L_infer.tar

# 下载 OCR 检测模型（约 100 MB）
wget https://paddleocr.bj.bcebos.com/PP-OCRv5/chinese/PP-OCRv5_server_det_infer.tar
tar -xf PP-OCRv5_server_det_infer.tar
rm PP-OCRv5_server_det_infer.tar

# 下载 OCR 识别模型（约 120 MB）
wget https://paddleocr.bj.bcebos.com/PP-OCRv5/chinese/PP-OCRv5_server_rec_infer.tar
tar -xf PP-OCRv5_server_rec_infer.tar
rm PP-OCRv5_server_rec_infer.tar
```

### 方法 3: 从百度网盘下载

访问 PaddleOCR 官方模型库获取网盘链接：
- [PaddleOCR 模型列表](https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_ch/models_list.md)
- [PaddleX 模型库](https://github.com/PaddlePaddle/PaddleX)

### 方法 4: 首次运行时自动下载

直接运行程序，PaddleX 和 PaddleOCR 会自动下载模型到缓存目录：

```bash
python run.py --pdf pdfs/your.pdf
```

然后从缓存目录找到模型并复制到 `models/` 目录。

缓存目录位置：
- Linux/Mac: `~/.paddlex/` 和 `~/.paddleocr/`
- Windows: `C:\Users\YourName\.paddlex\` 和 `C:\Users\YourName\.paddleocr\`

## 📝 注意事项

- 模型文件较大（共约 200-500 MB），已添加到 `.gitignore`
- 使用符号链接可以避免重复占用磁盘空间
- 确保模型目录结构正确，否则会报错
