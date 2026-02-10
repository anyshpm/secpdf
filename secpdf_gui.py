import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from secpdf.core import PDFSecurityTool
from secpdf._version import __version__
import os

class PDFSecurityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"PDF安全处理工具 v{__version__}")
        # 不设置具体的geometry值，让Tkinter自动计算窗口大小
        self.root.resizable(True, True)
        
        # 创建工具实例
        self.tool = PDFSecurityTool()
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        self.title_label = ttk.Label(self.main_frame, text="PDF安全处理工具", font=("SimHei", 16, "bold"))
        self.title_label.pack(pady=(0, 20))
        
        # 创建输入文件选择框架
        self.input_frame = ttk.LabelFrame(self.main_frame, text="1. 选择输入PDF文件", padding="10")
        self.input_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.input_var = tk.StringVar()
        input_entry_frame = ttk.Frame(self.input_frame)
        input_entry_frame.pack(fill=tk.X)
        
        ttk.Entry(input_entry_frame, textvariable=self.input_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_entry_frame, text="浏览", command=self.browse_input).pack(side=tk.RIGHT)
        
        # 创建模式选择框架
        self.mode_frame = ttk.LabelFrame(self.main_frame, text="2. 选择处理模式", padding="10")
        self.mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 模式按钮
        button_frame = ttk.Frame(self.mode_frame)
        button_frame.pack(fill=tk.X)
        
        # 创建水平排列的按钮
        ttk.Button(button_frame, text="加密PDF", command=lambda: self.on_mode_button_click("encrypt")).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(button_frame, text="生成图片", command=lambda: self.on_mode_button_click("images")).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(button_frame, text="图片PDF", command=lambda: self.on_mode_button_click("image-pdf")).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(button_frame, text="加密图片PDF", command=lambda: self.on_mode_button_click("encrypt-image-pdf")).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self.main_frame, text="状态:", font=("SimHei", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var, font=("SimHei", 10, "bold"), foreground="green")
        self.status_label.pack(anchor=tk.W, pady=(0, 0))
        
        # 初始化界面状态
        # 现在使用按钮直接触发操作，不再需要跟踪模式变量的变化
    
    def browse_input(self):
        """浏览输入PDF文件"""
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*")]
        )
        if file_path:
            self.input_var.set(file_path)
    
    def on_mode_button_click(self, mode):
        """点击模式按钮后的处理逻辑"""
        # 获取输入文件路径
        input_pdf = self.input_var.get()
        
        # 验证输入文件存在
        if not input_pdf:
            messagebox.showerror("错误", "请先选择输入PDF文件")
            return
        
        if not os.path.exists(input_pdf):
            messagebox.showerror("错误", f"输入文件不存在: {input_pdf}")
            return
        
        # 密码处理
        password = None
        if mode in ["encrypt", "encrypt-image-pdf"]:
            # 弹出密码输入对话框
            password_window = tk.Toplevel(self.root)
            password_window.title("输入密码")
            password_window.geometry("400x150")
            password_window.transient(self.root)
            password_window.grab_set()
            
            # 密码输入框架
            password_frame = ttk.Frame(password_window, padding="20")
            password_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(password_frame, text="请输入密码:").pack(anchor=tk.W, pady=(0, 10))
            password_var = tk.StringVar()
            password_entry = ttk.Entry(password_frame, textvariable=password_var, show="*")
            password_entry.pack(fill=tk.X, pady=(0, 15))
            password_entry.focus()
            
            # 确认按钮
            def on_password_ok():
                nonlocal password
                password = password_var.get()
                if not password:
                    messagebox.showerror("错误", "密码不能为空")
                    return
                password_window.destroy()
            
            button_frame = ttk.Frame(password_frame)
            button_frame.pack(fill=tk.X)
            ttk.Button(button_frame, text="确定", command=on_password_ok).pack(side=tk.RIGHT, padx=(10, 0))
            ttk.Button(button_frame, text="取消", command=password_window.destroy).pack(side=tk.RIGHT)
            
            # 等待密码输入窗口关闭
            self.root.wait_window(password_window)
            
            if not password:
                return
        
        # 选择输出路径
        output = None
        if mode == "images":
            # 生成图片模式，选择文件夹
            output = filedialog.askdirectory(title="选择图片输出文件夹")
        else:
            # 其他模式，选择PDF文件
            output = filedialog.asksaveasfilename(
                title="保存输出PDF文件",
                defaultextension=".pdf",
                filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*")]
            )
        
        if not output:
            return
        
        # 更新状态
        self.status_var.set("执行中...")
        self.root.update()
        
        try:
            # 根据模式执行不同操作
            if mode == "encrypt":
                self.tool.encrypt_regular_pdf(input_pdf, output, password)
            elif mode == "images":
                # 确保输出文件夹存在
                os.makedirs(output, exist_ok=True)
                self.tool.generate_images(input_pdf, output)
            elif mode == "image-pdf":
                self.tool.generate_image_pdf(input_pdf, output)
            elif mode == "encrypt-image-pdf":
                self.tool.generate_encrypted_image_pdf(input_pdf, output, password)
            
            # 执行成功
            self.status_var.set("执行成功！")
            messagebox.showinfo("成功", f"处理完成！结果已保存到: {output}")
        except Exception as e:
            # 执行失败
            self.status_var.set("执行失败")
            messagebox.showerror("错误", f"处理过程中出错: {str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    # 添加样式
    style = ttk.Style()
    style.configure("Accent.TButton", font=("SimHei", 10, "bold"))
    
    app = PDFSecurityGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
