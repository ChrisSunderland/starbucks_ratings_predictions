from src.StarbucksProject.config.configuration import ConfigurationManager
from src.StarbucksProject.components.data_validation import DataValidation
from src.StarbucksProject import logger


class DataValidationPipeline:

    def __init__(self):

        pass

    def main(self):

        try:

            config = ConfigurationManager()

            data_validation_config = config.get_data_validation_config()

            data_validation = DataValidation(config=data_validation_config)

            combined_data = data_validation.combine_data()

            data_validation.clean_data(combined_data)

            data_validation.validate_columns()

        except Exception as e:

            raise e


if __name__ == '__main__':

    STAGE_NAME = "Data Validation Stage"

    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        dv_pipe = DataValidationPipeline()
        dv_pipe.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e