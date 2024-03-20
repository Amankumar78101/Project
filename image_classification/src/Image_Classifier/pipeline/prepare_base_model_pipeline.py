from Image_Classifier.config.configuration import ConfigurationManager
from Image_Classifier.components.prepare_base_model import PretrainTrainModel
from Image_Classifier import logger

STAGE_NAME = "Prepare base model"

def main():
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")

        config_manager = ConfigurationManager()

        pre_base_model_config = config_manager.get_prepare_base_model_config()

        prepare_base_model = PretrainTrainModel(config=pre_base_model_config)

        prepare_base_model.get_base_model()

        prepare_base_model.update_base_model()

        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(f"Error occurred in stage {STAGE_NAME}: {str(e)}")
        raise e

if __name__ == '__main__':
    main()
