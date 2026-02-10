from setuptools import setup, find_packages
import os

# Read version from _version.py
version = {}
with open(os.path.join("secpdf", "_version.py")) as fp:
    exec(fp.read(), version)

setup(
    name="secpdf",
    version=version["__version__"],
    description="PDF文件安全处理工具",
    long_description="""PDF文件安全处理工具，支持以下功能：
1. 生成加密普通PDF文件
2. 生成图片
3. 生成图片内容的PDF
4. 生成图片内容的PDF加密文件
""",
    author="",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    py_modules=["secpdf_gui"],
    install_requires=[
        "PyMuPDF",
        "Pillow",
        "pypdf"
    ],
    entry_points={
        "console_scripts": [
            "secpdf=secpdf.core:main",
            "secpdf-gui=secpdf_gui:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
