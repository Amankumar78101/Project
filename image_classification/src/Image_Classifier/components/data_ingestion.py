
from flask import Flask, render_template
import base64
import os
import shutil
import threading
import uuid
import time
import random
import urllib.request as request
from Image_Classifier import logger  # Import logger
from Image_Classifier.entity.config_entity import DataIngestionConfig
from pathlib import Path


class ImageHandler:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.captureCount = 0

    def remove_folder(self, folder_path):
        def remove():
            logger.info(f"Waiting for 10 minutes before removing the folder '{folder_path}'...")
            time.sleep(600)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"Folder '{folder_path}' removed successfully.")
            else:
                logger.warning(f"The folder '{folder_path}' does not exist.")
        return remove

    def process_request(self, image_data,folder_name,remove_folder_name):
        _, encoded_data = image_data.split(',', 1)
        decoded_image = base64.b64decode(encoded_data)

        os.makedirs(os.path.join(self.config.saved_images,folder_name), exist_ok=True)
        image_filename = str(uuid.uuid4()) + '.png'
        image_path = os.path.join(self.config.saved_images,folder_name, image_filename)

        with open(image_path, 'wb') as f:
            f.write(decoded_image)

        self.captureCount += 1

        if remove_folder_name:
            folder_path = os.path.join(self.config.saved_images,remove_folder_name)
            if os.path.exists(folder_path):
                remove_thread = threading.Thread(target=self.remove_folder(folder_path))
                remove_thread.start()
            else:
                logger.warning(f"The folder '{remove_folder_name}' does not exist.")

        images = [os.path.join(self.config.saved_images,folder_name, image) for image in os.listdir(os.path.join(self.config.saved_images,folder_name))]
        logger.info("Image processed successfully")
        return images

    def split_train_test(self):
        os.makedirs(self.config.train_dir, exist_ok=True)
        os.makedirs(self.config.test_dir, exist_ok=True)

        for class_folder in os.listdir(self.config.saved_images):
            class_path = os.path.join(self.config.saved_images, class_folder)
            if os.path.isdir(class_path):
                train_class_dir = os.path.join(self.config.train_dir, class_folder)
                test_class_dir = os.path.join(self.config.test_dir, class_folder)
                os.makedirs(train_class_dir, exist_ok=True)
                os.makedirs(test_class_dir, exist_ok=True)

                images = os.listdir(class_path)
                random.shuffle(images)

                num_test_images = int(self.config.test_ratio * len(images))
                test_images = images[:num_test_images]
                train_images = images[num_test_images:]

                for image in train_images:
                    src = os.path.join(class_path, image)
                    dest = os.path.join(train_class_dir, image)
                    shutil.move(src, dest)

                for image in test_images:
                    src = os.path.join(class_path, image)
                    dest = os.path.join(test_class_dir, image)
                    shutil.move(src, dest)

                shutil.rmtree(class_path)
        logger.info("Data split into train and test sets")
