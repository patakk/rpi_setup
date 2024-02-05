from flask import Flask, request, render_template, redirect, jsonify, url_for
from werkzeug.utils import secure_filename
from inky import Inky_Impressions_7 as Inky
from PIL import Image
import uuid
import os

app = Flask('Inky Impression 7.3" App')
UPLOAD_FOLDER = os.path.join(app.static_folder, 'images')
THUMBNAILS_FOLDER = os.path.join(app.static_folder, 'thumbnails')

THUMBNAIL_SIZE = (256, 256)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAILS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_thumbnail(image_path):
    img = Image.open(image_path)
    img.thumbnail(THUMBNAIL_SIZE)
    basename = os.path.basename(image_path)
    thumbnail_path = os.path.join(THUMBNAILS_FOLDER, basename)
    img.save(thumbnail_path)


def update_display(image_path):
    display = Inky()
    im = Image.open(image_path)
    if im.size[0] < im.size[1]:
        im = im.rotate(90, expand=True)
    
    w0 = 800
    h0 = 480
    om0 = w0/h0
    om = im.size[0]/im.size[1]
    if om > om0:
        nh = h0
        nw = int(nh*om)
        dd = (nw - w0)//2
        im = im.resize((nw, nh))
        im = im.crop((dd, 0, dd+w0, h0))
    elif om < om0:
        nw = w0
        nh = int(nw/om)
        dd = (nh - h0)//2
        im = im.resize((nw, nh))
        im = im.crop((0, dd, w0, dd+h0))
    
    display.set_image(im, saturation=1.0)
    try:
        display.show()
    except RuntimeError:
        pass


def initialize():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not allowed_file(filename):
            continue
        thumbnail_path = os.path.join(THUMBNAILS_FOLDER, filename)
        if not os.path.exists(thumbnail_path):
            create_thumbnail(file_path)


@app.route('/gallery')
def gallery():
    thumbnails = [f for f in os.listdir(THUMBNAILS_FOLDER) if allowed_file(f)]
    return render_template('gallery.html', images=thumbnails)


@app.route('/display_image/<filename>')
def display_image(filename):
    if not allowed_file(filename) or '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Invalid filename'}), 400

    image_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))

    if os.path.exists(image_path):
        update_display(image_path)
        return redirect('/gallery')
    else:
        return jsonify({'error': 'File does not exist'}), 404


@app.route('/', methods=['GET'])
def upload_form():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(str(uuid.uuid4()) + os.path.splitext(file.filename)[-1])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        create_thumbnail(file_path)  # Create thumbnail for the uploaded image
        update_display(file_path)
        return redirect('/')

if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=5000, debug=True)
