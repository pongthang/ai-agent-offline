I want to build an offline voice assistant ai-gent in a system of 4GB ram, 4 core , running lubuntu 24. consider below ai models.
1. LLM - qwen 0.5b running using ollama.
2. vosk -asr and vad
3. pysttsx3 for tts. 
use sound device to read input device , don't take input while tts is playing. take user input audio --> text --> llm --> text output --> tts. all are done sequentially one after another. you can use threading and multiprocessing for implementing the above.implement in python.
you can get ollama as below
```python
url = "http://192.168.31.176:11434/api/generate"
payload = {
    "model": "qwen:0.5b",
    "prompt": "Explain quantum computing in simple terms."
}

```
keep the program running until user say lets stop , or stop this.