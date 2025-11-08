import requests, json, re
class LLM():
    def __init__(self,url = "http://192.168.31.176:11434/api/generate"):

        self.url = url

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
    
    def get_stream_response(self, text,audio_queue,tts_sys):

        ## Modify the payload
        payload = {
            "model": self.model,
            "prompt": text
        }
        ## Send llm request here
        response = requests.post(self.url, json=payload, stream=True)

        buffer = ""
        full_text = ""

        sentence_end_pattern = re.compile(r'([.!?])')

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    chunk = data["response"]
                    buffer += chunk
                    full_text += chunk

                    # Check for complete sentences
                    while True:
                        match = sentence_end_pattern.search(buffer)
                        if not match:
                            break

                        # Find sentence end and split
                        end_index = match.end()
                        sentence = buffer[:end_index].strip()
                        buffer = buffer[end_index:].lstrip()
                        samples, sample_rate = tts_sys.generate_tts_audio(sentence)
                        audio_queue.put((samples, sample_rate))
                        # Print each full sentence immediately
                        print("Agent --> ",sentence)

                elif data.get("done"):
                    break

        # Print any remaining text (incomplete last sentence)
        if buffer.strip():
            print(buffer.strip())
            samples, sample_rate = tts_sys.generate_tts_audio(buffer.strip())
            audio_queue.put((samples, sample_rate))
            audio_queue.put("done")
            print("Agent --> Done")
        else:

            audio_queue.put("done")
            print("Agent --> Done")


            

if __name__=="__main__":

    llm = LLM()

    text = llm.get_response("Hello How are you?")

    print(text)
