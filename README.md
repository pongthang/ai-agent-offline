# Your offline AI voice assistant

## AI models which are used in this project

- Automatic Speech Recognition(ASR) - vosk
- Language Model (LM) - Qwen 0.5b
- Text to speech(TTS) - Kokoro

## Prompt sharing

Today, we reach an era where prompt becomes new programming language and LLM becomes the compiler. So I believe sharing our prompt while developing things will be a great help to other and our own development. So, feel free to check the prompts in the [prompts_development](./prompts_development/) for more. 

## How to setup the project

#### Install ollama - for hosting LM
```bash
## Install ollama
curl -fsSL https://ollama.com/install.sh | sh

## check whether it is installed correctly
ollama --version

## pull qwen 0.5b
ollama pull qwen:0.5b

## check the ollama is running or not

sudo systemctl status ollama

## Consider enable ollama so it will start when system is booted otherwise you need to start manually
sudo systemctl enable ollama
sudo systemctl start ollama

```
Consider checking out ollama documentation to see how to run in local network not only localhost.

##### Note
Now your language model is running and get inference at `http://localhost:11434/api/generate`

#### Clone this repo

```bash
git clone https://github.com/pongthang/ai-agent-offline.git
```

#### Set up a python virtual environment
Make a python3.12 virtual environment. You can use conda also. Here I use python venv

```bash
## Move inside the repo
cd ai-agent-offline

## create python venv
python3.12 -m venv myenv

## Activate
source myenv/bin/activate

## Install dependencies
pip install -r requirements.txt


## Download kokoro models

source download_kokoro_models.bash

```

#### Make required changes to voice_assistant.py

Open voice_assistant.py file and check for environment variables.

```python
# Environment variables
DEVICE = None
stream_tts=True
url= "http://localhost:11434/api/generate"
```

Change the stream_tts `False` if you don't want sentence by sentence tts and llm response. Just play around and select the mode you like.

Change the url according to your ollama deployment. `localhost` if you want to run in same machine (ollama + voice_assistant) or ollama in different machine in local network.

Save after make changes.

#### Run the voice assistant program

```bash
## Activate the myenv if not
source myenv/bin/activate

python voice_assistant.py
```

Now you can talk to your offline personal voice assistant.


### Next steps:

- I will add the customization of Language model. 
- Testing different small language models
- Making as agent
- RAG system
- Independent AI researcher

#### Welcome to AI Revolution !!

#### Feel free to raise a issue if you face any difficulties and to contribute in this project.
### MIT License

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
