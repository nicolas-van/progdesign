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


