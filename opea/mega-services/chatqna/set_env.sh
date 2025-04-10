#!/usr/bin/env bash

# To make this script executable, run: chmod +x set_env.sh

# Determine the host IP address
export host_ip=$(hostname -I | awk '{print $1}')

if [ -z "${host_ip}" ]; then
  echo "Error: host_ip is not set. Please set host_ip first."
fi
echo "Setting host_ip to: ${host_ip}"

# Hugging Face API Token (replace the placeholder)
export HUGGINGFACEHUB_API_TOKEN="PLACE HF TOKEN HERE"

if [ "${HUGGINGFACEHUB_API_TOKEN}" == "PLACE HF TOKEN HERE" ]; then
  echo "Error: HUGGINGFACEHUB_API_TOKEN is not set. Please set HUGGINGFACEHUB_API_TOKEN."
fi

export EMBEDDING_MODEL_ID="BAAI/bge-base-en-v1.5"
export INDEX_NAME="rag-redis"
export OLLAMA_HOST=${host_ip}
export OLLAMA_MODEL="llama3.2"
export DATAPREP_SERVICE_PORT=6007
export RETRIEVER_SERVICE_PORT=7000
export LLM_ENDPOINT_PORT=11434
export BACKEND_SERVICE_PORT=8888
export FRONTEND_SERVICE_PORT=5173
export REDIS_PORT=6379

# Logging Flag (disabled by default, set to a non-empty string to enable)
export LOGFLAG=""

# If you are in a proxy environment, set the proxy-related environment variables:
#no_proxy="localhost,127.0.0.1"
#export no_proxy="$no_proxy,$host_ip,chatqna-aipc-backend-server,tei-embedding-service,retriever,tei-reranking-service,redis-vector-db,dataprep-redis-service,ollama-service"

echo "Environment variables for the ChatQnA MegaService have been set."