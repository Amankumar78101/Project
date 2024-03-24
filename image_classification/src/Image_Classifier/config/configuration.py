
import os
from pathlib import Path
from flask import request

from Image_Classifier.utils.utils import read_yaml, create_dir
from Image_Classifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from Image_Classifier.entity.config_entity import DataIngestionConfig,PrepareBaseModelConfig,PrepareCallbacksConfig,TrainingConfig,EvaluationConfig
from Image_Classifier import logger  

class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH
    ):
        """
        Initialize ConfigurationManager with folder names and file paths.

        Args:
            config_filepath (str): Path to the configuration file.
            params_filepath (str): Path to the parameters file.
        """
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_dir([self.config.artifacts_root])
        logger.info('Artifact folder created')

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Get data ingestion configuration.

        Returns:
            DataIngestionConfig: Data ingestion configuration object.
        """
        config = self.config.data_ingestion
        params = self.params
        data_ingestion_config = DataIngestionConfig(
            saved_images=config.saved_images,
            train_dir=config.train_dir,
            test_dir=config.test_dir,
            test_ratio=params.TEST_RATIO
            )
        logger.info("Data ingestion configuration loaded successfully")
        return data_ingestion_config
    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_dir([config.root_dir_pre_model])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir_pre_model=Path(config.root_dir_pre_model),
            updated_model=Path(config.updated_model),
            params_image_size=self.params.IMAGE_SIZE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_neural=self.params.NEURAL,
            params_loss=self.params.LOSS,
            params_optimizer=self.params.OPTIMIZER,
            params_learning_rate=self.params.LEARNING_RATE,
            model_name=self.params.MODEL_NAME,
            freeze_all=self.params.FREEZE_ALL,
            freeze_till=self.params.FREEZE_TILL

        )
        return prepare_base_model_config
    def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
        config = self.config.prepare_callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_dir([
            Path(model_ckpt_dir),
            Path(config.tensorboard_root_log_dir)
        ])

        prepare_callback_config = PrepareCallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)
        )

        return prepare_callback_config

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params
        self.training_data = os.path.join(self.config.data_ingestion.saved_images, "saved_images")
        create_dir([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(prepare_base_model.updated_model),
            training_data=Path(self.training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )

        return training_config
    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model=self.config.training.trained_model_path,
            training_data=self.config.Evaluation.training_data,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return eval_config