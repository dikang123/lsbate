# -*- coding: utf-8 -*-
# tested on Python 3.5.1


class CodeBuilder:
    INDENT_STEP = 4     # 每次缩进的空格数

    def __init__(self, indent=0):
        self.indent = indent    # 当前缩进
        self.lines = []         # 保存一行一行生成的代码

    def forward(self):
        """缩进前进一步"""
        self.indent += self.INDENT_STEP

    def backward(self):
        """缩进后退一步"""
        self.indent -= self.INDENT_STEP

    def add(self, code):
        self.lines.append(code)

    def add_line(self, code):
        self.lines.append(' ' * self.indent + code)

    def __str__(self):
        """拼接所有代码行后的源码"""
        return '\n'.join(map(str, self.lines))

    def __repr__(self):
        """方便调试"""
        return str(self)
