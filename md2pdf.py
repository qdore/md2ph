#!/usr/bin/python
import sys
import markdown2
import os
import string
import re
#from pygments.lexers.compiled import JavaLexer, CLexer, CppLexer
from pygments.lexers.asm import CppLexer
from pygments.lexers.jvm import JavaLexer
import os.path
from pygments.lexers.agile import PythonLexer
import pygments
from pygments.formatters.html import HtmlFormatter
from BeautifulSoup import *
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')
nohl = False
codehl="default"
def rev2html(str, path, filename):
    title = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>
'''
    html = '''</title>
<link rel="stylesheet" href="file///usr/local/Cellar/wkhtmltox/css/base.css" />
</head>
<body><div class="container">
'''
    end = '''
</div></body>
</html>'''
    filenext = os.path.splitext(filename)
    file = open(path + '/' + filenext[0] + '.html', 'w+')
    file.writelines(title)
    file.write(filenext[0])
    file.writelines(html)
    file.writelines(str)
    file.writelines(end)
    file.close()



def rev2pdf(str, path, filename):
    title = '''<html>
<head>
<meta charset="utf-8">
<title>
'''
    html = '''</title>
<link rel="stylesheet" href="http://localhost:880/base.css" />
</head>
<body class="container">
'''
    end = '''</body>
</html>'''
    filenext = os.path.splitext(filename)
    file = open(path + '/' + filenext[0] + '.html.html', 'w+')
    file.writelines(title)
    file.write(filenext[0])
    file.writelines(html)
    file.writelines(str)
    file.writelines(end)
    file.close()
    os.system('/usr/local/Cellar/wkhtmltox/bin/wkhtmltopdf --margin-top 25mm --margin-left 20mm --margin-right 20mm --margin-bottom 20mm ' \
              + path + '/' + filenext[0] + '.html.html ' \
              + path + '/' + filenext[0] + '.pdf' + ' 2>/dev/null')
    os.remove(path + '/' + filenext[0] + '.html.html')

def pretreat(fi):
    with open(fi) as fd:
        test = False;
        str = ''
        for lines in fd:
            if test:
                lines = '\t' + lines
            if "```" in lines:
                test = ~test
                lines = '\n'
            else:
                if not test:
                    if '#' in lines:
                        lines = lines + '\n'
            str = str + lines
    return str
def change(code):
    code = code.replace('&lt;', 'kdhfgkjdshfjghd')
    code = code.replace('&gt;', 'oaakjsadhfkjdsh')
    lex = pygments.lexers.guess_lexer(code)
    if codehl == 'python':
        lex = PythonLexer()
    if codehl[0] is 'c':
        lex = CppLexer()
    if codehl == 'java':
        lex = JavaLexer()
    code = pygments.highlight(code, lex, HtmlFormatter())
    code = code[code.find('<pre>') + 5: code.find('</pre>')]
    code = code.replace('kdhfgkjdshfjghd', '&lt;')
    code = code.replace('oaakjsadhfkjdsh', '&gt;')
    return '<code>' + code + '</code>'

def htmlresove(str):
    soup = BeautifulSoup(str)
    for codes in soup.findAll('code'):
        codes.replaceWith(BeautifulSoup(change(codes.text)))
    return unicode(soup)



for i in range(1 ,len(sys.argv)):
    if  '-nohl' in sys.argv[i]:
        nohl = True
    if  '-' in sys.argv[i]:
        if  'nohl' not in sys.argv[i]:
            codehl = sys.argv[i].replace('-' ,'')
            codehl = codehl.lower()


for i in range(1 ,len(sys.argv)):
    if  '-' == sys.argv[i][0]:
        continue
    str = pretreat(sys.argv[i])
    str = markdown2.markdown(str, extras=["footnotes"])
    if nohl is False:
        str = htmlresove(str)
    rev2pdf(str ,'.', os.path.split(sys.argv[i])[1])

