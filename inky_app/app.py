from flask import Flask, request, render_template_string, redirect, url_for
from inky import Inky_Impressions_7 as Inky
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/path/to/uploaded/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            update_display(filename)
            return redirect(url_for('upload_file'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
