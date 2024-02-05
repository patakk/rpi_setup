
import RPi.GPIO as GPIO
import signal
import random
import glob
import os

from inky_app.app import allowed_file
from inky_app.app import update_display


UPLOAD_FOLDER = 'inky_app/static/images'

BUTTON_LABEL_DICT = {
    5: 'A',
    6: 'B',
    16: 'C',
    24: 'D'
}

def get_image_folder_state():
    paths = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
    paths = [p for p in paths if allowed_file(os.path.basename(p))]
    paths.sort(key=os.path.getctime)
    return paths


def random_image():
    print('Random Image')
    images = get_image_folder_state()
    current_idx = random.randint(0, len(images)-1)
    print(f'{current_idx+1} / {len(images)}')
    image = images[current_idx]
    with open('current_img_idx', 'w') as f:
        f.write(str(current_idx))
    print(image)
    update_display(image)


def next_image():
    print('Next Image')
    images = get_image_folder_state()
    current_idx = int(open('current_img_idx', 'r').read())
    current_idx = (current_idx+1+len(images)) % len(images)
    print(f'{current_idx+1} / {len(images)}')
    image = images[current_idx]
    with open('current_img_idx', 'w') as f:
        f.write(str(current_idx))
    print(image)
    update_display(image)


def prev_image():
    print('Previous Image')
    images = get_image_folder_state()
    current_idx = int(open('current_img_idx', 'r').read())
    current_idx = (current_idx-1+len(images)) % len(images)
    print(f'{current_idx+1} / {len(images)}')
    image = images[current_idx]
    with open('current_img_idx', 'w') as f:
        f.write(str(current_idx))
    print(image)
    update_display(image)


def handle_button(pin):
    label = BUTTON_LABEL_DICT[pin]
    if str(label) == 'A':
        random_image()
    elif str(label) == 'B':
        next_image()
    elif str(label) == 'C':
        prev_image()
    elif str(label) == 'D':
        random_image()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(list(BUTTON_LABEL_DICT.keys()), GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for pin in BUTTON_LABEL_DICT:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

    signal.pause()

if __name__ == '__main__':
    setup()