from flask import Flask, render_template, request, jsonify,  Response
from ImageProcessor import ImageProcessor
import io
import cv2
import base64

app = Flask(__name__)
processor = ImageProcessor()


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


if __name__ == '__main__':
    app.run(debug=True)