# epam-GenAI

### Jupyter Notebook
with a description of all the steps
**src/research.ipynb**

## solution server
### CONFIG 

create a file **.env** with the following parameters in the project folder
```
HUGGINGFACEHUB_API_TOKEN = hf_********
LINK_SITE = https://www.bbc.com/
MAX_COUNT = 15
```

* HUGGINGFACEHUB_API_TOKEN - api key from HUGGINGFACE
* LINK_SITE - processing site
* MAX_COUNT  - The number of news items to be processed

run server 

```sh
docker build -t genai .
docker run --name genai-con -d -p 8501:8501 genai

```
### link http://0.0.0.0:8501/playground/

