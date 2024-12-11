# epam-GenAI

### Jupyter Notebook
**src/research.ipynb**

## solution server
### CONFIG 

.env file
```
HUGGINGFACEHUB_API_TOKEN = hf_********
LINK_SITE = https://www.bbc.com/
MAX_COUNT = 15
```
run server 

```sh
docker build -t epam .
docker run --name epam-con -d -p 8501:8501 epam

```
### link http://0.0.0.0:8501/playground/

