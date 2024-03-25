# Agriculture AI Chatbot Demo

This is a demo application featuring an AI-based chatbot to showcase AWS machine learning capabilities.

The project integrates the following technologies:
- Amazon Bedrock - to run an LLM model.
- Amazon Kendra - for storing an indexed database of documents for the knowledge base.
- Amazon EC2 - to host the app's HTTP endpoint.
- Amazon S3 Bucket - for storing required documents.

## Environment Setup

The following environment variables are required for the application to run:

- `AWS_DEFAULT_REGION` - The AWS region to use.
- `AWS_KENDRA_INDEX_ID` - The index ID of the Kendra database.

Additional variables may be required if AWS is not configured on the host machine.

## How to Run the Project
Upload all files from the `data` folder to the corresponding Amazon Kendra index.

Install all dependencies:
```bash
pip install -r requirements.txt
```

Next, set up all environment variables as described in the [Environment Setup](#environment-setup) section.
```bash
export AWS_DEFAULT_REGION=%YOUR_REGION%
export AWS_KENDRA_INDEX_ID=%YOUR_KENDRA_INDEX_ID%
```

Finally, start the Flask application:
```bash
FLASK_APP=app.py flask run --host=0.0.0.0 --port 5005 --debug
```