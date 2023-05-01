from flask import Flask, render_template, request, send_from_directory
from image_processor import ImageProcessor
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image1 = request.files['image1']
    image2 = request.files['image2']
    component1 = request.form['component1']
    component2 = request.form['component2']
    ratio = float(request.form['ratio'])

    processor1 = ImageProcessor()
    processor2 = ImageProcessor()

    if not processor1.open_image(image1) or not processor2.open_image(image2):
        return "Error opening images", 400

    if not processor1.check_size(processor2.image):
        return "Image sizes do not match", 400

    output_image = processor1.mix_components(processor2.image, component1, component2, ratio)
    output_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}.png")
    cv2.imwrite(output_filename, output_image)

    return send_from_directory(app.config['UPLOAD_FOLDER'], output_filename)

if __name__ == '__main__':
    app.run(debug=True)
