from flask import Flask, render_template, request, jsonify
from pathlib import Path
from Image_Classifier.config.configuration import ConfigurationManager
from Image_Classifier.components.data_ingestion import ImageHandler
from Image_Classifier import logger

app = Flask(__name__)

# Initialize configuration manager and image handler
config_manager = ConfigurationManager()
data_ingestion_config = config_manager.get_data_ingestion_config()
image_handler = ImageHandler(data_ingestion_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if 'image_data', 'folder', and 'remove_folder' are present in the request form
        if 'image_data' in request.form and 'folder' in request.form and 'remove_folder' in request.form:
            image_data = request.form['image_data']
            folder_name = request.form['folder']
            remove_folder_name = request.form['remove_folder']
            image_urls = image_handler.process_request(image_data, folder_name, remove_folder_name)

            return jsonify(images=image_urls)
        else:
            return jsonify(error='Missing form data'), 400
    
    # This line should be outside of the if block
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
