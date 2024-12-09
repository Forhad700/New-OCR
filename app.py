from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from src.services.ocrServices import ImageTextExtractor

app = Flask(__name__)
swagger = Swagger(app, template_file='apidocs/swagger.yml')  # Ensure the correct path to your Swagger YAML file

@app.route('/')
def index():
    return redirect('apidocs')
@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    """
    Upload an image and extract text from it using multiple OCR engines.
    This endpoint allows you to upload an image directly from Swagger UI.
    ---
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: The image file to extract text from.
    responses:
      200:
        description: Text extracted from the image using multiple OCR engines.
        schema:
          type: object
          properties:
            easyocr:
              type: string
              description: Text extracted using EasyOCR.
      400:
        description: Error message when no image is uploaded or an invalid file is provided.
    """
    if 'image' not in request.files:
        return jsonify(message="No file part"), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify(message="No selected file"), 400

    extractor = ImageTextExtractor()
    image_bytes = file.read()
    try:
        text_easy = extractor.extract_text(image_bytes)

        result = {
            "easyocr": text_easy
        }

        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify(message=f"Error processing image: {str(e)}"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)