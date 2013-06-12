#!/usr/bin/env python
from pygreen import pygreen
import os.path
import subprocess
from bottle import response

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

pygreen.cli()
