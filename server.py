import os
from os import listdir
from os.path import isfile, join

import time
from PIL import Image
from flask import send_file, request, app

from flask import Flask
app = Flask(__name__)


def gen_name(images):
    name = ""
    for part in PART_ONLY:
        if any(part in s for s in images if
               part == s.replace('-low', '').replace('-medium', '').replace('-high', '').replace('-replace', '')):
            full_part = [s for s in images if
                         part == s.replace('-low', '').replace('-medium', '').replace('-high', '').replace('-replace',
                                                                                                           '')]
            if len(full_part) > 1:
                # print(full_part)
                return 'same'
            if 'low' in full_part[0]:
                name += str(1)
            elif 'medium' in full_part[0]:
                name += str(2)
            elif 'high' in full_part[0]:
                name += str(3)
            elif 'replace' in full_part[0]:
                name += str(4)
            else:
                return "?????????"
        else:
            name += str(0)
    # print(name)
    return name + '.jpg'


def gen_image(path, parts, base_path, name):
    size = 240, 240
    background = Image.open(base_path)
    for part in parts:
        print(part)
        foreground = Image.open(path + '/' + part + '.png')
        background.paste(foreground, (0, 0), foreground)
    # background.show()
    background.thumbnail(size, Image.ANTIALIAS)
    rgb_im = Image.new("RGB", background.size, (255, 255, 255))
    rgb_im.paste(background, (0, 0), background)
    rgb_im.save(name, "JPEG")
    # base = cv2.imread("C:\\Users\\wit543\\horribilis\\exitum\\ivaa_frontend\\static\\car\\base\\back.png")
    # img2 = cv2.imread(path + '/' + part + '.png')
    # # I want to put logo on top-left corner, So I create a ROI
    # rows, cols, channels = img2.shape
    # roi = base[0:rows, 0:cols]
    # # Now create a mask of logo and create its inverse mask also
    # img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    # mask_inv = cv2.bitwise_not(mask)
    # # Now black-out the area of logo in ROI
    # img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # # Take only region of logo from logo image.
    # img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
    # print(base.shape)
    # dst = cv2.add(img1_bg,img2_fg)
    # cv2.imshow('res', dst)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def gen(parts, part_image_path, base_image_path, output_path):
    onlyfiles = [f.split('.')[0] for f in listdir(part_image_path) if isfile(join(part_image_path, f))]
    parts = [part for part in parts if part in onlyfiles]
    name = gen_name(parts)
    if name != 'same':
        name = output_path + '/' + name
        gen_image(part_image_path, parts, base_image_path, name)
        return name
    return None

def gen_side(parts, side):
    sides = ['front', 'back', 'left', 'right']
    if side not in sides:
        return
    path = "./images/" + side
    base_path = "./images/base/" + side + ".png"
    output_path = "./images-out/" + side
    name = gen(parts, path, base_path, output_path)
    if not name:
        return base_path
    return name


@app.route('/get_image')
def get_image():
    parts = str(request.args.get('parts')).split(',')
    side = request.args.get('side')
    if not side:
        return
    filename = gen_side(parts, side)
    return send_file(filename, mimetype='image/jpg')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
