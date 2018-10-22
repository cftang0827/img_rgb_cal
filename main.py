from werkzeug import secure_filename
from flask import Flask, redirect, request, url_for, Response
import json
import os
import sys
import numpy as np
import cv2


if os.path.isdir('tmp') is False:
    os.mkdir('tmp')
UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = set(
    ['png', 'jpg', 'JPEG', 'JPG', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result_list = []
    if request.method == 'POST':
        file_list = request.files.getlist("file")
        for file in file_list:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result_list.append(
                    cal(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            else:
                result_list.append({
                    'file_name': file.filename,
                    'error': 'Not allowd file type, only accept {}'.format(ALLOWED_EXTENSIONS)
                })
        return Response(json.dumps(result_list, indent=4), mimetype='application/json')
    return '''
    <!doctype html>
    <title>RGB calculator</title>
    <h1>RGB calculator</h1>
    <form action="/" method=post name="file" id="name" enctype=multipart/form-data>
      <p><input type=file multiple="" name=file>
         <input type=submit value=Upload>
    </form>
    '''


def cal(file_name):
    img = cv2.imread(file_name)[:, :, ::-1]
    img_size = img.shape[:2]
    r_sum = float(np.sum(img[:, :, 0]))
    g_sum = float(np.sum(img[:, :, 1]))
    b_sum = float(np.sum(img[:, :, 2]))

    overall_pixel = r_sum + g_sum + b_sum
    r_percent = round(r_sum * 100 / overall_pixel, 3)
    g_percent = round(g_sum * 100 / overall_pixel, 3)
    b_percent = round(b_sum * 100 / overall_pixel, 3)

    result = {}
    result['file_name'] = file_name.split('/')[-1]
    result['photo_size'] = '{}x{}'.format(img_size[0], img_size[1])
    result['r/g/b'] = '{}% /{}% /{}%'.format(r_percent, g_percent, b_percent)

    return result


if __name__ == '__main__':
    app.run(host='localhost', port=9527, debug=False, threaded=True)
