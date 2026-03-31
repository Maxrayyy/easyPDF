# easyPDF

PDF 文本提取工具 - 基于 PaddleX Layout Detection + PaddleOCR

## 功能特性

- ✅ **布局检测**: 使用 PP-DocLayout_plus-L 精确识别文本区域
- ✅ **OCR 识别**: 使用 PP-OCRv5 高精度文字识别
- ✅ **多种输出格式**: 支持 txt、json、markdown 格式
- ✅ **灵活配置**: YAML 配置文件，便于自定义
- ✅ **模块化设计**: 代码结构清晰，易于扩展
- ✅ **日志记录**: 完整的日志系统，便于调试

## 项目结构

```
easyPDF/
├── config/
│   └── settings.yaml          # 配置文件
├── src/
│   ├── __init__.py
│   ├── config.py              # 配置管理
│   ├── logger.py              # 日志模块
│   ├── pdf_processor.py       # PDF 处理
│   ├── layout_detector.py     # 布局检测
│   ├── ocr_engine.py          # OCR 引擎
│   ├── text_extractor.py      # 文本提取
│   └── main.py                # 主入口
├── models/                    # 模型文件（用户自己配置）
│   └── README.md              # 模型设置说明
├── pdfs/                      # PDF 文件（用户自己添加）
│   └── README.md              # PDF 目录说明
├── data/
│   ├── txt/                   # 输出文本
│   └── figures/pages/         # 临时图片
├── requirements.txt           # 依赖包
├── run.py                     # 启动脚本
└── README.md
```

## 安装

### 1. 克隆项目

```bash
git clone <https://github.com/Maxrayyy/easyPDF.git>
cd easyPDF
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 下载模型

#### 快速下载（推荐）

```bash
python download_models.py
```

模型会自动下载到 PaddlePaddle 缓存目录。

#### 手动下载

使用 wget 下载（详见 [models/README.md](models/README.md)）：

```bash
cd models

# 布局检测模型
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0b2/PP-DocLayout_plus-L_infer.tar
tar -xf PP-DocLayout_plus-L_infer.tar && rm PP-DocLayout_plus-L_infer.tar

# OCR 检测模型
wget https://paddleocr.bj.bcebos.com/PP-OCRv5/chinese/PP-OCRv5_server_det_infer.tar
tar -xf PP-OCRv5_server_det_infer.tar && rm PP-OCRv5_server_det_infer.tar

# OCR 识别模型
wget https://paddleocr.bj.bcebos.com/PP-OCRv5/chinese/PP-OCRv5_server_rec_infer.tar
tar -xf PP-OCRv5_server_rec_infer.tar && rm PP-OCRv5_server_rec_infer.tar
```

### 4. 添加 PDF

将 PDF 文件放到 `pdfs/` 目录：

```bash
cp /path/to/your.pdf pdfs/
# 或创建符号链接
ln -s /path/to/your.pdf pdfs/
```

详见 [pdfs/README.md](pdfs/README.md)

## 使用方法

### 基本用法

```bash
python run.py --pdf /path/to/your.pdf
```

### 指定页码范围

```bash
python run.py --pdf /path/to/your.pdf --first-page 10 --last-page 20
```

### 指定输出格式

```bash
# 输出为文本
python run.py --pdf input.pdf --output output.txt --format txt

# 输出为 JSON
python run.py --pdf input.pdf --output output.json --format json

# 输出为 Markdown
python run.py --pdf input.pdf --output output.md --format markdown
```

### 清理临时文件

```bash
python run.py --pdf input.pdf --cleanup
```

### 详细日志

```bash
python run.py --pdf input.pdf --verbose
```

### 保存日志到文件

```bash
python run.py --pdf input.pdf --log-file process.log
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--pdf` | PDF 文件路径 | 配置文件中的默认值 |
| `--output` | 输出文件路径 | `data/txt/output.txt` |
| `--first-page` | 起始页码 | 配置文件中的默认值 |
| `--last-page` | 结束页码 | 配置文件中的默认值 |
| `--format` | 输出格式 (txt/json/markdown) | `txt` |
| `--cleanup` | 处理后清理临时文件 | `False` |
| `--verbose` | 显示详细日志 | `False` |
| `--log-file` | 日志文件路径 | 无（仅控制台输出） |

## 配置说明

编辑 `config/settings.yaml` 可以自定义：

- 模型路径
- 默认输入输出路径
- 处理参数（DPI、设备等）
- OCR 参数
- 布局检测目标区域
- 输出格式选项

## 输出格式

### TXT 格式

纯文本格式，每页用分隔符分开：

```
===== 第 1 页 =====
这是第一页的文本内容...

===== 第 2 页 =====
这是第二页的文本内容...
```

### JSON 格式

结构化数据，包含坐标和标签信息：

```json
[
  {
    "page_num": 1,
    "regions": [
      {
        "text": "文本内容",
        "bbox": [100, 200, 500, 250],
        "label": "text"
      }
    ]
  }
]
```

### Markdown 格式

Markdown 格式，标题和正文分层：

```markdown
## 第 1 页

### 章节标题

正文内容...
```

## 开发

### 添加新功能

项目采用模块化设计，可以轻松扩展：

1. **新增布局类型**: 修改 `config/settings.yaml` 中的 `target_labels`
2. **自定义 OCR**: 在 `ocr_engine.py` 中扩展 `OCREngine` 类
3. **新增输出格式**: 在 `text_extractor.py` 中添加 `_save_as_xxx` 方法

### 运行测试

```bash
pytest tests/
```

## 常见问题

### 1. 模型加载失败

检查配置文件中的模型路径是否正确，模型文件是否完整。

### 2. 内存不足

- 减小 `processing.dpi` 值
- 减小 `processing.max_crop_width` 值
- 分批处理页面

### 3. OCR 识别效果差

- 提高 `processing.dpi` 值（推荐 300-600）
- 检查 PDF 源文件质量
- 尝试其他 PaddleOCR 模型
