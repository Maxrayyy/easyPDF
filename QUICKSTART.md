# 快速启动指南

## 🚀 立即开始

### 0. 配置模型和 PDF（首次使用）

#### 下载模型

**一键下载（推荐）：**

```bash
python download_models.py
```

模型会自动下载到缓存目录。或者使用 wget 手动下载（详见 [models/README.md](models/README.md)）。

#### 添加 PDF

将 PDF 文件放到 `pdfs/` 目录：

```bash
cp /path/to/your.pdf pdfs/
```

### 1. 查看帮助

```bash
python run.py --help
```

### 2. 运行第一个示例

```bash
# 使用默认配置（处理第 9-69 页）
python run.py

# 或指定 PDF 文件和页码范围
python run.py --pdf /path/to/your.pdf --first-page 1 --last-page 10
```

## 📝 常用命令

### 提取整个 PDF
```bash
python run.py --pdf input.pdf
```

### 提取指定页面
```bash
python run.py --pdf input.pdf --first-page 5 --last-page 15
```

### 输出为 JSON 格式
```bash
python run.py --pdf input.pdf --output result.json --format json
```

### 输出为 Markdown 格式
```bash
python run.py --pdf input.pdf --output result.md --format markdown
```

### 处理后清理临时文件
```bash
python run.py --pdf input.pdf --cleanup
```

### 显示详细日志
```bash
python run.py --pdf input.pdf --verbose
```

### 保存日志到文件
```bash
python run.py --pdf input.pdf --log-file extraction.log
```

## ⚙️ 配置修改

编辑 `config/settings.yaml` 修改：

### 修改模型路径和 PDF 路径
```yaml
models:
  layout_model_dir: "models/PP-DocLayout_plus-L_infer"  # 相对路径
  # 或使用绝对路径: "/your/path/to/PP-DocLayout_plus-L_infer"

paths:
  default_pdf: "pdfs/sample.pdf"  # 默认 PDF 文件
```

### 修改默认处理参数
```yaml
processing:
  dpi: 300                    # 提高到 600 可获得更好质量
  first_page: 1               # 默认起始页
  last_page: 100              # 默认结束页
  device: "gpu"               # 改为 gpu 加速（需要 GPU 支持）
```

### 修改要提取的区域类型
```yaml
layout:
  target_labels:
    - "text"
    - "paragraph_title"
    - "table"                 # 添加表格
    - "figure"                # 添加图片
```

## 🔧 代码调用示例

### 基本使用
```python
from src import TextExtractor

extractor = TextExtractor()
stats = extractor.extract_from_pdf(
    pdf_path="input.pdf",
    output_path="output.txt",
    first_page=1,
    last_page=10
)
print(stats)
```

### JSON 输出
```python
stats = extractor.extract_from_pdf(
    pdf_path="input.pdf",
    output_path="output.json",
    output_format="json"
)
```

### Markdown 输出
```python
stats = extractor.extract_from_pdf(
    pdf_path="input.pdf",
    output_path="output.md",
    output_format="markdown"
)
```

## 🐛 问题排查

### 问题 1: 模块导入失败
```bash
# 安装依赖
pip install -r requirements.txt
```

### 问题 2: 模型路径错误
检查 `config/settings.yaml` 中的模型路径是否正确：
```bash
ls /home/zhidong_huang/PDF_models/PP-DocLayout_plus-L_infer
```

### 问题 3: 内存不足
在 `config/settings.yaml` 中降低 DPI：
```yaml
processing:
  dpi: 200  # 降低到 200
```

### 问题 4: PDF 文件无法打开
确保 PDF 文件存在且没有加密：
```bash
ls -lh /path/to/your.pdf
```

## 📊 输出格式说明

### TXT 格式
```
===== 第 1 页 =====
这是页面文本内容...

===== 第 2 页 =====
更多文本内容...
```

### JSON 格式
```json
[
  {
    "page_num": 1,
    "regions": [
      {
        "text": "文本内容",
        "bbox": [100, 200, 500, 300],
        "label": "text"
      }
    ]
  }
]
```

### Markdown 格式
```markdown
## 第 1 页

### 章节标题

正文内容段落...
```

## 💡 性能优化建议

1. **使用 GPU 加速**: 修改配置 `device: "gpu"`
2. **批量处理**: 分批处理大文件
3. **降低 DPI**: 如果不需要高精度，可降低到 200-250
4. **清理临时文件**: 使用 `--cleanup` 参数

## 📚 下一步

- 阅读完整文档: [README.md](README.md)
- 修改配置文件: [config/settings.yaml](config/settings.yaml)
- 查看模型设置: [models/README.md](models/README.md)

祝你使用愉快！🎉
