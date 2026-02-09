import unittest
import os
import tempfile
from secpdf import PDFSecurityTool

class TestPDFSecurityTool(unittest.TestCase):
    """
    PDF安全处理工具的单元测试
    遵循TDD开发最佳实践
    """
    
    def setUp(self):
        """
        测试前的准备工作
        """
        self.tool = PDFSecurityTool()
        self.test_pdf = "test/example.pdf"
        self.test_password = "testpassword123"
        
        # 确保测试PDF文件存在
        self.assertTrue(os.path.exists(self.test_pdf), "测试PDF文件不存在")
    
    def test_pdf_to_images(self):
        """
        测试PDF转图片功能
        """
        # 执行PDF转图片
        images = self.tool.pdf_to_images(self.test_pdf)
        
        # 验证返回结果
        self.assertIsInstance(images, list, "应该返回图片对象列表")
        self.assertTrue(len(images) > 0, "应该至少转换一页")
    
    def test_images_to_pdf_in_memory(self):
        """
        测试图片转PDF功能
        """
        # 先获取图片对象
        images = self.tool.pdf_to_images(self.test_pdf)
        
        # 执行图片转PDF
        pdf_bytes = self.tool.images_to_pdf_in_memory(images)
        
        # 验证返回结果
        self.assertIsInstance(pdf_bytes, bytes, "应该返回PDF字节数据")
        self.assertTrue(len(pdf_bytes) > 0, "PDF字节数据不应为空")
    
    def test_encrypt_pdf_in_memory(self):
        """
        测试PDF加密功能
        """
        # 先获取PDF字节数据
        with open(self.test_pdf, "rb") as f:
            pdf_bytes = f.read()
        
        # 执行PDF加密
        encrypted_pdf_bytes = self.tool.encrypt_pdf_in_memory(pdf_bytes, self.test_password)
        
        # 验证返回结果
        self.assertIsInstance(encrypted_pdf_bytes, bytes, "应该返回加密后的PDF字节数据")
        self.assertTrue(len(encrypted_pdf_bytes) > 0, "加密后的PDF字节数据不应为空")
    
    def test_encrypt_regular_pdf(self):
        """
        测试模式1: 生成加密普通PDF文件
        """
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            output_pdf = temp_file.name
        
        try:
            # 执行加密普通PDF
            self.tool.encrypt_regular_pdf(self.test_pdf, output_pdf, self.test_password)
            
            # 验证输出文件存在
            self.assertTrue(os.path.exists(output_pdf), "加密PDF文件应存在")
            self.assertTrue(os.path.getsize(output_pdf) > 0, "加密PDF文件不应为空")
        finally:
            # 清理临时文件
            if os.path.exists(output_pdf):
                os.unlink(output_pdf)
    
    def test_generate_images(self):
        """
        测试模式2: 生成图片
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # 执行生成图片
            self.tool.generate_images(self.test_pdf, temp_dir)
            
            # 验证图片文件存在
            image_files = [f for f in os.listdir(temp_dir) if f.endswith('.png')]
            self.assertTrue(len(image_files) > 0, "应该生成至少一张图片")
            
            # 验证每张图片都不为空
            for image_file in image_files:
                image_path = os.path.join(temp_dir, image_file)
                self.assertTrue(os.path.getsize(image_path) > 0, f"图片文件 {image_file} 不应为空")
    
    def test_generate_image_pdf(self):
        """
        测试模式3: 生成图片内容的PDF
        """
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            output_pdf = temp_file.name
        
        try:
            # 执行生成图片内容的PDF
            self.tool.generate_image_pdf(self.test_pdf, output_pdf)
            
            # 验证输出文件存在
            self.assertTrue(os.path.exists(output_pdf), "图片内容PDF文件应存在")
            self.assertTrue(os.path.getsize(output_pdf) > 0, "图片内容PDF文件不应为空")
        finally:
            # 清理临时文件
            if os.path.exists(output_pdf):
                os.unlink(output_pdf)
    
    def test_generate_encrypted_image_pdf(self):
        """
        测试模式4: 生成图片内容的PDF加密文件
        """
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            output_pdf = temp_file.name
        
        try:
            # 执行生成图片内容的PDF加密文件
            self.tool.generate_encrypted_image_pdf(self.test_pdf, output_pdf, self.test_password)
            
            # 验证输出文件存在
            self.assertTrue(os.path.exists(output_pdf), "加密图片内容PDF文件应存在")
            self.assertTrue(os.path.getsize(output_pdf) > 0, "加密图片内容PDF文件不应为空")
        finally:
            # 清理临时文件
            if os.path.exists(output_pdf):
                os.unlink(output_pdf)
    
    def test_save_images(self):
        """
        测试保存图片功能
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # 先获取图片对象
            images = self.tool.pdf_to_images(self.test_pdf)
            
            # 执行保存图片
            image_paths = self.tool.save_images(images, temp_dir)
            
            # 验证返回结果
            self.assertIsInstance(image_paths, list, "应该返回图片路径列表")
            self.assertEqual(len(image_paths), len(images), "保存的图片数量应与转换的图片数量一致")
            
            # 验证图片文件存在
            for image_path in image_paths:
                self.assertTrue(os.path.exists(image_path), f"图片文件 {image_path} 应存在")
                self.assertTrue(os.path.getsize(image_path) > 0, f"图片文件 {image_path} 不应为空")

if __name__ == '__main__':
    unittest.main()
