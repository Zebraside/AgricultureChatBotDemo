class Chatbot:
    def __init__(self, qa, retrievalChain = False):
        self.qa = qa
        self.retrievalChain = retrievalChain

    def start_chat(self):
        print("Starting chat bot")
        self.chat(None, None)

    def chat(self, text, history=""):
        if text is None:
            prompt = ""
        else:
            prompt = text
        if 'q' == prompt or 'quit' == prompt or 'Q' == prompt:
            return
        elif len(prompt) > 0:
            try:
                if self.retrievalChain:
                    result = self.qa.question(prompt, history)
                else:
                    result = self.qa.input(prompt)
            except Exception as e:
                print(e)
                result = "No answer"

            return result