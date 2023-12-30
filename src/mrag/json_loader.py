import json
from dataclasses import dataclass
from pathlib import Path  # noqa: F811
from typing import List, Optional, Union

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader

from mrag.utils import logger

log = logger.get_logger(__name__)


@dataclass
class JSONLoader(BaseLoader):
    def __init__(
        self,
        file_path: Union[str, Path],
        content_key: Optional[str] = None,
    ):
        self.file_path = Path(file_path).resolve()
        self.content_key = content_key

    def load(self) -> List[Document]:
        """Load and return documents from the JSON file."""

        docs = []
        with open(self.file_path) as file:
            try:
                data = json.load(file)

                text = {}
                text["summary"] = data["summary"]
                text["url"] = data["url"]
                text["operationId"] = data["operationId"]
                text["http_method"] = data["http_method"]
                text["country"] = data["country"]
                text["parameters"] = data["parameters"]
                page_content = str(text)

                metadata = {}
                metadata["source"] = data["source"]
                docs.append(Document(page_content=page_content, metadata=metadata))
            except Exception as error:
                log.debug(f"{error} . Loading this json file:{self.file_path}.")
        return docs


def get_documents(selected_files_path):
    """
    Retrieves documents from the selected files.

    Args:
        selected_files_path (List[str]): A list of file paths to the selected files.

    Returns:
        List[Document]: A list of documents retrieved from the selected files.
    """
    loaders = []
    for json_path in selected_files_path:
        json_loader = JSONLoader(file_path=json_path)
        loaders.append(json_loader)

    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs
