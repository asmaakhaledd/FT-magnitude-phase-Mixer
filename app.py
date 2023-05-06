from flask import Flask, render_template, request, jsonify,  Response
from ImageProcessor import ImageProcessor
import io
import cv2
import base64

app = Flask(__name__)
processor = ImageProcessor()
processor1 = ImageProcessor()
processor2 = ImageProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    # Get user inputs
    file = request.files['file']
    component = request.form['component']
    processor.open_image(file)
    processor.perform_fft()
    response =processor.display_image(component)
    return Response(response=response, status=200, mimetype='image/jpeg')

@app.route('/fftmixer', methods=['POST'])
def fftmixer():
    image1 = request.files['image1']
    image2 = request.files['image2']
    component1 = request.form['component1']
    component2 = request.form['component2']
    ratio1 = request.form['ratio1']
    ratio2 = request.form['ratio2']

    processor1.open_image(image1)
    processor1.perform_fft()
    processor1_fft=processor1.return_fft()
    component_result1 = processor1.component_result(component1)
    
    processor2.open_image(image2)
    processor2.perform_fft()
    processor2_fft=processor2.return_fft()
    component_result2 = processor1.component_result(component2)

    response = processor.mix_components(component_result1,component_result2,processor1_fft,processor2_fft,ratio1,ratio2)

    return Response(response=response, status=200, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)