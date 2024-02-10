from flask import Flask, request, render_template, redirect, jsonify
from werkzeug.utils import secure_filename
import uuid
import os
import base64
from shared import allowed_file
from shared import update_display
from shared import create_thumbnail
from shared import UPLOAD_FOLDER
from shared import THUMBNAILS_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAILS_FOLDER, exist_ok=True)

app = Flask('Inky Impression 7.3" App')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/canvas')
def canvas():
    return render_template('canvas.html')


import glob


def get_image_folder_state():
    paths = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
    paths = [p for p in paths if allowed_file(os.path.basename(p))]
    paths.sort(key=os.path.getctime)
    return paths


@app.route('/display_image/<filename>')
def display_image(filename):
    if not allowed_file(filename) or '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Invalid filename'}), 400

    image_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))

    if os.path.exists(image_path):
        print('image from gallery')
        images = get_image_folder_state()
        current_idx = images.index(image_path)
        print(f'{current_idx+1} / {len(images)}')
        with open('../current_img_idx', 'w') as f:
            f.write(str(current_idx))

        update_display(image_path)
        return jsonify({'success': 'Image changed'}), 200
    else:
        return jsonify({'error': 'File does not exist'}), 404


@app.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')


@app.route('/upload_canvas', methods=['POST'])
def upload_canvas_image():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data'}), 400

    # Strip the header of base64 string
    image_data = data['image'].split(';base64,')[-1]

    try:
        image_bytes = base64.b64decode(image_data)
        filename = secure_filename(str(uuid.uuid4()) + '.png')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(image_bytes)

        create_thumbnail(file_path)

        with open('../current_img_idx', 'w') as f:
            f.write(str(len(os.listdir(UPLOAD_FOLDER)) - 1))

        update_display(file_path)
        print('canvas image saved')
        return jsonify({'success': 'Image saved', 'filename': filename}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
        print('new file saved')
        create_thumbnail(file_path)

        with open('../current_img_idx', 'w') as f:
            f.write(str(len(os.listdir(UPLOAD_FOLDER)) - 1))

        update_display(file_path)
        return redirect('/')
        # return jsonify({'success': 'Image uploaded'}), 200

import sys
if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=80, debug=False)
