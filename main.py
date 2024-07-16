from src.StarbucksProject.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.StarbucksProject import logger

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    di_pipe = DataIngestionTrainingPipeline()
    di_pipe.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e