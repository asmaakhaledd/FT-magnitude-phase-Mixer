from flask import Flask, make_response, render_template, request, jsonify,  Response
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
    response1 =processor1.display_image(component1)
    processor1_fft=processor1.return_fft()
    component_result1 = processor1.component_result(component1)

    processor2.open_image(image2)
    processor2.perform_fft()
    processor2_fft=processor2.return_fft()
    response2 =processor2.display_image(component2)
    component_result2 = processor2.component_result(component2)

    # mixed_image =processor.mixer(response1,response2,ratio1,ratio2)
    mixed_image =processor.mix_components(component_result1,component_result2,processor1_fft,processor2_fft,ratio1,ratio2)
    
    return Response(response=mixed_image, status=200, mimetype='image/jpeg')
    # mixed_image_bytes = mixed_image.tobytes()

    # response = make_response(mixed_image_bytes)
    # response.headers.set('Content-Type', 'image/jpeg')
    # response.headers.set('Content-Disposition', 'attachment', filename='mixed_image.jpg')

    return response

if __name__ == '__main__':
    app.run(debug=True)