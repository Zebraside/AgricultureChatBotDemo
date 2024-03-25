from typing import List
import os

import boto3
from langchain.embeddings import BedrockEmbeddings

from utils import bedrock

class EmbeddingModels:
    def __init__(self):
        self.boto3_bedrock = bedrock.get_bedrock_client(
            assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
            region=os.environ.get("AWS_DEFAULT_REGION", None)
        )

        self.br_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=self.boto3_bedrock)

    def get_model(self):
        return self.br_embeddings

    def get_embedding_for_document(self, document: str):
        return self.br_embeddings.embed_query(document)

    def get_embedding_for_documents(self, documents: List[str]):
        return self.br_embeddings.embed_documents(documents)