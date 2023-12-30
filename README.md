# Rag 🤖💭
Chatbot to answer questions about api services. 

<div id="header" align="center">
  <img src="https://github.com/pilarcode/rag_langchain/blob/main/app/assets/question_answer.png" width="800"/>
</div>


## 🟣 Usage

To interact with the assistant, we recommend running the backend app and then opening one of the UIs developed in this project in your browser.
e.g., http://localhost:8046


## 🟣 Data 
Api specification about pets.


## 🟣 Development

### Installation in Dev
To set up a development environment, follow these steps:

1. Navigate to the root directory of the repository and create a new conda environment for development:

```bash
conda create -n mrag python=3.11 -y && conda activate mrag

```

2. Install poetry

```bash
pip install poetry
```

3. Build the whl package with poetry

```bash
poetry build
```

4. Copy the whl file in the dist directory to the root directory

```bash
cp dist/mrag-0.1.0-py3-none-any.whl  app/.
```

5. Edit the requirements.txt and install all the dependencies:

```bash
pip install -r app/requirements.txt

```

6. Run the app:

```bash
cd app
python app_entrypoint.py
```
### Init repo

```bash
$ git init .
```
and link it to the cloud repo. e.g.:
```bash
$ git remote add origin https://github.com/pilarcode/rag_langchain.git
$ git branch -M main
$ git push -uf origin main
```

### Update dependencies to the latest version

```bash
$ poetry update
```

## 🟣 Deployment 🖱️

To generate the containerized app and run it on-prem or on a VM, follow these steps:

1. Build the Docker image:

```bash
docker build -t mrag .
```

2. Run the Docker container:

```bash
docker run -it -p 8046:8046 mrag
```


3. Tag the Docker image:

```bash
docker tag mrag <your-registry-path>/mrag
```

4. Push the Docker image to your cloud Container/Artifact Registry. i.e.:

```bash
docker push <your-registry-path>/mrag
```

Replace `<your-registry-path>` with the path to your Container Registry.



## 🟣 Implemented with this tools 
* LangChain
* AzureOpenAI: LLM and embeddings
* Vector stores: Chroma, Faiss, DeepLake
* Poetry
* Docker
* Jupyter notebooks
* Python



