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


def read_file_paths(directory, extension_file="*.json", recursive=False):
    """
    Retrieve a list of file paths from the given directory.

    Parameters:
        directory (str): The directory to search for files in.

    Returns:
        list: A list of file paths that match the specified pattern.
    """

    file_paths = glob.glob(os.path.join(directory, extension_file), recursive=recursive)
    return file_paths


def show_doc_service_details(documents_found):
    """
    Generates a pandas DataFrame containing the service details for the given list of documents.

    Parameters:
        documents_found (list): A list of documents containing service details.

    Returns:
        df (pandas DataFrame): A DataFrame containing the service details with columns for operationId, api, country,
        url, and http_method.
    """

    columns = ["operationId", "api", "country", "url", "http_method"]
    df = pd.DataFrame(columns=columns)
    for doc in documents_found:
        operationId = doc.metadata["operationId"]
        api = doc.metadata["api"]
        country = doc.metadata["country"]
        url = doc.metadata["url"]
        http_method = doc.metadata["http_method"]
        doc_row = pd.Series([operationId, api, country, url, http_method], index=columns)
        df = pd.concat([df, doc_row.to_frame().T], ignore_index=True)
    return df


def show_doc_service_parameters(documents_found):
    """
    Generate a DataFrame from a list of documents.

    Parameters:
        documents_found (list): A list of documents.

    Returns:
        df (pandas.DataFrame): A DataFrame containing the operationId and parameters of each document.
    """
    columns = ["operationId", "parameters"]
    df = pd.DataFrame(columns=columns)
    for doc in documents_found:
        operationId = doc.metadata["operationId"]
        parameters = doc.metadata["parameters"]
        doc_row = pd.Series([operationId, parameters], index=columns)
        df = pd.concat([df, doc_row.to_frame().T], ignore_index=True)
    return df


def show_doc_description(documents_found):
    """
    Generate a DataFrame with the operationId and description of each document in the given list.

    Parameters:
    - documents_found (list): A list of documents.

    Returns:
    - df (pandas.DataFrame): A DataFrame containing the operationId and description columns.
    """
    columns = ["operationId", "description"]
    df = pd.DataFrame(columns=columns)
    for doc in documents_found:
        operationId = doc.metadata["operationId"]
        description = doc.page_content
        doc_row = pd.Series([operationId, description], index=columns)
        df = pd.concat([df, doc_row.to_frame().T], ignore_index=True)
    return df


def show_doc(document):
    """
    Print the type, page content, and metadata of a document.

    Parameters:
        document (object): The document object to show the details of.

    Returns:
        None
    """
    print("type:", type(document))
    print("page_content:", document.page_content)
    print("metadata:", document.metadata)


def prepare_parameters(parameters: list):
    """
    Generates a text based on the given list of parameters.

    Parameters:
        parameters (list): A list of dictionaries representing the parameters.
                           Each dictionary should have 'name' and 'description' keys.

    Returns:
        str: The generated text based on the parameters.
    """
    text = ""
    for param in parameters:
        try:
            if "name" in param and param["name"]:
                text += "The parameter " + param["name"] + " "
            if "description" in param and param["description"]:
                text += "means " + param["description"] + "."
        except Exception as error:
            print(param, error)
    return text


def create_ground_truth_dataset(subset_docs: list):
    columns = [
        "operationId",
        "summary",
        "http_method",
        "url",
        "country",
        "service_description",
        "parameters",
        "source",
        "api",
    ]
    df = pd.DataFrame(columns=columns)

    for doc in subset_docs:
        page_content = ast.literal_eval(doc.page_content)
        metadata = doc.metadata

        # Fields Should be the same as in the JsonLoader class
        api = page_content["api"]
        operationId = page_content["operationId"]
        summary = page_content["summary"]
        http_method = page_content["http_method"]
        url = page_content["url"]
        country = page_content["country"]
        service_description = page_content["service_description"]
        parameters = page_content["parameters"]
        source = metadata["source"]

        doc_row = pd.Series(
            [operationId, summary, http_method, url, country, service_description, parameters, source, api],
            index=columns,
        )
        df = pd.concat([df, doc_row.to_frame().T], ignore_index=True)
    return df
