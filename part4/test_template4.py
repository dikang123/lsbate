# -*- coding: utf-8 -*-
import os
import sys

import pytest

sys.path.insert(0, '../part3/')

from template4a import Template as TemplateA              # noqa
from template4b import Template as TemplateB              # noqa
from template4c import Template as TemplateC              # noqa

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, 'templates')


class TestTemplateA:
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
        (
         open('templates/child1.html').read(),
         None, {'header': 'child_header'},
         '''<div id="header"> child_header </div>
<div id="footer"> parent_footer </div>
'''),
        (
         open('templates/child2.html').read(),
         None, None, '<div id="header"> child_header  parent_header  </div>\n'
         ),
        (
         '<h1>{{ title }}</h1>',
         None, {'title': 'hello<br />world'},
         '<h1>hello&lt;br /&gt;world</h1>'
         ),   # noqa
        (
         '<h1>{{ noescape(title) }}</h1>',
         None, {'title': 'hello<br />world'},
         '<h1>hello<br />world</h1>'
        ),
    ])
    def test_template4a(self, text, code, context, output):
        template = self.Template(text, template_dir=template_dir)
        assert template.render(context) == output


class TestTemplateB(TestTemplateA):
    Template = TemplateB

    def test_template4b(self):
        template = self.Template('{{ open("/etc/passwd").read() }}')
        with pytest.raises(NameError):
            template.render()

    def test_template4b_issue(self):
        t = self.Template('{{ escape.__globals__["__builtins__"]["open"]("/etc/passwd").read()[0] }}')  # noqa
        t.render()


class TestTemplateC(TestTemplateB):
    Template = TemplateC

    def test_template4b_issue(self):
        pass

    def test_template4c(self):
        template = self.Template('{{ escape.__globals__["__builtins__"]["open"]("/etc/passwd").read()[0] }}')  # noqa
        with pytest.raises(AttributeError):
            template.render()
