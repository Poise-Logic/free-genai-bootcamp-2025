# Deploying OPEA ChatQnA MegaService Deployment on Intel CPU / AIPC (Single Node, Ollama)

## Overview

This guide provides step-by-step instructions for deploying the OPEA ChatQnA example application using **Docker Compose**. This deployment leverages the OPEA GenAIComps microservice pipeline, specifically using **Ollama** for the Large Language Model (LLM) component on an **Intel Client CPU or AIPC**.

## System Architecture

*   **Deployment Model:** Single-node, on-premises via Docker Compose.
*   **Orchestration:** Docker Compose.
*   **Core Pipeline:** Data Prep -> Embedding (TEI) -> Retriever -> LLM (Ollama) -> Backend (Mega Service) -> UI.
*   **Supporting Services:** Redis (Vector DB), Nginx (Reverse Proxy).
*   **Target Environment:** Windows 11 + Docker Desktop + WSL2 (Ubuntu 24.04).

## Prerequisites
- **Docker Desktop:** Make sure Docker Desktop is running and properly integrated with your WSL2 environment. You can verify this by running Docker commands within your WSL2 terminal.
  - Alternatively, install docker engine directly on your WSL2 instance.
- **WSL2 Environment:** You should have a properly configured WSL2 environment running a linux distribution. In this case, we'll use Ubuntu 24.04.
- **Git:** Git is required to clone the OPEA repositories. You can check if Git is installed by running `git --version`. If not, install it using `sudo apt update && sudo apt install git`.
- **Python 3.9+:** Python is needed for setting up a virtual environment if required for any auxiliary scripts or tools. Check your Python version with `python3 --version`. If necessary, install or upgrade Python.
- Sufficient disk space and RAM available on your machine to run the Docker containers. *At the time of writing, the total size of all docker images is approximately 16.34 GB*. For optimal performance, I recommend at least 8GB of RAM, with 16GB being ideal for running all services simultaneously.

## Prepare (Building / Pulling) Docker images
For this ChatQnA example, the following docker images will be needed:
- VectorDB: `redis/redis-stack:7.2.0-v9`
- Dataprep(redis): `opea/dataprep:latest`
- TEI-embedding: `ghcr.io/huggingface/text-embeddings-inference:cpu-1.6`
- Retriever(redis): `opea/retriever:latest`
- LLM: `ollama/ollama`
- ChatQnA Megaservice: `opea/chatqna:latest`
- ChatQnA UI: `opea/chatqna-ui:latest`
- Nginx Server: `opea/nginx:latest`

### Pulling Pre-built Images
If you decide to pull the docker containers and not build them locally, you can proceed to the next step (**Deploying the Services**) where all the necessary containers will be pulled in from Docker Hub.

**Note:** You should build docker images from source by yourself if:
- You're working with the latest code from the main branch (where port configurations may differ from published images)
- You're unable to download the pre-built docker image
- You need a specific Docker image version

### Building Docker Images

Follow the steps below to build the docker images from within the GenAIComps and GenAIExample (specifically for ChatQnA and UI) folder.

#### Clone OPEA Repositories

```bash
# Create and navigate to your preferred repository cloning directory
mkdir -p ~/OPEA
cd ~/OPEA

# Clone the OPEA repository which contains the GenAIExamples
git clone https://github.com/opea-project/GenAIExamples.git

# Clone the main OPEA repository, which contains the GenAIComps
git clone https://github.com/opea-project/GenAIComps.git

# Navigate into the `GenAIComps` directory:
cd GenAIComps
```

#### Build Microservice Images

**Build Retriever Image:**

```bash
docker build --no-cache -t opea/retriever:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/retrievers/src/Dockerfile .
```

**Build Dataprep Image:**

```bash
docker build --no-cache -t opea/dataprep:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/dataprep/src/Dockerfile .
```

**Build Nginx Docker Image:**

```sh
cd GenAIComps
docker build -t opea/nginx:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/third_parties/nginx/src/Dockerfile .
```

#### Build the (ChatQnA) Megaservice Image
The Megaservice is a pipeline that channels data through different microservices, each performing varied tasks. We define the different microservices and the flow of data between them in the chatqna.py file, say in this example the output of embedding microservice will be the input of retrieval microservice which will in turn passes data to the reranking microservice and so on. You can also add newer or remove some microservices and customize the megaservice to suit the needs.

```bash
cd ~/OPEA/GenAIExamples/ChatQnA
docker build --no-cache -t opea/chatqna:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy  -f Dockerfile .
```

