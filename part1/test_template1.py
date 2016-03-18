# -*- coding: utf-8 -*-
import pytest

from template1a import CodeBuilder as CodeBuilderA
from template1b import Template as TemplateB
from template1c import Template as TemplateC
from template1d import Template as TemplateD


class TesteCodeBuilderA:

    def setup(self):
        self.code_builder = CodeBuilderA()

    def test_forward(self):
        self.code_builder.forward()
        assert self.code_builder.indent == 4

    def test_backward(self):
        self.code_builder.backward()
        assert self.code_builder.indent == -4

    def test_add(self):
        self.code_builder.add('hello')
        assert self.code_builder.lines == ['hello']

    def test_add_line(self):
        self.code_builder.forward()
        self.code_builder.add_line('hello')
        assert self.code_builder.lines == ['    hello']


class TestTemplateB:
    Template = TemplateB

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        ('', '''def __func_name():
    __result = []
    __result.extend([])
    return "".join(__result)''', {}, ''),
    ])
    def test_templateb(self, text, code, context, output):
        template = self.Template(text)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output


class TestTemplateC:
    """变量"""
    Template = TemplateC

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        ('<h1>{{ title }}</h1>', '''def __func_name():
    __result = []
    __result.extend(['<h1>',str(title),'</h1>'])
    return "".join(__result)''', {'title': 'Python'}, '<h1>Python</h1>'),
        ('{{ 1 + 2 }}', None, {}, '3'),
        ('{{ items[0] }}', None, {'items': [1, 2, 3]}, '1'),
        ('{{ func() }}', None, {'func': list}, '[]'),
    ])
    def test_templatec(self, text, code, context, output):
        template = self.Template(text)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output


class TestTemplateD(TestTemplateC):
    """注释"""
    Template = TemplateD

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        ('<h1>{{ title }} {# comment #}</h1>', '''def __func_name():
    __result = []
    __result.extend(['<h1>',str(title),' ','</h1>'])
    return "".join(__result)''', {'title': 'Python'}, '<h1>Python </h1>'),
    ])
    def test_templated(self, text, code, context, output):
        template = self.Template(text)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output
