#!/usr/bin/env python
from pygreen import pygreen
import os.path
import subprocess
from bottle import response

pygreen.file_exclusion.append("($|\/)_.*")

old_file_renderer = pygreen.file_renderer
def file_renderer(path):
    if path.split(".")[-1] == "less":
        file_path = os.path.join(pygreen.folder, path)
        css = subprocess.check_output(["lessc", file_path])
        response.content_type = 'text/css'
        return css
    return old_file_renderer(path)
pygreen.file_renderer = file_renderer

pygreen.cli()