#### Build ChatQnA-UI Image

```bash
cd ~/OPEA/GenAIExamples/ChatQnA/ui
docker build --no-cache -t opea/chatqna-ui:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f ./docker/Dockerfile .
```

#### Sanity Check: List the downloaded/built images.
Run the command: `docker images` check if you have the below set of docker images, before moving on to the next step:
- opea/dataprep:latest
- opea/retriever:latest
- opea/chatqna:latest
- opea/chatqna-ui:latest
- opea/nginx:latest

## Start MicroServices and MegaService

### Setup Environment Variables
To set up environment variables for deploying ChatQnA services, follow these steps:

Since the docker compose file and ChatQnA services will consume some environment variables, you need to setup them in advance as below either by running individual commands or using a script(set_env.sh).

```sh
# Determine the host IP address
export host_ip=$(hostname -I | awk '{print $1}')

# Hugging Face API Token (replace the placeholder)
export HUGGINGFACEHUB_API_TOKEN="PLACE HF TOKEN HERE"

export EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"
export INDEX_NAME="rag-redis"
export OLLAMA_HOST=${host_ip}
export OLLAMA_MODEL="llama3.2"
```

Run: `chmod +x set_env.sh` to make the script executable.

Source the environment variables from the set_env.sh file:
```bash
source ./set_env.sh
```
### Deploy the Services Using Docker Compose
To deploy the ChatQnA services, execute the `docker compose up` command. Ensure you are in the folder where the docker compose file resides before running the below command.

```bash
docker compose up -d
```

The ChatQnA docker images should automatically be downloaded from the OPEA registry and deployed locally:

```
[+] Running 9/9
 ✔ Network chatqna_opea-network           Created                                                                                                                     0.1s 
 ✔ Container tei-embedding-server         Started                                                                                                                     0.8s 
 ✔ Container ollama                       Started                                                                                                                     0.9s 
 ✔ Container redis-vector-db              Started                                                                                                                     0.8s 
 ✔ Container retriever-redis-server       Started                                                                                                                     1.0s 
 ✔ Container dataprep-redis-server        Started                                                                                                                     1.0s 
 ✔ Container chatqna-aipc-backend-server  Started                                                                                                                     1.2s 
 ✔ Container chatqna-aipc-ui-server       Started                                                                                                                     1.4s 
 ✔ Container chatqna-aipc-nginx-server    Started                                                                                                                     1.6s 
```

## Validate Services

### Check Environment Variables

Check the start up log by running `docker compose logs -f`. When you're in the same directory as the docker-compose.yaml file, Docker Compose will automatically detect and use it without needing the -f flag to specify the file path. You can also add options like:
- `docker compose logs [service_name]` to see logs for a specific service only
- `docker compose logs --tail=20` to see only the last 100 lines

The warning messages point out the variables are NOT set.

To check environment variables for a running container, use:
```bash
docker compose exec [service_name] env
```

### Check the Deployment Status
After running docker compose, check if all the containers launched via docker compose have started:

```sh
docker ps -a`
```

For this deployment, the following 8 containers should have started:
```
CONTAINER ID   IMAGE                                                   COMMAND                  CREATED          STATUS          PORTS                                            NAMES
32a51dcbe611   opea/nginx:latest                                       "/docker-entrypoint.…"   58 minutes ago   Up 57 minutes   0.0.0.0:80->80/tcp                               chatqna-aipc-nginx-server
f0ec9e4011b6   opea/chatqna-ui:latest                                  "docker-entrypoint.s…"   58 minutes ago   Up 57 minutes   0.0.0.0:5173->5173/tcp                           chatqna-aipc-ui-server
deaed587c7b7   opea/chatqna:latest                                     "bash entrypoint.sh"     58 minutes ago   Up 57 minutes   0.0.0.0:8888->8888/tcp                           chatqna-aipc-backend-server
f4e2bd209b01   opea/dataprep:latest                                    "sh -c 'python $( [ …"   58 minutes ago   Up 57 minutes   0.0.0.0:6007->5000/tcp                           dataprep-redis-server
9fc310e84112   opea/retriever:latest                                   "python opea_retriev…"   58 minutes ago   Up 5 seconds    0.0.0.0:7000->7000/tcp                           retriever-redis-server
ee21b83225b9   redis/redis-stack:7.2.0-v9                              "/entrypoint.sh"         58 minutes ago   Up 58 minutes   0.0.0.0:6379->6379/tcp, 0.0.0.0:8001->8001/tcp   redis-vector-db
b3f08339dc5a   ollama/ollama                                           "bash -c 'ollama ser…"   58 minutes ago   Up 58 minutes   0.0.0.0:11434->11434/tcp                         ollama
2fe10d9dd297   ghcr.io/huggingface/text-embeddings-inference:cpu-1.6   "text-embeddings-rou…"   58 minutes ago   Up 58 minutes   0.0.0.0:6006->80/tcp                             tei-embedding-server
```
Next we can check the container logs to get to know what happened during the docker start.

### Check Docker Container Log
Use the below command to check container logs for potential errors. 

```bash
docker logs <CONTAINER ID> -t
```

Replace <Container ID> with the actual ID of the container (e.g., 32a51dcbe611). You can find the container IDs in the output of `docker ps -a`.

### Check All ChatQnA Services

**1. ChatQnA Megaservice**
```sh
curl http://${host_ip}:8888/v1/chatqna -H "Content-Type: application/json" -d '{
     "messages": "What is the revenue of Nike in 2023?"
     }' | sed '/DONE/d' | sed 's/data: b//g' | tr -d "'" | tr -d '\n'; echo -e "\ndata: [DONE]"
