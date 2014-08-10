from operator import itemgetter
from itertools import groupby
from collections import OrderedDict
import os, time
from flask import Flask, render_template, g
import subprocess
import sys, os

PWD = os.getcwd()
TEMPLATE_DIR = os.path.join(PWD, "templates")

# Utility Functions
def reload_compass(pwd=PWD):
    with subprocess.Popen(['compass', 'compile'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=pwd) as p:
        stdout, stderr = p.communicate()
        print("-- COMPASS SAYS --", file=sys.stdout)
        print(stderr.decode(errors='replace'), file=sys.stdout)
        print(stdout.decode(errors='replace'), file=sys.stdout)


def get_watch_file_additions(path=PWD):
    extra_dirs = [
        os.path.join(PWD, 'sass'),
        ]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    return extra_files

def add_dib_structure(app):
    """
    This just grabs the template directory and loads in into dictionary. Really only used to make creating the navbar
    more bareable. It's likely that this is already available in flask/g
    :param template_dir: location of template directory
    :return: dict of it's layout
    """
    loaded_templates = [i for i in map(os.path.split, app.jinja_env.list_templates(extensions='html'))]
    dib_tmp = OrderedDict()
    tmps = sorted([(folder, sorted([ template for _, template in templates]))
                   for folder, templates in groupby(loaded_templates, key=itemgetter(0))])

    for k, v in tmps:
        w = []
        for template in v:
            w.append({'name': template, 'path': os.path.join(k, template)})

        if k in dib_tmp.keys():
            dib_tmp[k] += w
        else:
            dib_tmp[k] = w

    app.jinja_env.globals['dib_tmp'] = dib_tmp
    for k, v in dib_tmp.items():
        print("key: {}".format(k))
        print(v)


app = Flask(__name__)
app.debug = True
add_dib_structure(app)
# new comment
@app.route("/")
def index():
    return render_template('dib/dib-index.html', )


@app.route('/pages')
def pages_index():
    return render_template('dib/dib-pages-index.html')


@app.route('/pages/<page_name>')
def page_render(page_name):
    print("page_name: {}".format(page_name))
    return render_template('pages/{}'.format(page_name))


@app.route('/widgets')
def widgets_index():
    return render_template('dib/dib-widget-index.html')


@app.route('/widgets/<name>')
def widget_render(name):
    print(name)
    return render_template('widgets/{}'.format(name))


if __name__ == "__main__":
    reload_compass(PWD)
    app.run(extra_files=get_watch_file_additions(path=PWD))
