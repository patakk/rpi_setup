from inky import Inky_Impressions_7 as Inky
from PIL import Image
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

THUMBNAIL_SIZE = (256, 256)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
THUMBNAILS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'thumbnails')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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
    
    display.set_image(im, saturation=.76)
    try:
        display.show()
    except RuntimeError:
        pass