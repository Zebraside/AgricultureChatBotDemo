import os

import boto3
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

from utils import bedrock


def get_chat_history(input):
    return input

class AmazonChatModel:
    def __init__(self, retriever):
        prompt_template = """Human: This is a friendly conversation between a human and an AI.
        The AI is talkative and provides specific details from its context but limits it to 240 tokens.
        If the AI does not know the answer to a question, it truthfully says it
        does not know.

        Assistant: OK, got it, I'll be a talkative truthful AI assistant.

        Human: Here are a few documents from out knowledge base in <knowledge base> tags:
        <knowledge base>
        {context}\n
        </knowledge base>
        Based on the above information, provide a detailed answer for, {question}
        Try not to use and internal tags in <> or json fields in the answer. 
        Answer "don't know" if not present in the knowledge base. 


        Assistant:
        """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        condense_qa_template = """
        {chat_history}
        Human:
        Given the previous conversation and a follow up question below, rephrase the follow up question
        to be a standalone question.

        Follow Up Question: {question}
        Standalone Question:

        Assistant:"""
        standalone_question_prompt = PromptTemplate.from_template(condense_qa_template)

        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        boto3_bedrock = bedrock.get_bedrock_client(
            assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
            region=os.environ.get("AWS_DEFAULT_REGION", None)
        )

        self.titan_llm = Bedrock(
            region_name=os.getenv("AWS_DEFAULT_REGION"),
            model_kwargs={"max_tokens_to_sample":300, "temperature": 0, "top_k":250, "top_p":0.999, "anthropic_version":"bedrock-2023-05-31"},
            model_id="anthropic.claude-v2"
        )
        self.memory_chain = ConversationBufferMemory(memory_key="chat_history", input_key="question", return_messages=True)

        self.qa = ConversationalRetrievalChain.from_llm(
            llm= self.titan_llm, 
            retriever=retriever,
            get_chat_history=get_chat_history,
            condense_question_prompt=standalone_question_prompt, 
            combine_docs_chain_kwargs={"prompt":PROMPT},
            verbose=True)

    def question(self, prompt, chat_history = ""):
        result = self.qa.run({'question': prompt, 'chat_history': chat_history})
        # NOTE: response is inserted as raw HTML for demo purposes. Formatting is done using HTML tags
        return result.replace("\n", "<br>")

    def input(self, prompt):
        return self.qa.run({'input': prompt})
