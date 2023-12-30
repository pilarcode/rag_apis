import glob
import os
from dataclasses import dataclass

from langchain.text_splitter import RecursiveCharacterTextSplitter

from mrag.json_loader import JSONLoader
from mrag.utils import logger
from mrag.utils.doc_utils import extract_data_from_specs

log = logger.get_logger(__name__)
DEFAULT_CHUNK_SIZE = 4000
DEFAULT_OVERLAP = 0


@dataclass
class Loader:
    """
    Docs Loader Class
    """

    specs_path: str
    docs_path: str

    def __post_init__(self) -> None:
        """Post initialization"""

        self.splitter = RecursiveCharacterTextSplitter(chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_OVERLAP)

        if not os.path.exists(self.specs_path):
            raise ValueError(f"Invalid specs_path: {self.specs_path}")

        if not os.path.exists(self.docs_path):
            # Extract data from api specification
            extract_data_from_specs(specs_path=self.specs_path, docs_path=self.docs_path)

    def extract_docs(self):
        """
        Extract the pages/chunks from all the files in the docs_path
        """

        path = self.docs_path + "/*.json"
        log.debug(f"Loading documents from: {path}")
        json_paths = glob.glob(path, recursive=True)

        loaders = []
        for json_path in json_paths:
            json_loader = JSONLoader(file_path=json_path)
            loaders.append(json_loader)

        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        return docs
