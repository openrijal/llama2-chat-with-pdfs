# Example LLAMA2
This example is using LLAMA2 for local pdf question/answer bot.

# Local Setup
## Clone this repo
```
git clone https://github.com/openrijal/llama2-demo.git
```

## Virtual Environment
It is recommended to create a virtual environment to isolate all packages and versions.
[Conda](https://docs.conda.io/en/latest/) and [Virtualenv](https://virtualenv.pypa.io/en/latest/) are some popular options.

### Create Virtual Environment
If you choose conda, you can install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for your operating system and create a new virtual environment
```
conda create -n llama2-demo python=3.7
```

### Activate Virtual Environment
```
conda activate llama2-demo
```

## Install Dependencies
Install the dependencies using pip
```
pip install -r requirements.txt
```

## Download LLAMA Model
Download a LLAMA model suitable for your computer. There are many to choose from, but you can choose the one that works for your case. There are also quantized models that can run on a CPU. I have the code written to use a 7b parameters quantized model to be run on CPU, so you might wanna change that accordingly.

The model I have used in this example is `llama-2-7b-chat-ggmlv3.q8_0.bin` by [TheBloke](https://huggingface.co/TheBloke). You can find it [here](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q8_0.bin).

Copy the model file into the directory.

## Data Directory
For this demo, I have assummed that all the PDFs you have are kept inside a folder named `data`. The code explicity adds the location and the extention to search to be only `*.pdf`. If you want to use other files, the loaders and the glob needs to be changed accordingly. The same process should work though.

# Library Dependencies
There are a few libraries that is the core of the entire demo.
- Langchain -- used for almost all llm tasks
- Chainlit -- used to turn code into chat interface
- FAISS -- the vector database
- PyPdf -- the pdf parsing library

# Executing the App
Use chainlit to  just run the app.py with auto-reload
```
chainlit run app.py -w
```