src\Image_Classifier\components\data_ingestion.py

from flask import Flask, render_template, request
import base64
import os
import shutil
import threading
import uuid
import time

class ImageHandler:
    def __init__(self):
        self.captureCount = 0

    def remove_folder(self, folder_path):
        # Function to remove the folder after 10 minutes
        def remove():
            print(f"Waiting for 10 minutes before removing the folder '{folder_path}'...")
            # Wait for 10 minutes
            time.sleep(600)
            # Check if the folder exists before trying to remove it
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                print(f"Folder '{folder_path}' removed successfully.")
            else:
                print(f"The folder '{folder_path}' does not exist.")
        return remove

    def process_request(self):
        if request.method == 'POST':
            image_data = request.form['image']
            folder_name = request.form['folder'].strip()
            remove_folder_name = request.form.get('remove_folder')

            _, encoded_data = image_data.split(',', 1)
            decoded_image = base64.b64decode(encoded_data)

            saved_images = 'artifacts/data_ingestion/saved_images'

            # Create the directory if it doesn't exist
            os.makedirs(os.path.join(saved_images, folder_name), exist_ok=True)
            image_filename = str(uuid.uuid4()) + '.png'
            image_path = os.path.join(saved_images, folder_name, image_filename)

            with open(image_path, 'wb') as f:
                f.write(decoded_image)

            self.captureCount += 1

            if remove_folder_name:
                folder_path = os.path.join(saved_images, remove_folder_name)
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                else:
                    print(f"The folder '{remove_folder_name}' does not exist.")

            # Schedule folder removal if a new folder is created
            if not remove_folder_name:
                folder_path = os.path.join(saved_images, folder_name)
                threading.Thread(target=self.remove_folder(folder_path)).start()

            # Get all the image URLs in the folder
            images = [os.path.join(saved_images, folder_name, image) for image in os.listdir(os.path.join(saved_images, folder_name))]

            # Pass the list of image URLs to the template
            return render_template('index.html', images=images)

        return render_template('index.html', images=[])

