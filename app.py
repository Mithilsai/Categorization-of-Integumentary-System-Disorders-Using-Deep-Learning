from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
from PIL import Image,ImageEnhance

from tensorflow.keras.models import load_model
# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
MODEL_PATH = 'skin_model2.h5'
model = load_model(MODEL_PATH)
print('Model loaded. Check http://127.0.0.1:5000/')

def softmax(x):
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x
class_list=['Psoriasis','Measles','Melanoma','Ringworm']

def predicting(fp, model):
    img=Image.open(fp)
    target_size=(224,224)
    
    if img.size != target_size:
        img = img.resize(target_size)
    enhancer = ImageEnhance.Contrast(img)
    factor=2.5
    img = enhancer.enhance(factor)
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.inception_v3.preprocess_input(x)
    preds = model.predict(x)
    tem_ar=softmax(preds[0])
    return class_list[tem_ar.argmax()] 

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
@app.route('/second', methods=['GET', 'POST'])
def second():
    return render_template('page.html')
@app.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('data.html')
@app.route('/pdf',  methods=['GET', 'POST'])
def pdf():
    return render_template('pdf.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = predicting(file_path, model)

        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)

