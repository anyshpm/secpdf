import fitz
from PIL import Image
from pypdf import PdfWriter, PdfReader
from io import BytesIO
import os
import argparse


class PDFSecurityTool:
    """
    PDF文件安全处理工具
    支持四种模式：
    1. 生成加密普通PDF文件
    2. 生成图片
    3. 生成图片内容的PDF
    4. 生成图片内容的PDF加密文件
    """
    
    def pdf_to_images(self, pdf_path):
        """
        将PDF文件转换为图片对象
        
        Args:
            pdf_path: PDF文件路径
        
        Returns:
            图片对象列表
        """
        print("正在将PDF转换为图片...")
        
        # 打开PDF文件
        doc = fitz.open(pdf_path)
        images = []
        
        # 遍历每一页
        for page_num in range(len(doc)):
            # 获取页面
            page = doc.load_page(page_num)
            
            # 转换页面为图片
            pix = page.get_pixmap()
            
            # 将pixmap转换为PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        
        doc.close()
        print(f"成功转换 {len(images)} 页")
        return images
    
    def save_images(self, images, output_folder):
        """
        保存图片到指定文件夹
        
        Args:
            images: 图片对象列表
            output_folder: 输出文件夹路径
        """
        # 确保输出文件夹存在
        os.makedirs(output_folder, exist_ok=True)
        
        print(f"正在保存图片到 {output_folder}...")
        image_paths = []
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{i+1}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)
        
        print(f"成功保存 {len(image_paths)} 张图片")
        return image_paths
    
    def images_to_pdf_in_memory(self, images):
        """
        在内存中将图片对象合并为PDF字节数据
        
        Args:
            images: 图片对象列表
        
        Returns:
            PDF字节数据
        """
        if not images:
            raise ValueError("No images to convert")
        
        print("正在将图片合并为PDF...")
        # 准备图片
        prepared_images = []
        for img in images:
            # 确保图片模式一致
            if img.mode != "RGB":
                img = img.convert("RGB")
            prepared_images.append(img)
        
        # 在内存中保存为PDF
        output_stream = BytesIO()
        first_image = prepared_images[0]
        other_images = prepared_images[1:]
        
        first_image.save(
            output_stream,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=other_images
        )
        
        output_stream.seek(0)
        print("图片合并完成")
        return output_stream.read()
    
    def encrypt_pdf_in_memory(self, pdf_bytes, password):
        """
        在内存中为PDF添加密码保护
        
        Args:
            pdf_bytes: PDF文件的字节数据
            password: 密码
        
        Returns:
            加密后的PDF字节数据
        """
        print("正在为PDF添加密码保护...")
        # 创建PDF写入器
        writer = PdfWriter()
        
        # 从字节数据读取PDF
        reader = PdfReader(BytesIO(pdf_bytes))
        
        # 添加所有页面到写入器
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)
        
        # 设置加密
        writer.encrypt(password)
        
        # 将加密后的PDF写入字节流
        output_stream = BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)
        
        print("加密完成")
        return output_stream.read()
    
    def encrypt_regular_pdf(self, input_pdf, output_pdf, password):
        """
        模式1: 生成加密普通PDF文件
        
        Args:
            input_pdf: 输入PDF文件路径
            output_pdf: 输出加密PDF文件路径
            password: 密码
        """
        print("模式1: 生成加密普通PDF文件")
        
        # 读取原始PDF
        with open(input_pdf, "rb") as f:
            pdf_bytes = f.read()
        
        # 加密PDF
        encrypted_pdf_bytes = self.encrypt_pdf_in_memory(pdf_bytes, password)
        
        # 保存加密后的PDF
        print(f"正在保存加密PDF文件...")
        with open(output_pdf, "wb") as f:
            f.write(encrypted_pdf_bytes)
        
        print(f"处理完成！加密PDF已保存到: {output_pdf}")
    
    def generate_images(self, input_pdf, output_folder):
        """
        模式2: 生成图片
        
        Args:
            input_pdf: 输入PDF文件路径
            output_folder: 图片输出文件夹
        """
        print("模式2: 生成图片")
        
        # PDF转图片
        images = self.pdf_to_images(input_pdf)
        
        # 保存图片
        self.save_images(images, output_folder)
    
    def generate_image_pdf(self, input_pdf, output_pdf):
        """
        模式3: 生成图片内容的PDF
        
        Args:
            input_pdf: 输入PDF文件路径
            output_pdf: 输出PDF文件路径
        """
        print("模式3: 生成图片内容的PDF")
        
        # PDF转图片
        images = self.pdf_to_images(input_pdf)
        
        # 图片转PDF
        pdf_bytes = self.images_to_pdf_in_memory(images)
        
        # 保存PDF
        print(f"正在保存PDF文件...")
        with open(output_pdf, "wb") as f:
            f.write(pdf_bytes)
        
        print(f"处理完成！PDF已保存到: {output_pdf}")
    
    def generate_encrypted_image_pdf(self, input_pdf, output_pdf, password):
        """
        模式4: 生成图片内容的PDF加密文件
        
        Args:
            input_pdf: 输入PDF文件路径
            output_pdf: 输出加密PDF文件路径
            password: 密码
        """
        print("模式4: 生成图片内容的PDF加密文件")
        
        # PDF转图片
        images = self.pdf_to_images(input_pdf)
        
        # 图片转PDF
        pdf_bytes = self.images_to_pdf_in_memory(images)
        
        # 加密PDF
        encrypted_pdf_bytes = self.encrypt_pdf_in_memory(pdf_bytes, password)
        
        # 保存加密后的PDF
        print(f"正在保存加密PDF文件...")
        with open(output_pdf, "wb") as f:
            f.write(encrypted_pdf_bytes)
        
        print(f"处理完成！加密PDF已保存到: {output_pdf}")


def main():
    parser = argparse.ArgumentParser(description="PDF文件安全处理工具")
    parser.add_argument("mode", choices=["encrypt", "images", "image-pdf", "encrypt-image-pdf"], 
                        help="处理模式: encrypt=生成加密普通PDF文件, images=生成图片, image-pdf=生成图片内容的PDF, encrypt-image-pdf=生成图片内容的PDF加密文件")
    parser.add_argument("input", help="输入PDF文件路径")
    parser.add_argument("output", help="输出文件/文件夹路径")
    parser.add_argument("password", nargs="?", help="密码（encrypt和encrypt-image-pdf模式需要）")
    
    args = parser.parse_args()
    
    # 验证输入文件存在
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在 - {args.input}")
        exit(1)
    
    # 验证密码参数
    if args.mode in ["encrypt", "encrypt-image-pdf"] and not args.password:
        print("错误: encrypt和encrypt-image-pdf模式需要密码参数")
        exit(1)
    
    # 创建工具实例
    tool = PDFSecurityTool()
    
    # 根据模式执行不同操作
    if args.mode == "encrypt":
        tool.encrypt_regular_pdf(args.input, args.output, args.password)
    elif args.mode == "images":
        tool.generate_images(args.input, args.output)
    elif args.mode == "image-pdf":
        tool.generate_image_pdf(args.input, args.output)
    elif args.mode == "encrypt-image-pdf":
        tool.generate_encrypted_image_pdf(args.input, args.output, args.password)


if __name__ == "__main__":
    main()
