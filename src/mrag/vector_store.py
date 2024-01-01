import os
from dataclasses import dataclass

from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from mrag.utils import logger

log = logger.get_logger(__name__)


@dataclass
class VectorIndex:
    docs: list
    index_path: str
    embedding_function: AzureOpenAIEmbeddings

    def __post_init__(self):
        """Post initialization"""
        if self.index_path is None:
            raise ValueError(f" Invalid index_path: {self.index_path} at VectorIndex")

        if not isinstance(self.embedding_function, AzureOpenAIEmbeddings):
            raise TypeError("embedding_function must be an instance of AzureOpenAIEmbeddings.")

        self.index = None
        self.index_2 = None

        if not os.path.exists(self.index_path):
            self.create_index()
        else:
            self.load_index()

    def create_index(self):
        """
        Creates the index and saves in self.index_path. The index is also saved in the attribute self.index.
        """

        log.debug(f"Create the index in this path {self.index_path}")
       
        self.index = Chroma.from_documents(
            documents=self.docs,
            embedding=self.embedding_function,
            persist_directory=self.index_path,
            collection_metadata={"hnsw:space": "cosine"},
        )
        log.debug(f"Docs in the vector store:{self.index._collection.count()}")

    def load_index(self):
        """
        Loads the index from self.index_path and saves it in self.index.
        """
        log.debug("Loading the existing index")


        self.index = Chroma(
            persist_directory=self.index_path,
            embedding_function=self.embedding_function,
            collection_metadata={"hnsw:space": "cosine"},
        )
        log.debug(f"Docs loaded from the index {self.index_path}: {self.index._collection.count()}")
     