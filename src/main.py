"""主入口程序"""
import argparse
import sys
from pathlib import Path

from .config import config
from .logger import setup_logger, logger
from .text_extractor import TextExtractor


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="PDF 文本提取工具 - 使用 PaddleX Layout + PaddleOCR"
    )

    parser.add_argument(
        "--pdf",
        type=str,
        default=None,
        help=f"PDF 文件路径 (默认: {config.default_pdf})"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件路径 (默认: data/txt/output.txt)"
    )

    parser.add_argument(
        "--first-page",
        type=int,
        default=None,
        help=f"起始页码 (默认: {config.get('processing.first_page', 1)})"
    )

    parser.add_argument(
        "--last-page",
        type=int,
        default=None,
        help=f"结束页码 (默认: {config.get('processing.last_page', '全部')})"
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["txt", "json", "markdown"],
        default="txt",
        help="输出格式 (默认: txt)"
    )

    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="处理完成后清理临时图片"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细日志"
    )

    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="日志文件路径"
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 设置日志
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logger(
        level=getattr(__import__("logging"), log_level),
        log_file=args.log_file
    )

    # 确定输入输出路径
    pdf_path = args.pdf or config.default_pdf
    if not Path(pdf_path).exists():
        logger.error(f"PDF 文件不存在: {pdf_path}")
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        output_dir = config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        ext = args.format if args.format != "txt" else "txt"
        output_path = output_dir / f"output.{ext}"

    # 打印配置信息
    logger.info("=" * 60)
    logger.info("PDF 文本提取工具")
    logger.info("=" * 60)
    logger.info(f"输入文件: {pdf_path}")
    logger.info(f"输出文件: {output_path}")
    logger.info(f"输出格式: {args.format}")
    logger.info(f"页码范围: {args.first_page or '开始'} - {args.last_page or '结束'}")
    logger.info("=" * 60)

    try:
        # 创建提取器并执行
        extractor = TextExtractor()
        stats = extractor.extract_from_pdf(
            pdf_path=pdf_path,
            output_path=str(output_path),
            first_page=args.first_page,
            last_page=args.last_page,
            output_format=args.format,
            cleanup=args.cleanup
        )

        # 打印统计信息
        logger.info("=" * 60)
        logger.info("提取完成！")
        logger.info(f"成功页数: {stats['success_pages']}/{stats['total_pages']}")
        logger.info(f"文本区域: {stats['total_regions']}")
        if stats['failed_pages']:
            logger.warning(f"失败页码: {stats['failed_pages']}")
        logger.info(f"输出文件: {stats['output_path']}")
        logger.info("=" * 60)

    except KeyboardInterrupt:
        logger.info("\n用户中断")
        sys.exit(0)

    except Exception as e:
        logger.error(f"处理失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
