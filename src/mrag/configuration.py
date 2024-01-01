import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv
from mrag.utils import logger
log = logger.init(level="DEBUG", save_log=True)

@dataclass
class Configuration:
    def __init__(self):
        """
        Initializes an instance of the class.

        :param None: No parameters are required for this function.
        :return None: This function does not return any value.
        """
        # Load the environment variables from the .env file
        _ = load_dotenv(find_dotenv())

        # environment variables for tmp directories
        self.jsons_path = os.environ["JSON_PATH"]
        self.specs_path = os.environ["SPECS_PATH"]

        # vector database variables
        self.vector_index_path = os.environ["VECTOR_INDEX_PATH"]

        # azure open ai variables
        self.AZURE_EMBEDDINGS_DEPLOYMENT = os.environ["AZURE_EMBEDDINGS_DEPLOYMENT"]
        self.AZURE_LLM_DEPLOYMENT = os.environ["AZURE_LLM_DEPLOYMENT"]
        self.OPENAI_API_VERSION = os.environ["OPENAI_API_VERSION"]
        self.CHUNK_SIZE = os.environ["CHUNK_SIZE"]
        self.AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]