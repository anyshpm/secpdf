import argparse
import sys
import io
import os

# 设置标准输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from secpdf.core import PDFSecurityTool
from secpdf._version import __version__


def main():
    parser = argparse.ArgumentParser(
        description="PDF文件安全处理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s encrypt input.pdf output.pdf password    加密PDF文件
  %(prog)s images input.pdf ./output_folder        PDF转图片
  %(prog)s image-pdf input.pdf output.pdf          PDF转图片再转PDF
  %(prog)s encrypt-image-pdf input.pdf out.pdf pwd  PDF转图片再转加密PDF
        """
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("mode", choices=["encrypt", "images", "image-pdf", "encrypt-image-pdf"],
                        nargs="?", help="处理模式")
    parser.add_argument("input", nargs="?", help="输入PDF文件路径")
    parser.add_argument("output", nargs="?", help="输出文件/文件夹路径")
    parser.add_argument("password", nargs="?", help="密码（encrypt和encrypt-image-pdf模式需要）")

    args = parser.parse_args()

    # 如果没有提供模式，显示帮助信息
    if not args.mode:
        parser.print_help()
        sys.exit(1)

    # 验证必需参数
    if not args.input or not args.output:
        print("错误: 缺少必需参数")
        print(f"\n使用 '{sys.argv[0]} --help' 查看帮助信息")
        sys.exit(1)

    # 验证输入文件存在
    import os
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在 - {args.input}")
        sys.exit(1)

    # 验证密码参数
    if args.mode in ["encrypt", "encrypt-image-pdf"] and not args.password:
        print("错误: encrypt和encrypt-image-pdf模式需要密码参数")
        sys.exit(1)

    # 创建工具实例
    tool = PDFSecurityTool()

    # 根据模式执行不同操作
    try:
        if args.mode == "encrypt":
            tool.encrypt_regular_pdf(args.input, args.output, args.password)
        elif args.mode == "images":
            tool.generate_images(args.input, args.output)
        elif args.mode == "image-pdf":
            tool.generate_image_pdf(args.input, args.output)
        elif args.mode == "encrypt-image-pdf":
            tool.generate_encrypted_image_pdf(args.input, args.output, args.password)
    except Exception as e:
        print(f"错误: 处理过程中出错 - {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
