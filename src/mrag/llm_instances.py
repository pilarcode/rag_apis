import os

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from openai import AzureOpenAI

from mrag.utils import logger

log = logger.get_logger(__name__)
load_dotenv()

AZURE_EMBEDDINGS_DEPLOYMENT = os.environ["AZURE_EMBEDDINGS_DEPLOYMENT"]
AZURE_LLM_DEPLOYMENT = os.environ["AZURE_LLM_DEPLOYMENT"]
OPENAI_API_VERSION = os.environ["OPENAI_API_VERSION"]
CHUNK_SIZE = os.environ["CHUNK_SIZE"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]


def get_embeddings_instance(
    azure_deployment=AZURE_EMBEDDINGS_DEPLOYMENT,
    openai_api_version=OPENAI_API_VERSION,
    chunk_size=CHUNK_SIZE,
):
    """
    Initialize and return an instance of the AzureOpenAIEmbeddings class for generating embeddings.

    Parameters:
        azure_deployment (str): The Azure deployment to use for the embeddings.
        openai_api_version (str): The OpenAI API version to use.
        chunk_size (int): The size of each chunk for splitting the input text.

    Returns:
        AzureOpenAIEmbeddings: An instance of the AzureOpenAIEmbeddings class.
    """

    embeddings_function = AzureOpenAIEmbeddings(
        azure_deployment=azure_deployment,
        openai_api_version=openai_api_version,
        chunk_size=chunk_size,
    )
    return embeddings_function


def get_llm_instance(
    azure_deployment=AZURE_LLM_DEPLOYMENT,
    openai_api_version=OPENAI_API_VERSION,
    temperature=0,
):
    """
    Initializes and returns an instance of the AzureChatOpenAI class.

    Parameters:
        azure_deployment (str): The Azure deployment to use for the AzureChatOpenAI instance. Defaults to AZURE_LLM_DEPLOYMENT.
        openai_api_version (str): The OpenAI API version to use for the AzureChatOpenAI instance. Defaults to OPENAI_API_VERSION.
        temperature (int): The temperature parameter to use for the AzureChatOpenAI instance. Defaults to 0.

    Returns:
        AzureChatOpenAI: An instance of the AzureChatOpenAI class.
    """

    llm_model = AzureChatOpenAI(
        azure_deployment=azure_deployment, openai_api_version=openai_api_version, temperature=temperature
    )
    return llm_model
