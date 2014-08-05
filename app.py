import os
from flask import Flask, render_template
import subprocess
import sys, os, glob

app = Flask(__name__)
app.debug = True

PWD = '/home/wjm/repos/design-in-browser'
TEMPLATE_DIR = os.path.join(PWD, "templates")

extra_dirs = [os.path.join(PWD, 'sass'), ]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)

WIDGET_PATH = os.path.join(TEMPLATE_DIR, 'widgets/')
widgets = sorted([os.path.relpath(os.path.join(dp, f), TEMPLATE_DIR)
                  for dp, _, filenames in os.walk(WIDGET_PATH)
                  for f in filenames
                  if os.path.splitext(f)[1] == '.html'])

PAGES_PATH = os.path.join(TEMPLATE_DIR, 'pages/')
pages = sorted([os.path.relpath(os.path.join(dp, f), TEMPLATE_DIR)
                for dp, _, filenames in os.walk(PAGES_PATH)
                for f in filenames
                if os.path.splitext(f)[1] == '.html'])


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/pages')
def pages(pages=pages):
    return render_template('pages-index.html', pages=pages)


@app.route('/pages/<page_name>')
def render_page(page_name):
    return render_template('pages/{}'.format(page_name))


@app.route('/widgets')
def widgets(widgets=widgets):
    return render_template('widget-index.html', widgets=widgets)


@app.route('/widgets/<widget_name>')
def render_widget(widget_name):
    return render_template('widgets/{}'.format(widget_name))


# Utility Functions
def reload_compass(pwd=PWD):
    with subprocess.Popen(['compass', 'compile'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=pwd) as p:
        stdout, stderr = p.communicate()
        print("-- COMPASS SAYS --", file=sys.stdout)
        print(stderr.decode(errors='replace'), file=sys.stdout)
        print(stdout.decode(errors='replace'), file=sys.stdout)


if __name__ == "__main__":
    reload_compass(PWD)
    app.run(extra_files=extra_files)
