from src.StarbucksProject.config.configuration import ConfigurationManager
from src.StarbucksProject.components.data_transformation import DataTransformation
from src.StarbucksProject import logger
from pathlib import Path


class DataTransformationPipeline:

    def __init__(self):
        pass

    def main(self):

        with open(Path("artifacts/data_validation/status.txt"), "r") as f:

            status = f.read().split(" ")[-1]
            if status == "True":  # check if validation data set is true
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.split_data()


if __name__ == '__main__':

    STAGE_NAME = "Data Transformation Stage"

    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        dt_pipe = DataTransformationPipeline()
        dt_pipe.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e