from src.StarbucksProject.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.StarbucksProject.pipeline.stage_02_data_validation import DataValidationPipeline
from src.StarbucksProject.pipeline.stage_03_data_transformation import DataTransformationPipeline
from src.StarbucksProject.pipeline.stage_04_model_training import ModelTrainingPipeline
from src.StarbucksProject.pipeline.stage_05_model_evaluation import ModelEvaluationPipeline
from src.StarbucksProject import logger
import joblib

# stage 1 (data ingestion) has been commented out so you can run the program without obtaining a Yelp API key

# STAGE_NAME = "Data Ingestion Stage"
#
# try:
#     logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
#     di_pipe = DataIngestionTrainingPipeline()
#     di_pipe.main()
#     logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#     logger.exception(e)
#     raise e

STAGE_NAME = "Data Validation Stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    dv_pipe = DataValidationPipeline()
    dv_pipe.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    dt_pipe = DataTransformationPipeline()
    dt_pipe.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Training Stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    mt_pipe = ModelTrainingPipeline()
    mt_pipe.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Evaluation Stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    me_eval_pipe = ModelEvaluationPipeline()
    final_model = me_eval_pipe.main()
    joblib.dump(final_model, 'final_model.joblib')

    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e