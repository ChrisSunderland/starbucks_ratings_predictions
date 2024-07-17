from src.StarbucksProject.constants import *
from src.StarbucksProject.utils.common import read_yaml, create_directories
from src.StarbucksProject.entity.config_entity import (DataIngestionConfig, DataValidationConfig,
                                                       DataTransformationConfig)


class ConfigurationManager:

    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,  # Path("config/config.yaml")
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(root_dir=config.root_dir,
                                                    acs_source_url=config.acs_source_url,
                                                    local_zip_file=config.local_zip_file,
                                                    acs_data_clean=config.acs_data_clean,
                                                    acs_demo_housing_clean=config.acs_demo_housing_clean,
                                                    acs_econ_clean=config.acs_econ_clean,
                                                    acs_housing_clean=config.acs_housing_clean,
                                                    acs_social_clean=config.acs_social_clean,
                                                    yelp_api_endpoint=config.yelp_api_endpoint,
                                                    yelp_data=config.yelp_data,
                                                    yelp_csv=config.yelp_csv)

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(root_dir=config.root_dir,
                                                      acs_demo_housing=config.acs_demo_housing,
                                                      acs_econ=config.acs_econ,
                                                      acs_housing=config.acs_housing,
                                                      acs_social=config.acs_social,
                                                      yelp=config.yelp,
                                                      acs_yelp_combined=config.acs_yelp_combined,
                                                      all_schema=schema,
                                                      STATUS_FILE=config.STATUS_FILE)

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:

        config = self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config = DataTransformationConfig(root_dir=config.root_dir,
                                                              data_path=config.data_path)

        return data_transformation_config