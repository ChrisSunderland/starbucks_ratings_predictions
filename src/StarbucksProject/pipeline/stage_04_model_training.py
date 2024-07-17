from src.StarbucksProject.config.configuration import ConfigurationManager
from src.StarbucksProject.components.model_training import ModelTrainer
from src.StarbucksProject import logger


class ModelTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        try:

            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.train()

        except Exception as e:
            raise e


if __name__ == '__main__':

    STAGE_NAME = "Model Training Stage"

    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        mt_pipe = ModelTrainingPipeline()
        mt_pipe.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e