```

Here is the output for your reference:
```
I don"t" have real-time access to current financial data, but I can suggest some possible sources where you may be able to find the latest revenue figures for Nike in 2023.\n\nAccording to recent reports, Nike"s" revenue for 2022 was around $44.5 billion. However, I couldn"t" find any information on their revenue for 2023 as it has not been officially announced yet.\n\nFor the most up-to-date and accurate information, I recommend checking Nike"s" official website or financial reports from reputable sources such as Bloomberg or Forbes. They should have the latest financial data available.
data: [DONE]
```

**2. TEI Embedding MicroService**

```json
curl ${host_ip}:6006/embed \
    -X POST \
    -d '{"inputs":"What is AI?"}' \
    -H 'Content-Type: application/json'
```
This test the embedding service. It sends “What is AI?” to the embedding service, the output is the embedding result of the sentences, it is a list of vector.
`[[0.008912046,-0.014962528,0.029607954,0.004155268,0.02462766,0.03157888,0.030918386,0.0039674975,-0.02111754,-0.014492543,....,013575585,-0.0023442914,-0.007383723,-0.019244181,-0.008772969,0.0039020278,0.018359566,-0.02897681,0.005634722,-0.028921258]]`

*Note:* The vector dimension are decided by the embedding model and the output value is dependent on model and input data.

**3. Retriever Microservice**
To validate the retriever microservice, you need to generate a mock embedding vector of length 768 in Python script:

```sh
export your_embedding=$(python3 -c "import random; embedding = [random.uniform(-1, 1) for _ in range(768)]; print(embedding)")
curl http://${host_ip}:7000/v1/retrieval \
  -X POST \
  -d '{"text":"What is the revenue of Nike in 2023?","embedding":"'"${your_embedding}"'"}' \
  -H 'Content-Type: application/json'
