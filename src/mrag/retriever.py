from dataclasses import dataclass

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers import BM25Retriever, ContextualCompressionRetriever, EnsembleRetriever, SelfQueryRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from mrag.utils import logger

log = logger.get_logger(__name__)


@dataclass
class RetrieverQA:
    llm: object
    vector_index: object
    k: int

    def __post_init__(self):
        """Post initialization"""

        if self.llm is None:
            raise ValueError(f"Invalid llm: {self.llm} at RetrieverQA")

        if self.vector_index is None:
            raise ValueError(f"Invalid vector_index: {self.vector_index} at RetrieverQA")

        if self.k is None:
            self.k = 3

        self.retriever = self.vector_index.as_retriever(search_kwargs={"k": self.k})
        log.debug("RetrieverQA created")

    def get_relevant_documents(self, question):
        """
        Get relevant documents for a given question.

        Args:
            question (str): The question for which to retrieve relevant documents.

        Returns:
            list: A list of relevant documents.
        """
        return self.retriever.get_relevant_documents(question)


@dataclass
class ContextualCompressionRetrieverQA:
    llm: None
    vector_index: None

    def __post_init__(self):
        """Post initialization"""

        if self.llm is None:
            raise ValueError(f"Invalid llm: {self.llm} at MultiRetrieverQA")

        if self.vector_index is None:
            raise ValueError(f"Invalid vector_index: {self.vector_index} at MultiRetrieverQA")

        base_retriever = self.vector_index.as_retriever()
        compressor = LLMChainExtractor.from_llm(self.llm)
        self.retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=base_retriever)

        log.debug("ContextualCompressionRetrieverQA created")

    def get_relevant_documents(self, question):
        return self.retriever.get_relevant_documents(question)


@dataclass
class MMRRetrieverQA:
    llm: None
    vector_index: None

    def __post_init__(self):
        """Post initialization"""

        if self.llm is None:
            raise ValueError(f"Invalid llm: {self.llm} at MultiRetrieverQA")

        if self.vector_index is None:
            raise ValueError(f"Invalid vector_index: {self.vector_index} at MultiRetrieverQA")

        self.retriever = self.vector_index.as_retriever(search_type="mmr", search_kwargs={"score_threshold": 0.7})
        log.debug("MMRRetrieverQA created")

    def get_relevant_documents(self, question):
        return self.retriever.get_relevant_documents(question)


@dataclass
class EnsembleRetrieverQA:
    llm: None
    vector_index: None
    documents: list

    def __post_init__(self):
        """Post initialization"""

        if self.llm is None:
            raise ValueError(f"Invalid llm: {self.vector_db_type} at EnsembleRetrieverQA")

        if self.vector_index is None:
            raise ValueError(f"Invalid vector_index: {self.index_path} at EnsembleRetrieverQA")

        page_content_list = [doc.page_content for doc in self.documents]

        # initialize the bm25 retriever
        bm25_retriever = BM25Retriever.from_texts(page_content_list)
        bm25_retriever.k = 2

        # initialize the ensemble retriever
        self.retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, self.vector_index.as_retriever()], weights=[0.5, 0.5]
        )
        log.debug("EnsembleRetrieverQA created")

    def get_relevant_documents(self, question):
        return self.retriever.get_relevant_documents(question)


@dataclass
class SelfQueryRetrieverQA:
    llm: None
    vector_index: None

    def __post_init__(self):
        """Post initialization"""

        if self.llm is None:
            raise ValueError(f"Invalid llm: {self.llm} at SelfQueryRetrieverQA")

        if self.vector_index is None:
            raise ValueError(f"Invalid vector_index: {self.vector_index} at SelfQueryRetrieverQA")

        metadata_field_info = [
            AttributeInfo(
                name="source",
                description="The api specification (yaml file) the service  is from",
                type="string",
            ),
            AttributeInfo(
                name="api",
                description="The api the service is from",
                type="string",
            ),
            AttributeInfo(
                name="country",
                description="The country the service is from",
                type="string",
            ),
            AttributeInfo(
                name="url",
                description="The url of the service",
                type="string",
            ),
            AttributeInfo(
                name="operationId",
                description="The operationId of the service",
                type="string",
            ),
            AttributeInfo(
                name="summary",
                description="The summary of the service",
                type="string",
            ),
            AttributeInfo(
                name="http_method",
                description="The http_method of the service, should be one of `delete`,`get`, `post`, `put`",
                type="string",
            ),
        ]

        document_content_description = "A service or endpoint description"

        self.retriever = SelfQueryRetriever.from_llm(
            self.llm,
            self.vector_index,
            document_content_description,
            metadata_field_info,
            verbose=True,
            enable_limit=True,
        )
        log.debug("SelfQueryRetrieverQA created")
        return self.retriever

    def get_relevant_documents(self, question):
        return self.retriever.get_relevant_documents(question)
