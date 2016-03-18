# -*- coding: utf-8 -*-
import sys

import pytest

sys.path.insert(0, '../part1/')

from test_template1 import TestTemplateD as TestTemplate1D  # noqa
from template2a import Template as TemplateA              # noqa
from template2b import Template as TemplateB              # noqa
from template2c import Template as TemplateC              # noqa
from template2d import Template as TemplateD              # noqa


class TestTemplateA(TestTemplate1D):
    """if"""
    Template = TemplateA

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        ('''
{% if score >= 80 %}
A
{% elif score >= 60 %}
B
{% else %}
C
{% endif %}
''', '''def __func_name():
    __result = []
    __result.extend(['\\n'])
    if score >= 80:
        __result.extend(['\\nA\\n'])
    elif score >= 60:
        __result.extend(['\\nB\\n'])
    else:
        __result.extend(['\\nC\\n'])
    __result.extend(['\\n'])
    return "".join(__result)''', {'score': 90}, '\n\nA\n\n'),
        ('''
{% if score >= 80 %}
A
{% elif score >= 60 %}
B
{% else %}
C
{% endif %}
''', None, {'score': 70}, '\n\nB\n\n'),
        ('''
{% if score >= 80 %}
A
{% elif score >= 60 %}
B
{% else %}
C
{% endif %}
''', None, {'score': 50}, '\n\nC\n\n'),
    ])
    def test_template2a(self, text, code, context, output):
        template = self.Template(text)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output


class TestTemplateB(TestTemplateA):
    """for"""
    Template = TemplateB

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        ('''
{% for number in numbers %}
{{ number }}
{% endfor %}
''', '''def __func_name():
    __result = []
    __result.extend(['\\n'])
    for number in numbers:
        __result.extend(['\\n',str(number),'\\n'])
    __result.extend(['\\n'])
    return "".join(__result)''', {'numbers': range(3)}, '\n\n0\n\n1\n\n2\n\n'),
    ])
    def test_template2a(self, text, code, context, output):
        template = self.Template(text)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output


class TestTemplateC(TestTemplateB):
    """for"""
    Template = TemplateC

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        ('''
{% for number in numbers %}
   {% if number > 2 %}
      {% break %}
   {% else %}
      {{ number }}
   {% endif %}
{% else %}
   no break
{% endfor %}
''', '''def __func_name():
    __result = []
    __result.extend(['\\n'])
    for number in numbers:
        __result.extend(['\\n   '])
        if number > 2:
            __result.extend(['\\n      '])
            break
            __result.extend(['\\n   '])
        else:
            __result.extend(['\\n      ',str(number),'\\n   '])
        __result.extend(['\\n'])
    else:
        __result.extend(['\\n   no break\\n'])
    __result.extend(['\\n'])
    return "".join(__result)''', {'numbers': range(3)},
    '\n\n   \n      0\n   \n\n   \n      1\n   \n\n   \n      2\n   \n\n   no break\n\n'),  # noqa
        ('''
{% for number in numbers %}
   {% if number > 2 %}
      {% break %}
   {% else %}
      {{ number }}
   {% endif %}
{% else %}
   no break
{% endfor %}
''', '''def __func_name():
    __result = []
    __result.extend(['\\n'])
    for number in numbers:
        __result.extend(['\\n   '])
        if number > 2:
            __result.extend(['\\n      '])
            break
            __result.extend(['\\n   '])
        else:
            __result.extend(['\\n      ',str(number),'\\n   '])
        __result.extend(['\\n'])
    else:
        __result.extend(['\\n   no break\\n'])
    __result.extend(['\\n'])
    return "".join(__result)''', {'numbers': range(4)},
    '\n\n   \n      0\n   \n\n   \n      1\n   \n\n   \n      2\n   \n\n   \n      \n'),  # noqa
    ])
    def test_template2a(self, text, code, context, output):
        template = self.Template(text)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output


class TestTemplateD(TestTemplateC):
    Template = TemplateD
