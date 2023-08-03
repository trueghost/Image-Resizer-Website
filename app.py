from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change_resolution', methods=['POST'])
def change_resolution():
    if 'image' not in request.files:
        return "No image uploaded!", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image selected!", 400

    try:
        desired_width = int(request.form['desired_width'])
        desired_height = int(request.form['desired_height'])
    except ValueError:
        return "Invalid desired resolution!", 400

    img = Image.open(image_file) # type: ignore
    img = img.resize((desired_width, desired_height))

    output_io = io.BytesIO()
    img.save(output_io, format='JPEG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)