```

**4. Ollama MicroService**

```sh
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Are you AI?"}],
  "stream": false
}' | python3 -m json.tool
```

Response:

```json
{
    "model": "llama3.2",
    "created_at": "2025-04-09T15:43:17.593829077Z",
    "message": {
        "role": "assistant",
        "content": "Yes, I am an artificial intelligence (AI) model. I'm a computer program designed to simulate conversations, answer questions, and provide information on a wide range of topics. My primary function is to assist users like you with their queries, while also learning and improving over time.\n\nI'm built using a combination of natural language processing (NLP) and machine learning algorithms, which enable me to understand and respond to human language in a way that feels natural and intuitive.\n\nWhile I can provide helpful and accurate information, I'm not perfect and there may be times when I don't fully understand the context or nuances of a question. If you ever encounter any issues or confusion, feel free to ask for clarification or point out any errors!"
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 11943028348,
    "load_duration": 162411512,
    "prompt_eval_count": 29,
    "prompt_eval_duration": 273377107,
    "eval_count": 148,
    "eval_duration": 11506260969
}
```

**5. Dataprep Microservice**

To chat with retrieved information, you need to upload a file using Dataprep service. The dataprep microservice extracts the texts from variety of data sources, chunks the data, embeds each chunk using embedding microservice and store the embedded vectors in the redis vector database.

You can use the following commands to update the default knowledge base.

*Here is an example of Nike 2023 pdf file (Nike’s annual report on a form 10-K).*

```sh
# download pdf file
wget https://raw.githubusercontent.com/opea-project/GenAIComps/v1.1/comps/retrievers/redis/data/nke-10k-2023.pdf

# upload pdf file with dataprep
curl -X POST "http://${host_ip}:6007/v1/dataprep/ingest" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@./nke-10k-2023.pdf"
```

Output:
```
{"status":200,"message":"Data preparation succeeded"}
```

This command updates a knowledge base by uploading a local file for processing. Update the file path according to your environment.

*Alternatively*, you can add knowledge base via HTTP Links:
```sh
curl -X POST "http://${host_ip}:6007/v1/dataprep/ingest" \
     -H "Content-Type: multipart/form-data" \
     -F 'link_list=["https://opea.dev"]'
```
This command updates a knowledge base by submitting a list of HTTP links for processing.

**Get List of Uploaded Files:**
```sh
curl -X POST "http://${host_ip}:6007/v1/dataprep/get" \
     -H "Content-Type: application/json"
```

**Consume delete API:**
The `file_path` here should be the `id` get from `/v1/dataprep/get` API.

```sh
# delete link
curl -X POST "http://${host_ip}:6007/v1/dataprep/delete" \
     -d '{"file_path": "https://opea.dev.txt"}' \
     -H "Content-Type: application/json"

# delete file
curl -X POST "http://${host_ip}:6007/v1/dataprep/delete" \
     -d '{"file_path": "nke-10k-2023.pdf"}' \
     -H "Content-Type: application/json"

# delete all files and links
curl -X POST "http://${host_ip}:6007/v1/dataprep/delete" \
     -d '{"file_path": "all"}' \
     -H "Content-Type: application/json"
```

## Launch the UI

To access the frontend, open this URL: http://${host_ip}:80 in your browser. Port 80 is the default port we set for Nginx.

**Launch with origin port**
To access the frontend using the origin port, open the following URL in your browser: http://{host_ip}:5173. By default, the UI runs on port 5173 internally. If you prefer to use a different host port to access the frontend, you can modify the port mapping in the docker-compose.yaml file.

You should now see the ChatQnA web interface. You can enter a prompt to test the application.

## Cleanup the Deployment
When you are finished, you can stop and remove all the containers by running the below command from the same directory as the docker-compose.yaml file, Docker Compose will automatically detect and use it without needing the `-f` flag to specify the file path. 

To also remove all persistent volumes (including data) defined in your compose file include the `-v` flag.

```
docker compose down
```

## Troubleshooting

### ChatQnA UI Server Connection Issue - "Failed to load chat content" Error

If you do encounter the "failed to load chat content" error when interacting with the chat via UI, It's very likely related to an incorrect `.env` file() in UI server. It appears that this is a known bug with GenAIComps v1.2 and anyone using the prebuilt image from docker hub would be affected until OPEA publishes a new image with fix. You can learn more about the issue [here](https://github.com/opea-project/GenAIExamples/issues/1658). 

Check your UI server logs for any errors, to confirm if you're also seeing the below. 

```
TEI_EMBEDSvelteKitError: Not found: /v1/chatqna
2025-04-09 21:44:48 at resolve2 (file:///home/user/svelte/.svelte-kit/output/server/index.js:3204:18)
2025-04-09 21:44:48 at file:///home/user/svelte/.svelte-kit/output/server/index.js:3026:19
2025-04-09 21:44:48 at AsyncLocalStorage.run (node:async_hooks:346:14)
2025-04-09 21:44:48 at with_event (file:///home/user/svelte/.svelte-kit/output/server/index.js:66:22)
2025-04-09 21:44:48 at resolve (file:///home/user/svelte/.svelte-kit/output/server/index.js:3024:11)
2025-04-09 21:44:48 at init_promise.#options.hooks.handle (file:///home/user/svelte/.svelte-kit/output/server/index.js:3290:71)
2025-04-09 21:44:48 at file:///home/user/svelte/.svelte-kit/output/server/index.js:3019:28
2025-04-09 21:44:48 at AsyncLocalStorage.run (node:async_hooks:346:14)
2025-04-09 21:44:48 at with_event (file:///home/user/svelte/.svelte-kit/output/server/index.js:66:22)
2025-04-09 21:44:48 at respond (file:///home/user/svelte/.svelte-kit/output/server/index.js:3017:28) {
2025-04-09 21:44:48 status: 404,
2025-04-09 21:44:48 text: 'Not Found'DING_ENDPOINT
```

**Solution:** Building the UI server image from source should fix it. You can refer to the "Building Docker Images" section in this document for instructions on how to build the UI server image locally, which will resolve this connection issue.







