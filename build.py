import os
import subprocess
import shutil

# 清理之前的构建目录
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# 构建命令行版本
print("正在生成命令行版本可执行程序...")
command_cli = [
    'pyinstaller',
    '--onefile',
    '--name', 'secpdf',
    '--console',
    'secpdf.py'
]

try:
    # 执行构建命令
    result_cli = subprocess.run(command_cli, cwd=os.getcwd(), capture_output=True, text=True)
    
    if result_cli.returncode == 0:
        print("\n命令行版本构建成功！")
    else:
        print("\n命令行版本构建失败！")
        print("错误信息:")
        print(result_cli.stderr)
        print("输出信息:")
        print(result_cli.stdout)
        
except Exception as e:
    print(f"构建命令行版本过程中出错: {e}")

# 构建GUI版本
print("\n正在生成GUI版本可执行程序...")
command_gui = [
    'pyinstaller',
    '--onefile',
    '--name', 'secpdf-gui',
    '--windowed',  # 使用窗口模式而不是控制台模式
    'secpdf_gui.py'
]

try:
    # 执行构建命令
    result_gui = subprocess.run(command_gui, cwd=os.getcwd(), capture_output=True, text=True)
    
    if result_gui.returncode == 0:
        print("\nGUI版本构建成功！")
    else:
        print("\nGUI版本构建失败！")
        print("错误信息:")
        print(result_gui.stderr)
        print("输出信息:")
        print(result_gui.stdout)
        
except Exception as e:
    print(f"构建GUI版本过程中出错: {e}")

# 输出结果
print("\n构建完成！")
print("可执行程序已生成在 dist 目录中:")
print(f"命令行版本: {os.path.join(os.getcwd(), 'dist', 'secpdf.exe')}")
print(f"GUI版本: {os.path.join(os.getcwd(), 'dist', 'secpdf-gui.exe')}")
