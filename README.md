# Rag 🤖💭
Conversational Chatbot to answer questions about api services. 


<div id="header" align="center">
  <img src="https://github.com/pilarcode/rag_langchain/blob/main/app/assets/question_answer_es.png" width="1000"/>
  <p>This is the look and feel of the smart assistance and how generates responses to the users</p>
</div>

# Data 
Api specification about pets.


# Development
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

# Deployment 

To generate the containerized app and run it on-prem or on a VM, follow these steps:

1. Build the Docker image:

```bash
docker build -t mrag .
```

2. Run the Docker container:

```bash
docker run -it -p 8046:8046 mrag
```


# Run

To interact with the assistant, open your browser. e.g., http://localhost:8046


# Implemented with this tools 
* LangChain
* Gradio
* AzureOpenAI llm: gpt 3.5 turbo
* AzureOpenAI embeddings: text-embedding-ada-002
* Vector stores: Chroma
* Jupyter notebooks
* Python


# Tests

<div id="header" align="center">
  <img src="https://github.com/pilarcode/rag_langchain/blob/main/app/assets/login.png" width="600"/>
  <p>Login</p>
</div>


<div id="header" align="center">
  <img src="https://github.com/pilarcode/rag_langchain/blob/main/app/assets/greetings.png" width="1000"/>
  <p>The user says hi and the smart assistant should offer assistance to the users</p>
</div>

<div id="header" align="center">
  <img src="https://github.com/pilarcode/rag_langchain/blob/main/app/assets/question_answer_en.png" width="1000"/>
  <p>The user asks a question about a service in English</p>
</div>

<div id="header" align="center">
  <img src="https://github.com/pilarcode/rag_langchain/blob/main/app/assets/question_answer_fr.png" width="1000"/>
  <p>The user asks a question about a service in French</p>
</div>
