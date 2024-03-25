from flask import Flask, request, jsonify, render_template
import os

from embeddings_model import EmbeddingModels
from qa_model import AmazonChatModel
from chat import Chatbot

from amazon_retriever import AKRetriever


app = Flask(__name__)

# NOTE: following environment variables are required
# AWS_DEFAULT_REGION
# AWS_KENDRA_INDEX_ID

# os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

kenda_index_id = os.getenv("AWS_KENDRA_INDEX_ID") 
retriever = AKRetriever(index_id=kenda_index_id)
chat_model = AmazonChatModel(retriever)
chatbot = Chatbot(chat_model, retrievalChain=True)
chatbot.start_chat()


def convert_chat_history(chat_history):
    history = ""
    for message in chat_history:
        history += f"{message['sender']}: {message['text']}\n"

    return history


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['lastMessage']
    # Frontend sends chat history including the last question. It must be removed manually.
    chat_history = convert_chat_history(request.json['chatHistory'][:-1])
    bot_response = chatbot_response(user_message, chat_history)
    return jsonify({"response": bot_response})


def chatbot_response(message, history):
    global  chatbot
    print(type(chatbot))
    return chatbot.chat(message, history)

if __name__ == "__main__":
    app.run(debug=True)
