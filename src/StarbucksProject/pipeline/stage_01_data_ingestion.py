from src.StarbucksProject.config.configuration import ConfigurationManager
from src.StarbucksProject.components.data_ingestion import DataIngestion
from src.StarbucksProject import logger


class DataIngestionTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        config = ConfigurationManager()

        data_ingestion_config = config.get_data_ingestion_config()

        data_ingestion = DataIngestion(config=data_ingestion_config)

        data_ingestion.download_file()

        data_ingestion.extract_zip_file()

        data_ingestion.clean_all_csvs()

        data_ingestion.get_yelp_data()


if __name__ == '__main__':

    STAGE_NAME = "Data Ingestion Stage"

    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        di_pipe = DataIngestionTrainingPipeline()
        di_pipe.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e