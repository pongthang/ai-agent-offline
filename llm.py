import requests, json
class LLM():
    def __init__(self):

        self.url = "http://192.168.31.176:11434/api/generate"

        self.model = "qwen:0.5b"

    def get_response(self,text):

        payload = {
            "model": self.model,
            "prompt": text
        }

        response = requests.post(self.url, json=payload, stream=True)
        full_text = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    text = data["response"]
                    full_text += text
                    # print(text, end="", flush=True)
                elif data.get("done"):
                    break

        return full_text


if __name__=="__main__":

    llm = LLM()

    text = llm.get_response("Hello How are you?")

    print(text)