import os
import datetime
import csv

def get_template_path(path):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),path)
    if not os.path.isfile(file_path):
        raise Exception("file is not valid path {}".format(file_path))
    return file_path

def get_template(path):
    file_path = get_template_path(path)
    return open(file_path).read()

def render_context(template_text,context):
    return template_text.format(**context)
