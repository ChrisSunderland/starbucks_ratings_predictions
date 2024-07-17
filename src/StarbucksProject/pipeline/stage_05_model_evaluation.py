from src.StarbucksProject.config.configuration import ConfigurationManager
from src.StarbucksProject.components.model_evaluation import ModelEvaluation
from src.StarbucksProject import logger
from dotenv import load_dotenv


class ModelEvaluationPipeline:

    def __init__(self):
        pass

    def main(self):

        load_dotenv()
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluator = ModelEvaluation(config=model_evaluation_config)
        model_evaluator.tune_with_mlflow()


if __name__ == '__main__':

    STAGE_NAME = "Model Evaluation Stage"

    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        me_pipe = ModelEvaluationPipeline()
        me_pipe.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e