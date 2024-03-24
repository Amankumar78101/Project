

from tensorflow import keras
from keras import applications, layers
import tensorflow as tf
from keras import applications
from pathlib import Path
from Image_Classifier import logger


from Image_Classifier.entity.config_entity import PrepareBaseModelConfig

class PretrainTrainModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
        self.full_model = None  # Initialize full_model

    def get_base_model(self):
        try:
            logger.info("Base model loading started")
            model_name = 'VGG16'
            model = getattr(applications, model_name)
            self.base_model = model(
                input_shape=self.config.params_image_size,
                weights=self.config.params_weights,
                include_top=self.config.params_include_top  # Set to False to exclude the final dense layers
                )

            logger.info("Base model loaded")  # Moved this line after model loading
            return self.base_model 
        except Exception as e:
            logger.exception(e)
            raise e

    @staticmethod
    def prepare_full_model(base_model, No_of_neural, freeze_all, freeze_till, learning_rate, loss, optimizer):
        try:
            if freeze_all:
                for layer in base_model.layers:
                    layer.trainable = False
            elif freeze_till is not None and freeze_till > 0:
                for layer in base_model.layers[:-freeze_till]:
                    layer.trainable = False

            flatten_in = layers.Flatten()(base_model.output)
            ANN = layers.Dense(
                units=No_of_neural,
                activation='relu'
            )(flatten_in)
            ANN1 = layers.Dense(
                units=No_of_neural,
                activation='softmax'
            )(ANN)

            full_model = keras.models.Model(
                inputs=base_model.input,
                outputs=ANN1
            )

            full_model.compile(
                optimizer=optimizer,
                loss=loss,
                metrics=["accuracy"]
            )

            full_model.summary()
            return full_model
        except Exception as e:
            logger.exception(e)
            raise e

    def update_base_model(self):
        try:
            logger.info('Base model updated to data')
            self.full_model = self.prepare_full_model(
                base_model=self.base_model,
                No_of_neural=self.config.params_neural,  # Adjust this value
                freeze_all=self.config.freeze_all,
                freeze_till=self.config.freeze_till,
                learning_rate=self.config.params_learning_rate,
                loss=self.config.params_loss,
                optimizer=self.config.params_optimizer
            )


            # Uncomment and use your save_model function
            self.save_model(path=self.config.updated_model, model=self.full_model)
            logger.info('Base model updated and save completed ')
        except Exception as e:
            logger.exception(e)
            raise e
        
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

