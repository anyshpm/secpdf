# secpdf - PDF文件安全处理工具

本工具用于PDF文件的安全处理，支持多种处理模式，包括PDF加密、PDF转图片、图片转PDF等功能。提供命令行和GUI两种使用方式。

## 界面预览

![secpdf GUI界面](secpdf_gui.png)

## 功能

- **模式1**：生成加密普通PDF文件
- **模式2**：生成图片
- **模式3**：生成图片内容的PDF（防止文字被复制）
- **模式4**：生成图片内容的PDF加密文件（双重保护）
- 全内存操作，避免生成中间文件
- 提供命令行和GUI两种使用方式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 命令行版本

```bash
python secpdf.py <模式> <输入PDF文件> <输出路径> [密码]
```

### 模式说明

- **encrypt**：生成加密普通PDF文件（需要密码）
- **images**：生成图片（输出路径为文件夹）
- **image-pdf**：生成图片内容的PDF（输出路径为PDF文件）
- **encrypt-image-pdf**：生成图片内容的PDF加密文件（需要密码）

### 示例

#### 模式1：生成加密普通PDF文件
```bash
python secpdf.py encrypt input.pdf output_encrypted.pdf mypassword123
```

#### 模式2：生成图片
```bash
python secpdf.py images input.pdf output_images
```

#### 模式3：生成图片内容的PDF
```bash
python secpdf.py image-pdf input.pdf output_image_pdf.pdf
```

#### 模式4：生成图片内容的PDF加密文件
```bash
python secpdf.py encrypt-image-pdf input.pdf output_encrypted_image_pdf.pdf mypassword123
```

### 2. GUI版本

```bash
python secpdf_gui.py
```

#### GUI操作步骤

1. **选择输入PDF文件**：点击"浏览"按钮选择要处理的PDF文件
2. **选择处理模式**：点击对应模式的按钮（加密PDF、生成图片、图片PDF、加密图片PDF）
3. **输入密码（如果需要）**：对于加密模式，会弹出密码输入对话框
4. **选择输出路径**：根据模式，会弹出文件或文件夹选择对话框
5. **等待处理完成**：程序会自动执行处理并显示结果

## 工作原理

### 模式1：加密普通PDF
1. 读取原始PDF文件
2. 在内存中对PDF进行加密
3. 保存加密后的PDF文件

### 模式2：生成图片
1. 将PDF文件每页转换为图片对象
2. 将图片保存到指定文件夹

### 模式3：生成图片内容的PDF
1. 将PDF文件每页转换为内存中的图片对象
2. 在内存中将图片对象合并为PDF字节数据
3. 保存生成的PDF文件

### 模式4：生成图片内容的PDF加密文件
1. 将PDF文件每页转换为内存中的图片对象
2. 在内存中将图片对象合并为PDF字节数据
3. 在内存中对PDF字节数据进行加密
4. 保存加密后的PDF文件

## 注意事项

- **模式2**会在指定文件夹中生成图片文件，其他模式均为全内存操作
- 转换后的图片内容PDF无法直接复制文字，保护了文档内容
- 加密后的PDF文件需要密码才能打开
- 确保输入PDF文件存在且可读
- 对于大文件，可能会占用较多内存

## 依赖库

- PyMuPDF：用于PDF转图片
- Pillow：用于图片处理
- pypdf：用于PDF加密
- tkinter：用于GUI界面（Python内置，无需单独安装）
