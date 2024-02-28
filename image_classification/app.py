
from flask import Flask, render_template, request
import base64
import os
import shutil
import threading
import uuid
import time

from src.Image_Classifier.components.data_ingestion import ImageHandler

app = Flask(__name__)



image_handler = ImageHandler()

@app.route('/', methods=['GET', 'POST'])
def index():
    return image_handler.process_request()

if __name__ == '__main__':
    app.run(debug=True)
