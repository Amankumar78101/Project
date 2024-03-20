
import os
from pathlib import Path
from flask import request

from Image_Classifier.utils.utils import read_yaml, create_dir
from Image_Classifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from Image_Classifier.entity.config_entity import DataIngestionConfig,PrepareBaseModelConfig
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
