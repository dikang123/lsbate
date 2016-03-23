# -*- coding: utf-8 -*-
import os
import sys

import pytest

sys.path.insert(0, '../part2/')

from test_template2 import TestTemplateD as TestTemplate2D  # noqa
from template3a import Template as TemplateA              # noqa
from template3b import Template as TemplateB              # noqa
from template3c import Template as TemplateC              # noqa

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, 'templates')


class TestTemplateA(TestTemplate2D):
    """if"""
    Template = TemplateA

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        (
         open('templates/list.html').read(),
         None, {'items': ['item1', 'item2', 'item3']},
         '''<ul>
  
    <li>item1</li>

  
    <li>item2</li>

  
    <li>item3</li>

  
</ul>
'''),   # noqa
    ])
    def test_template3a(self, text, code, context, output):
        template = self.Template(text, template_dir=template_dir)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output


class TestTemplateB(TestTemplateA):
    """if"""
    Template = TemplateB

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        (
         open('templates/child1.html').read(),
         None, {'header': 'child_header'},
         '''<div id="header"> child_header </div>
<div id="footer"> parent_footer </div>
'''),
    ])
    def test_template3b(self, text, code, context, output):
        template = self.Template(text, template_dir=template_dir)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output


class TestTemplateC(TestTemplateB):
    """if"""
    Template = TemplateC

    @pytest.mark.parametrize(('text', 'code', 'context', 'output'), [
        (
         open('templates/child2.html').read(),
         None, None, '<div id="header"> child_header  parent_header  </div>\n'
         ),
    ])
    def test_template3c(self, text, code, context, output):
        template = self.Template(text, template_dir=template_dir)
        if code is not None:
            assert str(template.code_builder) == code
        assert template.render(context) == output
