from flask import Flask, render_template

import os
import random

app = Flask(__name__)


@app.route('/')
def index():
    with open('mantras.txt', 'r') as fp:
        mantras = fp.readlines()

    wallpapers = os.listdir('static/wallpapers/')
    return render_template('index.html',
                           mantra=random.choice(mantras),
                           wallpaper_file=random.choice(wallpapers))
