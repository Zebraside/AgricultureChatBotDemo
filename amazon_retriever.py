from typing import List

import boto3

from langchain_core.retrievers import  BaseRetriever
from langchain_core.pydantic_v1 import BaseModel

def query_kendra(index_id, query_text):
    kendra_client = boto3.client('kendra')
    files = []
    try:
        response = kendra_client.query(
            IndexId=index_id,
            QueryText=query_text
        )

        if 'ResultItems' in response:
            for item in response['ResultItems']:
                files.append(item['DocumentId'])
        else:
            print("No results found.")

    except Exception as e:
        print(f"Failed to query Kendra: {e}")

    return files

def parse_s3_uri(s3_uri):
    # Remove the 's3://' prefix and split the URI into bucket name and object key
    parts = s3_uri.replace("s3://", "").split("/", 1)
    bucket_name = parts[0]
    object_key = parts[1] if len(parts) > 1 else None
    return bucket_name, object_key

def get_s3_document_content(file_uri):
    s3_client = boto3.client('s3')
    try:
        bucket_name, object_key = parse_s3_uri(file_uri)
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        document_content = s3_object['Body'].read().decode('utf-8')
        
        return document_content

    except Exception as e:
        print(f"Error retrieving document from S3: {e}")
        return None


class Document:
    def __init__(self, content):
        self.page_content = content
        self.metadata = {}

class AKRetriever(BaseRetriever, BaseModel):
    index_id: str
    top_k: int = 3

    def __init__(self, index_id: str):
        super().__init__(index_id=index_id)
        self.top_k = 3

    def get_relevant_documents(self, query: str) -> List["Document"]:
        docuemnts = []
        files = query_kendra(self.index_id, query)
        print("KENDRA RESPONSE", files)
        for file in files:
            docuemnts.append(Document(get_s3_document_content(file)))
            print("FILE NAME", file)
            print(docuemnts[-1].page_content)

        return docuemnts