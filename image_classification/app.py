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
            
    return render_template('index.html')


@app.route('/submit_configuration', methods=['GET', 'POST'])
def submit_configuration():
    if request.method == 'POST':
        try:
            model_name = request.form['model_name']
            freeze_all = request.form.get('freeze_all')
            freeze_till = request.form['freeze_till']
            image_size = [int(x) for x in request.form['image_size'].strip('[]').split(',')]
            include_top = request.form.get('include_top')
            weights = request.form['weights']
            neural = int(request.form.get('neural', 2))
            epochs = int(request.form.get('epochs', 1))
            loss = request.form['loss']
            optimizer = request.form['optimizer']
            learning_rate = float(request.form.get('learning_rate', 0.01))
            augmentation = bool(request.form.get('augmentation'))
            batch_size = int(request.form.get('batch_size', 128))
            
            # Process the configuration parameters...
            
            return jsonify(success=True)
        except Exception as e:
            logger.exception("Failed to process configuration: %s", e)
            return jsonify(error='Failed to process configuration: %s' % e), 500
    return render_template('Prepare_model_params.html')


if __name__ == '__main__':
    app.run(debug=True)



