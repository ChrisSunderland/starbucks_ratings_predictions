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