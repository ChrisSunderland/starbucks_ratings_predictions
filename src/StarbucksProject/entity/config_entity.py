from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:

    root_dir: Path
    acs_source_url: str
    local_zip_file: Path
    acs_data_clean: Path
    acs_demo_housing_clean: Path
    acs_econ_clean: Path
    acs_housing_clean: Path
    acs_social_clean: Path
    yelp_api_endpoint: str
    yelp_data: Path
    yelp_csv: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    acs_demo_housing: Path
    acs_econ: Path
    acs_housing: Path
    acs_social: Path
    yelp: Path
    acs_yelp_combined: str
    all_schema: dict
    STATUS_FILE: str

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path