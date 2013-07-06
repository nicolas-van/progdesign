#!/usr/bin/env python
from pygreen import pygreen
import os.path
import subprocess
import re
from bottle import response

def markdown(*args, **kw):
    from markdown import markdown
    kw.update({
        "extensions": ["headerid", "codehilite"]
    })
    return markdown(*args, **kw)

def generate_index(pygreen, files, selector="body", levels=(1, 2)):
    headers = [('h%d' % x) for x in range(levels[0], levels[1] + 1)]
    from pyquery import PyQuery as pq
    lst = []
    for f in files:
        c = pygreen.file_renderer(f)
        d = pq(c)
        d = d(selector)
        hs = d.find(",".join(headers))
        for el in [pq(x) for x in hs]:
            level = int(el[0].tag[1]) - levels[0]
            text = el.text()
            id = el.attr("id")
            select = lambda lst, nb: lst if nb == 0 else select(lst[-1][2], nb - 1)
            select(lst, level).append((text, "%s#%s" % (f, id), []))

    def it(lst):
        if len(lst) == 0:
            return ""
        tmp = ""
        for i in lst:
            tmp += '<li><a href="%s">%s</a>%s</li>' % (i[1], i[0], it(i[2]))
        return "<ul>%s</ul>" % tmp

    return it(lst)

if __name__ == "__main__":
    pygreen.file_exclusion.append(r".*\.less")

    old_file_renderer = pygreen.file_renderer
    def file_renderer(path):
        if path.split(".")[-1] == "css":
            file_path = os.path.join(pygreen.folder, path)
            less_path = "%s.less" % ".".join(file_path.split(".")[0:-1])
            if not os.path.exists(file_path) and os.path.exists(less_path):
                css = subprocess.check_output(["lessc", less_path])
                response.content_type = 'text/css'
                return css
        return old_file_renderer(path)
    pygreen.file_renderer = file_renderer

    def lister():
        for dirpath, dirnames, filenames in os.walk(pygreen.folder):
            for f in filenames:
                if f.split(".")[-1] == "less" and not re.match(r"(^|.*\/)_.*", f):
                    absp = os.path.join(dirpath, f)
                    path = os.path.relpath(absp, pygreen.folder)
                    css_path = "%s.css" % ".".join(path.split(".")[0:-1])
                    yield css_path
    pygreen.file_listers.append(lister)

    pygreen.cli()


