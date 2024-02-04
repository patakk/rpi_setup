from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from inky import Inky_Impressions_7 as Inky
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/home/paolo/inky_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_display(image_path):
    display = Inky()
    im = Image.open(image_path)
    if im.size[0] < im.size[1]:
        im = im.rotate(90, expand=True)
    im = im.resize((800, 480))
    display.set_image(im)
    try:
        display.show()
    except RuntimeError:
        pass

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
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        update_display(file_path)
        return jsonify({'message': 'File uploaded and display updated successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

