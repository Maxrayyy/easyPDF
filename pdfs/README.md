# PDF 文件目录

## 📄 说明

将需要处理的 PDF 文件放到此目录。

## 🔧 使用方法

### 添加 PDF 文件

```bash
# 复制 PDF 到此目录
cp /path/to/your.pdf ./pdfs/

# 或创建符号链接
ln -s /path/to/your.pdf ./pdfs/
```

### 在配置中使用

编辑 `config/settings.yaml`：

```yaml
paths:
  default_pdf: "pdfs/your.pdf"  # 使用相对路径
```

或者在命令行中指定：

```bash
python run.py --pdf pdfs/your.pdf
```

也可以使用绝对路径：

```bash
python run.py --pdf /absolute/path/to/your.pdf
```

## 📝 注意事项

- PDF 文件不会被提交到 Git（已添加到 `.gitignore`）
- 支持相对路径和绝对路径
- 可以直接使用符号链接
