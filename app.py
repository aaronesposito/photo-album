from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.arw'}

@app.route('/')
def index():
    image_folder = os.path.join('static', 'images')
    images = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
    return render_template('index.html', images=images)

@app.route('/images/<filename>')
def image(filename):
    return send_from_directory(os.path.join('static', 'images'), filename)
