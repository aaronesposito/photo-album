from flask import Flask, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__)
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.arw'}


@app.route('/')
def index():
    return redirect(url_for('pagination', page=1))

@app.route('/album/<int:page>')
def pagination(page):
    image_folder = os.path.join('static', 'images')
    images = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
    end = 0
    paginated_images = []
    while end < len(images):
        end += 10
        if end > len(images):
            paginated_images.append(images[end-10:len(images)-1])
        else:
            paginated_images.append(images[end-10: end])
    print(page)

    return render_template('index.html', images=paginated_images[page-1], pages=len(paginated_images))

@app.route('/images/<filename>')
def image(filename):
    return send_from_directory(os.path.join('static', 'images'), filename)
