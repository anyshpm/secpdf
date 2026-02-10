"""
SecPDF - PDF文件安全处理工具

该包提供了PDF文件的安全处理功能，包括：
1. 加密PDF文件
2. PDF转图片
3. PDF转图片再转PDF
4. PDF转图片再转加密PDF
"""

from ._version import __version__, __author__, __license__
from .core import PDFSecurityTool

__all__ = ["__version__", "__author__", "__license__", "PDFSecurityTool"]
