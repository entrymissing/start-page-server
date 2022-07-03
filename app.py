from flask import Flask, render_template

import os
import random

app = Flask(__name__)

mantras = ['What is draining my energy?',
           'Small improvements accumulate and gain interest.']


@app.route('/')
def index():
    wallpapers = os.listdir('static/wallpapers/')
    return render_template('index.html', 
                           mantra=random.choice(mantras),
                           wallpaper_file=random.choice(wallpapers))


if __name__ == '__main__':
    app.run()
