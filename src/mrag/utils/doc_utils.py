import ast
import glob
import json
import os

import pandas as pd
import yaml

from mrag.utils import logger

log = logger.get_logger(__name__)


def extract_data_from_specs(specs_path, docs_path):
    """
    Extracts data from the specifications file and creates a JSON files for each endoinpt of the API.

    Args:
        specs_path (str): The path to the directory containing the specifications files.
        docs_path (str): The path to the directory where the JSON files will be created.

    Returns:
    None
    """

    log.debug("Extract data from the specifications file and creates a JSON files for each endoinpt of the API.")
    yaml_paths = os.path.join(specs_path, "**", "*.yaml")
    api_specs_paths = glob.glob(yaml_paths, recursive=True)

    for yaml_file in api_specs_paths:
        normpath = os.path.normpath(yaml_file)
        country = normpath.split("\\")[-2].split("_")[0]
        create_jsons_from_yaml(normpath, country, docs_path)


def create_jsons_from_yaml(yaml_path, country,  output_folder):
    """
    Create json files

    :param yaml_path: The path to the YAML file.
    :param country: The country associated with the JSON files.
    :param output_folder: The folder where the JSON files will be created.
    """
    log.debug(f" yaml file: {yaml_path}  , country:{country}")

    # Load the YAML data from file
    with open(yaml_path , encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # Load the JSON data from file
    title = data.get("info").get("title")
    basePath = data.get("servers")[0].get("url")
    paths = data.get("paths")

    for service_path in paths:

        for http_method, service in paths[service_path].items():
            operationId = service.get("operationId")
            parameters = service.get("parameters")
            responses = service.get("responses")
            
            summary = service.get("summary")
            tag = service.get("tags")

            json_data = {
                "country": country,
                "source": yaml_path.split("\\")[-1],
                "title": title,
                "basePath": basePath,
                "url": service_path,
                "operationId": operationId,
                "summary": summary,
                "parameters": parameters,
                "responses": responses,
                "http_method": http_method,
                "tag": tag,
            }

            # Create the output folder
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Create the JSON file
            json_file_path = output_folder + "/" + country + "_" + http_method + "_" + operationId + ".json"
            with open(json_file_path, "w") as file:
                json.dump(json_data, file)
