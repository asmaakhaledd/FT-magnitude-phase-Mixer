from flask import Flask, render_template, request, jsonify
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
    file1 = request.files['file1']
    file2 = request.files['file2']
    component1 = request.form['component1']
    component2 = request.form['component2']
    ratio = int(request.form['ratio'])

    # Open and process images
    if not processor.open_image(file1) or not processor.check_size(processor.open_image(file2)):
        return jsonify({'error': 'Failed to open images or image sizes do not match'})
    output = processor.mix_components(processor.image, component1, component2, ratio)

    # Convert output image to base64 string for display
    output_buffer = io.BytesIO()
    output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(output_buffer, output)
    output_buffer.seek(0)
    output_base64 = base64.b64encode(output_buffer.read()).decode('utf-8')

    return jsonify({'output': output_base64})

if __name__ == '__main__':
    app.run(debug=True)