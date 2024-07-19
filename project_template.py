import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[ %(asctime)s: %(message)s ]')
project_name = "StarbucksProject"

files = [".env",
         "requirements.txt",
         "setup.py",
         "next_steps.txt",
         "config/config.yaml",
         "schema.yaml",
         "params.yaml",
         ".github/workflows/.gitkeep",
         "notebooks/stage_01_data_ingestion.ipynb",
         f"src/{project_name}/__init__.py",  # set up logger in this file
         f"src/{project_name}/components/data_ingestion.py",
         f"src/{project_name}/config/configuration.py",
         f"src/{project_name}/constants/__init__.py",
         f"src/{project_name}/entity/config_entity.py",
         f"src/{project_name}/pipeline/stage_01_data_ingestion.py",
         f"src/{project_name}/utils/common.py",
         "main.py",
         "app.py",
         "templates/index.html",  # for flask app
         "templates/results.html", # for flask app
         "Dockerfile"]

# create the project's initial folder structure
for file in files:

    filepath = Path(file)
    file_dir, filename = os.path.split(filepath)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating directory: {file_dir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")