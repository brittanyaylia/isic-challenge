from flask import Flask, render_template, jsonify, make_response, Response, request
import numpy as np
from pprint import pprint
import io
import base64
import cv2 as cv
import numpy as np
import os
import tensorflow as tf

app = Flask(__name__)

trained_models = {
    'model1': {'': os.path.join('.', 'Resources', 'cnn_model.h5'), 'dim': (120, 187)},
    'model2': {'path': os.path.join('.', 'Resources', 'em_model-rgb-adam-weighted.h5'), 'dim': (120, 187)}
}

@app.route("/process-image", methods=['POST'])
def predict_image():
    if request.method == 'POST': 
        # first 22 characters general format [data:image/jpeg;base64]
        file_payload = request.get_data()[22:].decode()
        file_token = request.get_data()[:22].decode();

        im_bytes = base64.b64decode(file_payload)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
        
        #todo
        model_details = trained_models['model2'];
        model = load_model(model_details['path'])
        resized_img = cv.resize(img, model_details['dim'])
        prediction = model.predict(resized_img.reshape((1, model_details['dim'][0], model_details['dim'][1])))

        pprint(prediction) 

        return make_response(jsonify({'file_token': file_token, 'img_shape': img.shape}))
    else:
        return make_response(jsonify({'wtf': 'wtf'}))

def resize_image(img):
    pass

def load_model(model):
    pprint(model)
    return tf.keras.models.load_model(model)

def predict_image(img):
    pass

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
