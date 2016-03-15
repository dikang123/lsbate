# -*- coding: utf-8 -*-
# tested on Python 3.5.1
import re


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


class Template:

    def __init__(self, raw_text, indent=0, default_context=None,
                 func_name='__func_name', result_var='__result'):
        self.raw_text = raw_text
        self.default_context = default_context or {}
        self.func_name = func_name
        self.result_var = result_var
        self.code_builder = code_builder = CodeBuilder(indent=indent)
        self.buffered = []

        self.re_variable = re.compile(r'\{\{ .*? \}\}')
        self.re_tokens = re.compile(r'(\{\{ .*? \}\})')

        # 生成 def __func_name():
        code_builder.add_line('def {}():'.format(self.func_name))
        code_builder.forward()
        # 生成 __result = []
        code_builder.add_line('{} = []'.format(self.result_var))
        self._parse_text()

        self.flush_buffer()
        # 生成 return "".join(__result)
        code_builder.add_line('return "".join({})'.format(self.result_var))
        code_builder.backward()

    def _parse_text(self):
        tokens = self.re_tokens.split(self.raw_text)

        for token in tokens:
            # {{ variable }}
            if self.re_variable.match(token):
                variable = token.strip('{} ')
                self.buffered.append('str({})'.format(variable))
            else:
                self.buffered.append('{}'.format(repr(token)))

    def flush_buffer(self):
        # 生成类似代码: __result.extend(['<h1>', name, '</h1>'])
        line = '{0}.extend([{1}])'.format(
            self.result_var, ','.join(self.buffered)
        )
        self.code_builder.add_line(line)
        self.buffered = []

    def render(self, context=None):
        namespace = {}
        namespace.update(self.default_context)
        if context:
            namespace.update(context)
        exec(str(self.code_builder), namespace)
        result = namespace[self.func_name]()
        return result
